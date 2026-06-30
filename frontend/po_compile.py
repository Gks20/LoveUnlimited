"""Compile .po files to .mo without GNU msgfmt (Windows-friendly fallback)."""
import array
import struct
from pathlib import Path


def _unescape_po_string(value):
    if value is None:
        return ''
    return (
        value.replace('\\n', '\n')
        .replace('\\t', '\t')
        .replace('\\"', '"')
        .replace('\\\\', '\\')
    )


def _parse_po(path):
    entries = {}
    metadata = {}
    msgid = None
    msgstr = None
    fuzzy = False

    def store():
        nonlocal msgid, msgstr, fuzzy
        if msgid is None:
            return
        if fuzzy:
            msgid = msgstr = None
            fuzzy = False
            return
        if msgid == '':
            for line in (msgstr or '').split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip().lower()] = val.strip()
        else:
            entries[msgid] = msgstr or ''
        msgid = msgstr = None

    for raw_line in Path(path).read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if line.startswith('#,'):
            fuzzy = 'fuzzy' in line
            continue
        if line.startswith('msgid '):
            store()
            msgid = _unescape_po_string(line[6:].strip().strip('"'))
            msgstr = None
        elif line.startswith('msgstr '):
            msgstr = _unescape_po_string(line[7:].strip().strip('"'))
        elif line.startswith('"') and line.endswith('"'):
            chunk = _unescape_po_string(line[1:-1])
            if msgstr is None and msgid is not None:
                msgid += chunk
            elif msgstr is not None:
                msgstr += chunk
        elif not line:
            store()
    store()
    return metadata, entries


def compile_po_to_mo(po_path, mo_path):
    metadata, entries = _parse_po(po_path)
    header_lines = [
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ]
    if 'plural-forms' in metadata:
        header_lines.append(f"Plural-Forms: {metadata['plural-forms']}")
    header = '\n'.join(header_lines)
    catalog = {'': header}
    catalog.update(entries)

    ids = b''
    strs = b''
    keys = sorted(catalog.keys())
    offsets = []
    for key in keys:
        key_bytes = key.encode('utf-8')
        val_bytes = catalog[key].encode('utf-8')
        offsets.append((len(ids), len(key_bytes), len(strs), len(val_bytes)))
        ids += key_bytes + b'\0'
        strs += val_bytes + b'\0'

    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []
    for o_id, l_id, o_str, l_str in offsets:
        koffsets.append((l_id, o_id + keystart))
        voffsets.append((l_str, o_str + valuestart))

    output = array.array('I')
    output.append(0x950412de)
    output.append(0)
    output.extend((len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0))
    for length, offset in koffsets:
        output.extend((length, offset))
    for length, offset in voffsets:
        output.extend((length, offset))

    mo_path.parent.mkdir(parents=True, exist_ok=True)
    with open(mo_path, 'wb') as mo:
        mo.write(output.tobytes())
        mo.write(ids)
        mo.write(strs)


def compile_locale(locale_dir):
    base = Path(locale_dir)
    for po_file in base.glob('**/LC_MESSAGES/django.po'):
        compile_po_to_mo(po_file, po_file.with_suffix('.mo'))
