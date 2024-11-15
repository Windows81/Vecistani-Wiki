import os.path
import shutil
import glob
import re
import os

DRAFT_PREFIX = './draft'
WWW_PREFIX = './www'


def convert(name: str) -> None:
    fr_path = f'{DRAFT_PREFIX}/{name}'
    to_path = f'{WWW_PREFIX}/{name}'
    print(fr_path, '>>', to_path)
    if os.path.isdir(fr_path):
        shutil.copytree(fr_path, to_path, dirs_exist_ok=True)
        return

    fr = open(fr_path, 'r', encoding='utf-8')
    to = open(to_path, 'w', encoding='utf-8')

    data = fr.read()
    data = re.sub(
        r'(\t+)<citenote value="(\d+)" href="([^"]+)">([^"]+)</citenote>',
        r'\1<li id="cite-note-\2" value="\2">\n\1\t<a href="#cite-ref-\2">↑</a>\n\1\t<a href="\3">\4</a>\n\1</li>',
        data,
    )
    data = re.sub(
        r'\s*<citeref>(\d+)</citeref>',
        r'<a id="cite-ref-\1" href="#cite-note-\1">[\1]</a>',
        data,
    )
    data = re.sub(
        r'(\t+)<catalogue>([^"]+)</catalogue>',
        lambda m: ''.join([
            f'{m.group(1)}<div class="catalogue">',
            *(
                f'<a href="{p}">{p}</a>'
                for p in glob.glob(m.group(2), root_dir=DRAFT_PREFIX)
            ),
            "</div>",
        ]),
        data,
    )

    to.write(data)
    fr.close()
    to.close()


if __name__ == '__main__':
    os.makedirs(WWW_PREFIX, exist_ok=True)
    shutil.copytree('./internal', f'{WWW_PREFIX}/internal', dirs_exist_ok=True)
    for name in os.listdir(DRAFT_PREFIX):
        convert(name)
