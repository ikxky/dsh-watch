#!/usr/bin/env python3
"""Validate corpus and preparation tooling; never evaluates agent quality."""
import argparse
import json
import subprocess
import tempfile
import wave
from pathlib import Path
from datetime import timedelta

from replay import SOURCES, checked_time, load, parse_time, source_at, stage, verified_fixture

ROOT=Path(__file__).resolve().parent


def validate(root):
    m=verified_fixture(root)
    events=load(root,'controller/events.json')
    annotations=load(root,'controller/annotations.json')
    assert len(events)==m['delivery_count']==48
    assert len({(e['source_instance'],e['source_message_id']) for e in events})==47
    assert len(annotations)==len(events)
    assert len({a['batch'] for a in annotations})==16
    times=[parse_time(e['received_at']) for e in events]
    assert times==sorted(times)
    deltas=[(b-a).total_seconds() for a,b in zip(times,times[1:])]
    assert min(deltas)==2 and max(deltas)>60*60*48 and len(set(deltas))>10
    assert all(parse_time(e['occurred_at'])<=parse_time(e['received_at']) for e in events)
    assert sum(e['occurred_at']!=e['received_at'] for e in events)==2
    assert all(e['native_thread_id'] is None for e in events)
    for e in events:
        assert not set(e)&{'cases','batch','expected','duplicate_of','gold'}
        for a in e['attachments']:
            assert (root/a['ref']).is_file()
    duplicates=[e for e in events if e['source_message_id']=='m014']
    for field in ('source_instance','source_message_id','revision','actor','text','attachments','occurred_at'):
        assert duplicates[0][field]==duplicates[1][field]
    timeline=load(root,'controller/source-timeline.json')
    oracle=load(ROOT,'review-only/checkpoints.json')
    ids={e['delivery_id'] for e in events}
    assert all(set(c.get('evidence_deliveries',[]))<=ids for c in oracle['checks'])
    by_id={e['delivery_id']:e for e in events}
    assert all(parse_time(by_id[eid]['received_at'])<=parse_time(c['at'])
               for c in oracle['checks'] for eid in c.get('evidence_deliveries',[]))
    for s in timeline:
        for item in s['items']:
            assert parse_time(item['published_at'])<=parse_time(s['available_at'])
    from PIL import Image
    from pypdf import PdfReader
    Image.open(root/'assets/quote-a.png').verify()
    assert len(PdfReader(root/'assets/purchase-change.pdf').pages)==1
    with wave.open(str(root/'assets/demo-change.wav')) as w:
        duration=w.getnframes()/w.getframerate()
        assert duration>5
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(root/'assets/badge-stock.mp4')]))
    assert abs(float(probe['format']['duration'])-3)<0.05
    broken=False
    try:
        PdfReader(root/'assets/agenda-damaged.pdf')
    except Exception:
        broken=True
    assert broken
    with tempfile.TemporaryDirectory() as temp:
        base=Path(temp)
        stage(root,'2026-11-16T09:02:11+08:00','raw',base/'early')
        texts=''.join(p.read_text() for p in (base/'early').rglob('*.json*'))
        assert '93'+'000' not in texts and 'fixture-plugin-0.8' not in texts and 'd001' not in texts
        assert 'controller' not in texts and 'cases' not in texts
        names={p.name for p in (base/'early/attachments').rglob('*') if p.is_file()}
        assert names=={'purchase-request.md','quote-a.png','project-brief.md','quote-b.csv','activity-brief.md'}
        stage(root,'2026-11-17T10:36:08+08:00','parsed',base/'parsed',after='2026-11-17T10:36:00+08:00')
        lines=[json.loads(line) for line in (base/'parsed/inbox.jsonl').read_text().splitlines()]
        assert len(lines)==3 and not (base/'parsed/attachments').exists()
        assert 'reference_extraction' in lines[1]['attachments'][0]
        assert not any(p.name.startswith('expected') or p.name=='manifest.json' for p in (base/'parsed').rglob('*'))
        for arm in ('raw','parsed'):
            target=base/f'pending-{arm}'
            stage(root,'2026-11-18T08:51:05+08:00',arm,target,after='2026-11-18T08:51:02+08:00')
            pending=json.loads((target/'inbox.jsonl').read_text())
            assert pending['attachments'][0]['availability']=='pending'
            assert 'ref' not in pending['attachments'][0] and 'reference_extraction' not in pending['attachments'][0]
            assert not (target/'attachments').exists()
            release='2026-11-18T08:53:00+08:00' if arm=='raw' else '2026-11-18T08:54:00+08:00'
            target=base/f'ready-{arm}'
            stage(root,release,arm,target,after='2026-11-18T08:52:10+08:00')
            ready=json.loads((target/'inbox.jsonl').read_text())
            assert ready['event_type']=='media_ready' and ready['derived_from']=='office-a:m023:r1'
        target=base/'reference-not-yet'
        stage(root,'2026-11-18T08:53:59+08:00','parsed',target,after='2026-11-18T08:52:10+08:00')
        assert not (target/'inbox.jsonl').read_text()
        try:
            stage(root,'2026-11-16T09:02:11+08:00','raw',base/'early')
            raise AssertionError('Existing stage not rejected')
        except ValueError:
            pass
        # Every message, source revision and media boundary: before/equal/after.
        boundaries=set(times+[parse_time(x['available_at']) for x in timeline])
        for e in events:
            for a in e['attachments']:
                for key in ('available_at','reference_available_at'):
                    if key in a:
                        boundaries.add(parse_time(a[key]))
        boundaries={x+timedelta(seconds=d) for x in boundaries for d in (-1,0,1)
                    if parse_time(m['epoch'])<=x+timedelta(seconds=d)<=parse_time(m['end'])}
        for n, cutoff in enumerate(sorted(boundaries)):
            arms={}
            for arm in ('raw','parsed'):
                folder=base/f'boundary-{n}-{arm}'
                stage(root,cutoff.isoformat(),arm,folder)
                projected=[json.loads(line) for line in (folder/'inbox.jsonl').read_text().splitlines()]
                expected=[e for e in events if parse_time(e['received_at'])<=cutoff]
                assert len(projected)==len(expected)
                for original,visible in zip(expected,projected):
                    assert visible['text']==original['text']
                    assert visible['received_at']==original['received_at']
                    assert not set(visible)&{'cases','batch','delivery_id','expected'}
                    for a,v in zip(original['attachments'],visible['attachments']):
                        available=a.get('reference_available_at' if arm=='parsed' else 'available_at',original['received_at'])
                        if parse_time(available)>cutoff:
                            assert v['availability']=='pending' and 'ref' not in v and 'reference_extraction' not in v
                        elif arm=='raw':
                            assert (folder/v['ref']).is_file()
                        else:
                            assert v['reference_extraction']==load(root,'controller/parsed-reference.json')[a['name']]
                for source in SOURCES:
                    value=load(folder,f'sources/{source}.json')
                    assert value==source_at(root,source,cutoff.isoformat())
                    assert all(parse_time(x['published_at'])<=cutoff for x in value.get('items',[]))
                expected_paths={'inbox.jsonl','clock.json','identity-map.json'}|{f'sources/{s}.json' for s in SOURCES}
                expected_paths|={a['ref'] for e in projected for a in e['attachments'] if 'ref' in a}
                assert {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}==expected_paths
                arms[arm]=[{k:v for k,v in x.items() if k!='attachments'} for x in projected]
            assert arms['raw']==arms['parsed']
        try:
            stage(root,'2026-11-16T09:02:11+08:00','raw',base/'reverse',after='2026-11-17T10:36:00+08:00')
            raise AssertionError('Reverse time not rejected')
        except ValueError:
            pass
    first=source_at(root,'deepseek-plugin','2026-11-16T09:03:00+08:00')
    unchanged=source_at(root,'deepseek-plugin','2026-11-17T16:00:00+08:00',first['etag'])
    assert unchanged['status']==304 and 'items' not in unchanged
    fail=source_at(root,'deepseek-plugin','2026-11-18T16:00:00+08:00',first['etag'])
    assert fail['status']==503 and 'etag' not in fail and 'items' not in fail
    recovered=source_at(root,'deepseek-plugin','2026-11-19T09:00:00+08:00',first['etag'])
    assert recovered['status']==304
    change=source_at(root,'deepseek-plugin','2026-11-23T09:00:00+08:00',first['etag'])
    assert change['status']==200 and len(change['items'])==2
    old=source_at(root,'llm-news','2026-11-23T16:00:00+08:00')
    new=source_at(root,'llm-news','2026-11-24T09:03:00+08:00')
    assert next(x for x in old['items'] if x['item_id']=='n103')['revision']==1
    assert next(x for x in new['items'] if x['item_id']=='n103')['revision']==2
    withdrawn=source_at(root,'llm-news','2026-11-27T16:00:00+08:00')
    assert next(x for x in withdrawn['items'] if x['item_id']=='n103')['status']=='withdrawn'
    try:
        checked_time(root,'2026-11-16T09:00:00')
        raise AssertionError('Naive timestamp accepted')
    except ValueError:
        pass
    print(json.dumps({'status':'PASS','scope':'corpus_and_offline_preparation_only',
        'deliveries':48,'unique_source_messages':47,'batches':16,'assets':len(m['assets']),
        'min_interval_seconds':min(deltas),'max_interval_seconds':max(deltas),
        'tested_time_boundaries':len(boundaries),'paired_stage_snapshots':2*len(boundaries),
        'speech_seconds':round(duration,3),'video_seconds':3,'agent_business_checks':'NOT_RUN'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--fixture',type=Path,default=ROOT/'fixture')
    validate(p.parse_args().fixture)
