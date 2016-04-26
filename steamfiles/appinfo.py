import struct
from functools import partial

VDF_VERSION = 0x07564426
VDF_UNIVERSE = 0x00000001


def load(fp):
    return loads(fp.read())


def loads(content):
    if not isinstance(content, (bytes, bytearray)):
        raise TypeError('the Appinfo object must be a bytes-like object')

    return AppinfoDecoder(content).decode()


def dump(fp, obj):
    fp.write(dumps(obj))


def dumps(obj):
    raise NotImplementedError


class AppinfoDecoder:

    def __init__(self, content):
        self.content = content  # Incoming data (bytes)
        self.offset = 0         # Parsing offset
        self.data = {}          # Output (dictionary)

        # Functions to parse different data structures.
        self.value_parsers = {
            0x00: self.parse_subsections,
            0x01: self.read_string,
            0x02: partial(self.read_struct, 'I'),
            0x07: partial(self.read_struct, 'Q')
        }

    def decode(self):
        header_fields = ('version', 'universe')
        header = dict(zip(header_fields, self.read_struct('2I')))

        # Currently these are the only possible values for
        # a valid appinfo.vdf
        assert header['version'] == VDF_VERSION
        assert header['universe'] == VDF_UNIVERSE

        # Parsing applications
        fields = ('size', 'state', 'last_update', 'access_token', 'checksum', 'change_number')
        while True:
            app_id = self.read_struct('I')

            # AppID = 0 marks the last application in the Appinfo
            if not app_id:
                break

            app = dict(zip(fields, self.read_game_header()))
            app['sections'] = {}
            while True:
                section_id = self.read_byte()
                if not section_id:
                    break

                # Skip the 0x00 byte before section name.
                self.offset += 1

                section_name = self.read_string()
                app['sections'][section_name] = self.parse_subsections(root_section=True)

            self.data[app_id] = app

        return self.data

    def read_game_header(self):
        game_header = self.read_struct('<3IQ20sI')
        return game_header

    def parse_subsections(self, root_section=False):
        subsection = {}

        while True:
            value_type = self.read_byte()
            if value_type == 0x08:
                if root_section:
                    # There's one additional 0x08 byte at the end of
                    # the root subsection.
                    self.offset += 1
                break

            key = self.read_string()
            value = self.value_parsers.get(value_type, self._unknown_value_type)()

            subsection[key] = value

        return subsection

    def read_struct(self, fmt):
        result = struct.unpack_from(fmt, self.content, self.offset)
        self.offset += struct.calcsize(fmt)

        # A hack to return the value itself instead of a tuple of one element.
        if len(fmt) == 1:
            return result[0]
        else:
            return result

    def read_byte(self):
        byte = self.content[self.offset]
        self.offset += 1
        return byte

    def read_string(self):
        start = self.offset
        end = self.content.find(b'\0', self.offset)
        self.offset = end + 1
        return self.content[start:end]

    @staticmethod
    def _unknown_value_type():
        raise ValueError("Cannot parse the provided data type.")
