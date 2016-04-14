SECTION_START = '{'
SECTION_END = '}'


def loads(content):
    data = {}
    current_section = data
    sections = []

    lines = (line.replace('"', '').strip() for line in content.splitlines())
    for line in lines:
        if not line:
            continue

        try:
            key, value = line.split(None, 1)
        except ValueError:
            if line == SECTION_START:
                # Initialize the last added section.
                current_section = _prepare_subsection(data, sections)
            elif line == SECTION_END:
                # Remove the last section from the queue.
                sections.pop()
            else:
                # Add a new section to the queue.
                sections.append(line)
            continue

        current_section[key] = value

    return data


def load(fp):
    return loads(fp.read())


def dumps(obj):
    raise NotImplementedError


def dump(fp, obj):
    raise NotImplementedError


def _prepare_subsection(data, sections):
    current = data
    for i in sections[:-1]:
        current = current[i]

    current[sections[-1]] = {}
    return current[sections[-1]]
