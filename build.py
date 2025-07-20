import urllib.parse
import itertools
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

    count_func = itertools.count(0)
    ref_map = {}

    data = fr.read()

    def process_citenote(m: re.Match[str]) -> str:
        num = next(count_func)
        ref_map[m[2]] = num
        return '\n'.join([
            '%(tabs)s<li id="cite-note-%(num)d" value="%(num)d">',
            '%(tabs)s\t<a href="#cite-ref-%(num)d">↑</a>',
            '%(tabs)s\t<a href="%(href)s">%(link)s</a>',
            '%(tabs)s</li>',
        ]) % {
            'tabs': m[1],
            'num': num,
            'href': m[3],
            'link': m[4],
        }
    data = re.sub(
        r'(\t+)<citenote value="([^"]+)" href="([^"]+)">([^"]+)</citenote>',
        process_citenote,
        data,
    )

    def process_citeref(m: re.Match[str]) -> str:
        return (
            '<a id="cite-ref-%(num)d" href="#cite-note-%(num)d">[%(num)d]</a>'
        ) % {
            'num': ref_map[m[1]],
        }
    data = re.sub(
        r'\s*<citeref>([^<]+)</citeref>',
        process_citeref,
        data,
    )

    def process_header(m: re.Match[str]) -> str:
        return (
            '<%(head)s id="%(esc)s">%(name)s</%(head)s>'
        ) % {
            'head': m[1],
            'name': m[2],
            'esc': urllib.parse.quote(m[2]).replace(' ', '-'),
        }
    data = re.sub(
        r'<(h[234])>([^<]+)</\1>',
        process_header,
        data,
    )

    def process_catalogue(m: re.Match[str]) -> str:
        return ''.join([
            f'{m.group(1)}<div class="catalogue">',
            *(
                f'<a href="{p}">{p}</a>'
                for p in glob.glob(m.group(2), root_dir=DRAFT_PREFIX)
            ),
            "</div>",
        ])
    data = re.sub(
        r'(\t+)<catalogue>([^"]+)</catalogue>',
        process_catalogue,
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
