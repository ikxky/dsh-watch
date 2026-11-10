#!/usr/bin/env python3
"""Corpus consistency tests only, NOT a superagent evaluation runner."""
import hashlib, json, subprocess, wave
from pathlib import Path
r=Path(__file__).resolve().parent; g=r/'generated'
m=json.loads((g/'manifest.json').read_text())
a=[json.loads(x) for x in (g/'events.raw.jsonl').read_text().splitlines()]
b=[json.loads(x) for x in (g/'events.parsed.jsonl').read_text().splitlines()]
assert len(a)==len(b)==41
assert len({x['batch_id'] for x in a})==10
assert len({x['event_id'] for x in a})==41
assert [x['arrival_ms'] for x in a]==sorted(x['arrival_ms'] for x in a)
for x,y in zip(a,b):
    assert x['event_id']==y['event_id']
    for p,q in zip(x['attachments'],y['attachments']):
        assert (g/p['path']).exists() and 'parsed' not in p
        assert 'path' not in q and 'parsed' in q
for p in m['assets']:
    assert hashlib.sha256((g/p['path']).read_bytes()).hexdigest()==p['sha256']
for n in ['signal.wav','delivery.wav']:
    with wave.open(str(g/'media'/n)) as w: assert w.getnframes()>0 and w.getnchannels()==1
from PIL import Image
with Image.open(g/'media/venue.png') as im: im.verify()
from pypdf import PdfReader
assert len(PdfReader(g/'media/constraints.pdf').pages)==1
try: PdfReader(g/'media/broken.pdf')
except Exception: pass
else: raise AssertionError('bad PDF unexpectedly parsed')
video=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(g/'media/inventory.mp4')]))
assert float(video['format']['duration'])==2.0
expected=json.loads((r/'private/expected.json').read_text())
assert all(c['after'] in {x['event_id'] for x in a} for c in expected['checkpoints'])
print('PASS: 41 aligned events, 10 batches, hashes, arm isolation, image/PDF/WAV/video integrity and gold references. No model/framework tests were run.')

from project_event import project_event
for e in a+b:
    assert e['thread_id'] is None
    assert not {'supersedes','revokes','denies','duplicate_of'} & e.keys()
    if e['kind']=='message':
        projected=project_event(e)
        assert projected['occurred_ms']==e['occurred_ms'] and projected['arrival_ms']==e['arrival_ms']
        assert not {'event_id','batch_id','generation','fault','input_arm'} & projected.keys()
    else:
        try: project_event(e)
        except ValueError: pass
        else: raise AssertionError('non-message projected')
assert len({(x['source_instance'],x['source_message_id']) for x in a})==38
from collections import Counter
print('PASS: single-event projection, no scenario labels, controls rejected; counts:',dict(Counter(x['kind'] for x in a)))
