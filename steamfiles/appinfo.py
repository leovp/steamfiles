import struct
from collections import OrderedDict

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
        self.content = memoryview(content)  # Incoming data (bytes)
        self.offset = 0                     # Parsing offset
        self.data = OrderedDict()           # Output (dictionary)

        # Commonly used structs
        self.read_int32 = self.make_custom_reader('<I', single_value=True)
        self.read_int64 = self.make_custom_reader('<Q', single_value=True)
        self.read_vdf_header = self.make_custom_reader('<2I')
        self.read_game_header = self.make_custom_reader('<3IQ20sI')

        # Functions to parse different data structures.
        self.value_parsers = {
            0x00: self.parse_subsections,
            0x01: self.read_string,
            0x02: self.read_int32,
            0x07: self.read_int64,
        }

    def decode(self):
        header_fields = ('version', 'universe')
        header = OrderedDict(zip(header_fields, self.read_vdf_header()))

        # Currently these are the only possible values for
        # a valid appinfo.vdf
        assert header['version'] == VDF_VERSION
        assert header['universe'] == VDF_UNIVERSE

        # Parsing applications
        app_fields = ('size', 'state', 'last_update', 'access_token', 'checksum', 'change_number')
        while True:
            app_id = self.read_int32()

            # AppID = 0 marks the last application in the Appinfo
            if not app_id:
                break

            app = OrderedDict(zip(app_fields, self.read_game_header()))
            app['sections'] = OrderedDict()
            while True:
                section_id = self.read_byte()
                if not section_id:
                    break

                # Skip the 0x00 byte before section name.
                self.offset += 1

                section_name = self.read_string()
                app['sections'][section_name] = self.parse_subsections(root_section=True)

                # New Section ID's could be added in the future, or changes could be made to
                # existing ones, so instead of maintaining a table of section names and their
                # corresponding IDs, we are going to store the IDs with all the data.
                app['sections'][section_name]['_section_id'] = section_id

            self.data[app_id] = app

        return self.data

    def parse_subsections(self, root_section=False):
        subsection = OrderedDict()

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

    def make_custom_reader(self, fmt, single_value=False):
        custom_struct = struct.Struct(fmt)

        def return_many():
            result = custom_struct.unpack_from(self.content, self.offset)
            self.offset += custom_struct.size
            return result

        def return_one():
            result = custom_struct.unpack_from(self.content, self.offset)
            self.offset += custom_struct.size
            return result[0]

        if single_value:
            return return_one
        else:
            return return_many

    def read_byte(self):
        byte = self.content[self.offset]
        self.offset += 1
        return byte

    def read_string(self):
        for index, value in enumerate(self.content[self.offset:]):
            # NUL-byte – a string's end
            if value != 0:
                continue

            string = slice(self.offset, self.offset + index)
            self.offset += index + 1
            return self.content[string].tobytes()

    @staticmethod
    def _unknown_value_type():
        raise ValueError("Cannot parse the provided data type.")
