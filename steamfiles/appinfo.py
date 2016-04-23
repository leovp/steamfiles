VDF_VERSION = 0x07564426
VDF_UNIVERSE = 0x00000001


def load(fp):
    return loads(fp.read())


def loads(content):
    raise NotImplementedError


def dump(fp, obj):
    fp.write(dumps(obj))


def dumps(obj):
    raise NotImplementedError
