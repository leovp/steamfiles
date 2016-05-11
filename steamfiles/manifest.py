import struct
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

__all__ = ('load', 'loads', 'dump', 'dumps')

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

MSG_IDS = {
    'payload': MSG_PAYLOAD,
    'metadata': MSG_METADATA,
    'signature': MSG_SIGNATURE,
}

MessageClass = {
    MSG_PAYLOAD: Payload,
    MSG_METADATA: Metadata,
    MSG_SIGNATURE: Signature
}


def load(fp):
    return loads(fp.read())


def loads(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('can only load a bytes-like object as a Manifest')

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

    return parsed


def dump(obj, fp):
    fp.write(dumps(obj))


def dumps(obj):
    if not isinstance(obj, dict):
        raise TypeError('can only dump a dictionary as a Manifest')

    data = []
    int32 = struct.Struct('<I')

    for message_name in ('payload', 'metadata', 'signature'):
        message_data = obj[message_name]
        message_id = MSG_IDS[message_name]
        message_class = MessageClass[message_id]
        message = dict_to_protobuf(message_class, message_data)
        message_bytes = message.SerializeToString()
        message_size = len(message_bytes)

        data.append(int32.pack(message_id))
        data.append(int32.pack(message_size))
        data.append(message_bytes)

    # MSG_EOF marks the end of messages.
    data.append(int32.pack(MSG_EOF))
    return b''.join(data)
