__all__ = ('load', 'loads', 'dump', 'dumps')

SECTION_START = '{'
SECTION_END = '}'


def loads(data, wrapper=dict):
    """
    Loads ACF content into a Python object.
    :param data: An UTF-8 encoded content of an ACF file.
    :param wrapper: A wrapping object for key-value pairs.
    :return: An Ordered Dictionary with ACF data.
    """
    if not isinstance(data, str):
        raise TypeError('can only load a str as an ACF')

    parsed = wrapper()
    current_section = parsed
    sections = []

    lines = (line.strip() for line in data.splitlines())

    for line in lines:
        try:
            key, value = line.split(None, 1)
            key = key.replace('"', '').lstrip()
            value = value.replace('"', '').rstrip()
        except ValueError:
            if line == SECTION_START:
                # Initialize the last added section.
                current_section = _prepare_subsection(parsed, sections, wrapper)
            elif line == SECTION_END:
                # Remove the last section from the queue.
                sections.pop()
            else:
                # Add a new section to the queue.
                sections.append(line.replace('"', ''))
            continue

        current_section[key] = value

    return parsed


def load(fp, wrapper=dict):
    """
    Loads the contents of an ACF file into a Python object.
    :param fp: A file object.
    :param wrapper: A wrapping object for key-value pairs.
    :return: An Ordered Dictionary with ACF data.
    """
    return loads(fp.read(), wrapper=wrapper)


def dumps(obj):
    """
    Serializes a dictionary into ACF data.
    :param obj: A dictionary to serialize.
    :return: ACF data.
    """
    if not isinstance(obj, dict):
        raise TypeError('can only dump a dictionary as an ACF')

    return '\n'.join(_dumps(obj, level=0)) + '\n'


def dump(obj, fp):
    """
    Serializes a dictionary into ACF data and writes it to a file.
    :param obj: A dictionary to serialize.
    :param fp: A file object.
    """
    fp.write(dumps(obj))


def _dumps(obj, level):
    """
    Does the actual serializing of data into an ACF format.
    :param obj: A dictionary to serialize.
    :param level: Nesting level.
    :return: A List of strings.
    """
    lines = []
    indent = '\t' * level

    for key, value in obj.items():
        if isinstance(value, dict):
            # [INDENT]"KEY"
            # [INDENT]{
            line = indent + '"{}"\n'.format(key) + indent + '{'
            lines.append(line)
            # Increase intendation of the nested dict
            lines.extend(_dumps(value, level+1))
            # [INDENT]}
            lines.append(indent + '}')
        else:
            # [INDENT]"KEY"[TAB][TAB]"VALUE"
            lines.append(indent + '"{}"'.format(key) + '\t\t' + '"{}"'.format(value))

    return lines


def _prepare_subsection(data, sections, wrapper):
    """
    Creates a subsection ready to be filled.
    :param data: Semi-parsed dictionary.
    :param sections: A list of sections.
    :param wrapper: A wrapping object for key-value pairs.
    :return: A newly created subsection.
    """
    current = data
    for i in sections[:-1]:
        current = current[i]

    current[sections[-1]] = wrapper()
    return current[sections[-1]]
