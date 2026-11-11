#!/usr/bin/env python3
"""Check this package's Markdown local links without network access.

Supports inline links/images, reference definitions, ATX heading fragments and
explicit id/name anchors used by these docs. Not a general Markdown renderer.
Code fences and inline code are ignored. External URLs are reported, not fetched.
"""
import argparse
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def prose(text):
    lines, fence = [], None
    for line in text.splitlines():
        mark = re.match(r'^\s*(`{3,}|~{3,})', line)
        if mark:
            token = mark.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            lines.append('')
        else:
            lines.append('' if fence else re.sub(r'`+[^`]*`+', '', line))
    return '\n'.join(lines)


def anchors(text):
    clean = prose(text)
    result = set(re.findall(r'\b(?:id|name)=["\']([^"\']+)', clean))
    counts = {}
    for match in re.finditer(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', clean, re.M):
        title = re.sub(r'<[^>]+>', '', match.group(1)).lower()
        title = re.sub(r'[^\w\-\s]', '', title).replace(' ', '-')
        n = counts.get(title, 0)
        counts[title] = n + 1
        result.add(title if n == 0 else f'{title}-{n}')
    return result


def check(root):
    root = root.resolve()
    errors, local, external = [], 0, 0
    files = sorted(p for p in root.rglob('*.md') if not any(
        x in {'.git', 'node_modules', '__pycache__'} for x in p.relative_to(root).parts))
    for doc in files:
        clean = prose(doc.read_text(encoding='utf-8'))
        links = list(re.finditer(r'\]\(([^)\n]+)\)', clean))
        links += list(re.finditer(r'^\s{0,3}\[[^]\n]+\]:\s*(\S+)', clean, re.M))
        for match in links:
            # Optional Markdown title; package paths do not contain literal spaces.
            raw = match.group(1).strip().split()[0].strip('<>')
            ref = urlsplit(raw)
            label = f'{doc.relative_to(root)}:{clean[:match.start()].count(chr(10))+1}'
            if ref.scheme in {'http', 'https', 'mailto'}:
                external += 1
                continue
            if ref.scheme or ref.netloc or raw.startswith(('/', '\\')) or '\\' in raw:
                errors.append(f'{label}: non-portable local link {raw}')
                continue
            path = unquote(ref.path)
            target = (doc.parent / path).resolve() if path else doc
            local += 1
            if not target.is_relative_to(root):
                errors.append(f'{label}: escapes superagent-poc root: {raw}')
            elif not target.exists():
                errors.append(f'{label}: missing target: {raw}')
            elif ref.fragment and target.suffix.lower() == '.md':
                if unquote(ref.fragment) not in anchors(target.read_text(encoding='utf-8')):
                    errors.append(f'{label}: missing fragment: {raw}')
    return {'markdown_files': len(files), 'local_links': local,
            'external_links_not_fetched': external, 'errors': errors}


def self_test():
    with tempfile.TemporaryDirectory(prefix='poc-links-') as temp:
        root = Path(temp)
        (root / 'sub').mkdir()
        (root / 'README.md').write_text('# Entry\n[child](sub/page.md#hello)\n', encoding='utf-8')
        child = root / 'sub/page.md'
        child.write_text('# Hello\n[root](../README.md)\n```md\n[x](missing.md)\n```\n', encoding='utf-8')
        assert not check(root)['errors']
        child.write_text('# Hello\n[x](../../outside.md)\n[y](/README.md)\n[z](missing.md)\n[a](../README.md#missing)\n', encoding='utf-8')
        assert len(check(root)['errors']) == 4
    print('PASS: link-checker self-test (valid links, fences, escape, absolute, missing, fragment)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if not args.root.is_dir():
        parser.error('--root must be an existing package directory')
    result = check(args.root)
    errors = result.pop('errors')
    for error in errors:
        print('FAIL:', error)
    failed = bool(errors)
    print(('FAIL' if failed else 'PASS') + ': ' + str(result))
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
