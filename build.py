import re
import os


def convert(name: str) -> None:
    fr = open(f'draft/{name}', 'r', encoding='utf-8')
    to = open(f'{name}', 'w', encoding='utf-8')

    data = fr.read()
    data = re.sub(
        '(\t+)<citenote value="(\d+)" href="([^"]+)">([^"]+)</citenote>',
        '\\1<li id="cite-note-\\2" value="\\2">\n\\1\t<a href="#cite-ref-\\2">↑</a>\n\\1\t<a href="\\3">\\4</a>\n\\1</li>',
        data,
    )
    data = re.sub(
        '\s*<citeref>(\d+)</citeref>',
        '<a id="cite-ref-\\1" href="#cite-note-\\1">[\\1]</a>',
        data,
    )

    to.write(data)
    fr.close()
    to.close()


if __name__ == '__main__':
    for name in os.listdir('draft/'):
        convert(name)
