#!/usr/bin/env python3
"""Build an ordered gallery manifest from curated tiles plus newly added assets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'gallery-baseline.json').read_text())
VALID = {'nature', 'light', 'places', 'events', 'portraits', 'silhouette'}
EXCLUDED = set(BASELINE['excluded'])
CURATED = BASELINE['curated']

def category(path):
    folder = path.parts[1]
    return 'events' if folder == 'weddings' else folder

def asset(path):
    return path.startswith('assets/') and (ROOT / path).is_file()

items = []
seen = set()
for item in CURATED:
    path = item['src']
    if path in seen or not asset(path):
        continue
    seen.add(path)
    items.append(item)

for file in sorted((ROOT / 'assets').rglob('*')):
    if not file.is_file() or file.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}:
        continue
    rel = file.relative_to(ROOT).as_posix()
    cat = category(Path(rel))
    if cat not in VALID or rel in seen or rel in EXCLUDED:
        continue
    name = file.stem.replace('-', ' ').replace('_', ' ')
    items.append({'src': rel, 'cat': cat, 'alt': name, 'class': ''})
    seen.add(rel)

(ROOT / 'gallery-manifest.json').write_text(json.dumps(items, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote {len(items)} photos ({len(items)-len(CURATED)} new)')
