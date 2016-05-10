import struct
from collections import OrderedDict, namedtuple

__all__ = ('load', 'loads', 'dump', 'dumps')

VDF_VERSION = 0x07564426
VDF_UNIVERSE = 0x00000001

LAST_SECTION = b'\x00'
LAST_APP = b'\x00\x00\x00\x00'
SECTION_END = b'\x08'

TYPE_SECTION = b'\x00'
TYPE_STRING = b'\x01'
TYPE_INT32 = b'\x02'
TYPE_INT64 = b'\x07'

# VDF has variable length integers (32-bit and 64-bit).
Integer = namedtuple('Integer', ('size', 'data'))


def load(fp):
    return loads(fp.read())


def loads(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('can only load a bytes-like object as an Appinfo')

    return AppinfoDecoder(data).decode()


def dump(obj, fp):
    fp.write(dumps(obj))


def dumps(obj):
    if not isinstance(obj, dict):
        raise TypeError('can only dump a dictionary as an Appinfo')

    return b''.join(AppinfoEncoder(obj).iter_encode())


class AppinfoDecoder:

    def __init__(self, data):
        self.data = memoryview(data)  # Incoming data (bytes)
        self.offset = 0               # Parsing offset

        # Commonly used structs
        self._read_int32 = self.make_custom_reader('<I', single_value=True)
        self._read_int64 = self.make_custom_reader('<Q', single_value=True)
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
        parsed = OrderedDict()

        header_fields = ('version', 'universe')
        header = OrderedDict(zip(header_fields, self.read_vdf_header()))

        # Currently these are the only possible values for
        # a valid appinfo.vdf
        assert header['version'] == VDF_VERSION
        assert header['universe'] == VDF_UNIVERSE

        # Parsing applications
        app_fields = ('size', 'state', 'last_update', 'access_token', 'checksum', 'change_number')
        while True:
            app_id = self._read_int32()

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
                app['sections'][section_name]['__steamfiles_section_id'] = section_id

            parsed[app_id] = app

        return parsed

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
            result = custom_struct.unpack_from(self.data, self.offset)
            self.offset += custom_struct.size
            return result

        def return_one():
            result = custom_struct.unpack_from(self.data, self.offset)
            self.offset += custom_struct.size
            return result[0]

        if single_value:
            return return_one
        else:
            return return_many

    def read_int32(self):
        number = self._read_int32()
        return Integer(data=number, size=32)

    def read_int64(self):
        number = self._read_int64()
        return Integer(data=number, size=64)

    def read_byte(self):
        byte = self.data[self.offset]
        self.offset += 1
        return byte

    def read_string(self):
        for index, value in enumerate(self.data[self.offset:]):
            # NUL-byte – a string's end
            if value != 0:
                continue

            string = slice(self.offset, self.offset + index)
            self.offset += index + 1
            return self.data[string].tobytes()

    @staticmethod
    def _unknown_value_type():
        raise ValueError("Cannot parse the provided data type.")


class AppinfoEncoder:

    def __init__(self, data):
        self.data = data

    def iter_encode(self):
        # VDF Header
        yield struct.pack('<2I', VDF_VERSION, VDF_UNIVERSE)

        for app_id, app_data in self.data.items():
            # Game Header
            yield struct.pack('<I', app_id)
            yield struct.pack('<3IQ20sI', app_data['size'], app_data['state'],
                              app_data['last_update'], app_data['access_token'],
                              app_data['checksum'], app_data['change_number'])

            for section_name, section_data in app_data['sections'].items():
                # Delete '_section_id' from the dictionary, as it was placed there by
                # the decoding class only to preserve the section id number.
                section_id = section_data['__steamfiles_section_id']

                yield struct.pack('<H', section_id)
                yield self.encode_string(section_name)
                yield from self.iter_encode_section(section_data, root_section=True)

            yield LAST_SECTION

        yield LAST_APP

    def iter_encode_section(self, section_data, root_section=False):
        for key, value in section_data.items():
            if key == '__steamfiles_section_id':
                continue

            # Encode different types using their corresponding generators.
            if isinstance(value, dict):
                yield TYPE_SECTION
                yield self.encode_string(key)
                yield from self.iter_encode_section(value)
            elif isinstance(value, bytes):
                yield TYPE_STRING
                yield self.encode_string(key)
                yield self.encode_string(value)
            elif isinstance(value, Integer):
                yield from self.encode_integer(key, value)
            else:
                raise TypeError('Unknown value type')

        yield SECTION_END
        if root_section:
            # There's one additional 0x08 byte at the end of
            # the root subsection.
            yield SECTION_END

    def encode_integer(self, key, value):
        if value.size == 32:
            yield TYPE_INT32
            yield self.encode_string(key)
            yield struct.pack('<I', value.data)
        elif value.size == 64:
            yield TYPE_INT64
            yield self.encode_string(key)
            yield struct.pack('<Q', value.data)
        else:
            raise TypeError('Unknown type of an Integer')

    @staticmethod
    def encode_string(string):
        # A string with a NUL-byte at the end.
        # Example format for 'gameid': "7s".
        # The bytes packed with above format: b'gameid\x00'.
        fmt = str(len(string) + 1) + 's'
        return struct.pack(fmt, string)
