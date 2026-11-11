#!/usr/bin/env python3
"""Trusted-controller-only offline replay regression. No model or network calls.

Creates temporary local projections, checks them and prints counts only.
Not an injector, business evaluator, permission sandbox or continuous scheduler.
"""
import sys, json, collections, stat, tempfile, atexit
from pathlib import Path
sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / 'business-corpus'))
from replay import verified_fixture, load, stage, source_at, SOURCES
root = PACKAGE / 'business-corpus/fixture'
_temp = tempfile.TemporaryDirectory(prefix='poc-replay-check-')
atexit.register(_temp.cleanup)
out = Path(_temp.name)
m=verified_fixture(root); events=load(root,'controller/events.json')
results={}
for arm in ('raw','parsed'):
 target=out/f'full-{arm}'; stage(root,m['end'],arm,target)
 rows=[json.loads(x) for x in (target/'inbox.jsonl').read_text().splitlines()]
 assert len(rows)==48 and len({x['event_id'] for x in rows})==47
 times=sorted({e['received_at'] for e in events}|{a[k] for e in events for a in e['attachments'] for k in ('available_at','reference_available_at') if k in a})
 after=m['epoch']; delivered=[]
 for n,until in enumerate(times):
  dest=out/f'incremental-{arm}-{n:02}'
  stage(root,until,arm,dest,after=after)
  delivered += [json.loads(x) for x in (dest/'inbox.jsonl').read_text().splitlines()]
  after=until
 types=collections.Counter(e['event_type'] for e in delivered)
 assert len(delivered)==49 and types['media_ready']==1
 assert len([e for e in delivered if e['event_type']!='media_ready'])==48
 ready=next(e for e in delivered if e['event_type']=='media_ready')
 assert ready['derived_from']=='office-a:m023:r1'
 assert 'actor' not in ready and 'text' not in ready
 results[arm]={'full_stage_events':len(rows),'incremental_events':len(delivered),'media_ready':1,'release':ready['received_at'],'unique_message_ids':len({e['event_id'] for e in delivered if e['event_type']!='media_ready'})}
 if arm=='parsed':
  broken=[a['reference_extraction'] for e in rows for a in e['attachments'] if a['name']=='agenda-damaged.pdf']
  assert len(broken)==1 and broken[0]['status']=='failed' and broken[0]['text'] is None
  results['broken_reference']='PASS: failed, text=null; not substituted with successful extraction'
ident=load(root,'controller/identity-map.json')
assert ident['office-a/owner']==ident['office-b/owner']=='synthetic-owner'
assert ident['other_actors']=='context_only_no_user_authority'
assert all(e['native_thread_id'] is None for e in events)
results['identity_metadata']='PASS: owner cross-source mapping; other actors context-only; no implicit thread classification'
# Whitelist / artifact boundary, not an OS sandbox claim.
for arm in ('raw','parsed'):
 target=out/f'full-{arm}'
 names={p.name for p in target.rglob('*')}
 assert not names & {'controller','review-only','checkpoints.json','annotations.json','manifest.json','generate.py','replay.py','validate.py'}
 results[f'{arm}_directory_mode']=oct(stat.S_IMODE(target.stat().st_mode))
results['os_enforced_agent_permissions']='NOT_RUN: no agent process or sandbox created; staging is not a security boundary'
# Query every source state with previous ETag; no contents written to summary.
summary=[]
for source in SOURCES:
 etag=None
 for state in load(root,'controller/source-timeline.json'):
  if state['source_id']!=source: continue
  r=source_at(root,source,state['available_at'],etag)
  if r['status']==503: assert 'etag' not in r and 'items' not in r
  if r['status']==304: assert 'items' not in r
  if r['status']==200: etag=r['etag']
  summary.append({'source':source,'at':state['available_at'],'status':r['status'],'item_count':len(r.get('items',[])),'withdrawn_count':sum(i.get('status')=='withdrawn' for i in r.get('items',[]))})
results['source_transitions']=summary
results['status'] = 'PASS'
results['scope'] = 'offline_projection_only'
print(json.dumps(results,indent=2,ensure_ascii=False))
