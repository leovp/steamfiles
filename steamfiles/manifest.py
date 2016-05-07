import struct
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

try:
    from .manifest_pb2 import Payload, Metadata, Signature
except ImportError:
    print('Run with protoc>=3.0.0: protoc --python_out=. manifest.proto')
    raise

MSG_PAYLOAD = 0x71F617D0
MSG_METADATA = 0x1F4812BE
MSG_SIGNATURE = 0x1B81B817
MSG_EOF = 0x32C415AB

MSG_NAMES = {
    MSG_PAYLOAD: 'payload',
    MSG_METADATA: 'metadata',
    MSG_SIGNATURE: 'signature',
}

MessageClass = {
    MSG_PAYLOAD: Payload,
    MSG_METADATA: Metadata,
    MSG_SIGNATURE: Signature
}


def load(fp):
    return loads(fp.read())


def loads(data):
    data = memoryview(data)
    offset = 0
    parsed = {}
    int32 = struct.Struct('<I')

    while True:
        msg_id, = int32.unpack_from(data, offset)
        offset += int32.size

        if msg_id == MSG_EOF:
            break

        msg_size, = int32.unpack_from(data, offset)
        offset += int32.size

        msg_data = data[offset:offset + msg_size]
        offset += msg_size

        message = MessageClass[msg_id]()
        message.ParseFromString(msg_data)

        parsed[MSG_NAMES[msg_id]] = protobuf_to_dict(message)

    return parsed['metadata']


def dump(obj, fp):
    fp.write(dumps(obj))


def dumps(obj):
    raise NotImplementedError
