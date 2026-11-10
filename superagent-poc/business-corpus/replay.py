#!/usr/bin/env python3
"""Offline point-in-time material preparation, NOT an agent runner or scheduler.

Only the trusted controller runs this file. The tested agent gets the output
directory, never this file, fixture/controller, oracle, or arbitrary --at access.
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT = ROOT / 'fixture'
SOURCES = ('llm-news', 'deepseek-plugin', 'delivery')
VISIBLE = ('source','source_instance','source_message_id','revision','event_type',
           'conversation_id','native_thread_id','actor','occurred_at','received_at',
           'reply_to','addressed','text')


def parse_time(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('Timezone required; use RFC3339 with Z or an explicit offset.')
    return parsed


def load(root, path):
    return json.loads((root/path).read_text(encoding='utf-8'))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def verified_fixture(root):
    manifest=load(root,'manifest.json')
    for f in manifest['files']:
        p=(root/f['path']).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file():
            raise ValueError('Invalid fixture path')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:
            raise ValueError(f'Fixture hash mismatch: {f["path"]}')
    return manifest


def checked_time(root, value):
    now=parse_time(value)
    m=load(root,'manifest.json')
    if not parse_time(m['epoch']) <= now <= parse_time(m['end']):
        raise ValueError('Time outside frozen fixture window')
    return now


def source_at(root, source, at, if_none_match=None):
    now=checked_time(root,at)
    if source not in SOURCES:
        raise ValueError('Unknown fixture source')
    states=[s for s in load(root,'controller/source-timeline.json')
            if s['source_id']==source and parse_time(s['available_at'])<=now]
    if not states:
        return {'source_id':source,'checked_at':at,'status':404,'reason':'not_available'}
    current=max(states,key=lambda x:parse_time(x['available_at']))
    if current['status']=='error':
        return {'source_id':source,'checked_at':at,'status':current['error']['code'],
                'error':current['error']['message'],'freshness':'unknown'}
    body=json.dumps(current['items'],ensure_ascii=False,sort_keys=True).encode('utf-8')
    etag=hashlib.sha256(body).hexdigest()
    result={'source_id':source,'checked_at':at,'status':304 if etag==if_none_match else 200,
            'etag':etag,'snapshot_available_at':current['available_at']}
    if result['status']==200:
        result['items']=current['items']
    return result


def stage(root, until, arm, out, after=None):
    verified_fixture(root)
    now=checked_time(root,until)
    start=checked_time(root,after) if after else None
    if start and start>now:
        raise ValueError('--after must not be later than --until')
    if arm not in ('raw','parsed'):
        raise ValueError('Unknown arm')
    if out.exists():
        raise ValueError('Output must not exist; preserve previous evidence')
    if out.resolve().is_relative_to(root.resolve()):
        raise ValueError('Never stage inside the full fixture')
    out.mkdir(parents=True)
    events=load(root,'controller/events.json')
    refs=load(root,'controller/parsed-reference.json')
    inbox=[]

    def attachment_at(a, parent):
        attachment={k:a[k] for k in ('name','mime','size','sha256')}
        available=a.get('reference_available_at' if arm=='parsed' else 'available_at',parent['received_at'])
        if parse_time(available)>now:
            attachment['availability']='pending'
            # Availability times are controller forecasts, not model-visible facts.
            return attachment
        if arm=='raw':
            origin=(root/a['ref']).resolve()
            if not origin.is_relative_to((root/'assets').resolve()):
                raise ValueError('Attachment outside assets')
            target=Path('attachments')/a['sha256'][:16]/a['name']
            (out/target).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(origin,out/target)
            attachment.update(availability='ready',ref=str(target))
        else:
            attachment.update(availability='reference_text_only',reference_extraction=refs[a['name']])
        return attachment

    for e in events:
        arrival=parse_time(e['received_at'])
        if arrival>now:
            continue
        # Incremental stages release a genuine fixture readiness event, not a human message.
        if start and arrival<=start:
            for a in e['attachments']:
                available=a.get('reference_available_at' if arm=='parsed' else 'available_at',e['received_at'])
                if start<parse_time(available)<=now:
                    inbox.append({'event_id':f'{e["source_instance"]}:{e["source_message_id"]}:asset:{a["sha256"][:16]}:{arm}',
                        'event_type':'media_ready','source':'fixture_attachment_store',
                        'derived_from':f'{e["source_instance"]}:{e["source_message_id"]}:r{e["revision"]}',
                        'conversation_id':e['conversation_id'],'occurred_at':available,'received_at':available,
                        'attachments':[attachment_at(a,e)]})
            continue
        p={key:e[key] for key in VISIBLE}
        p['event_id']=f'{e["source_instance"]}:{e["source_message_id"]}:r{e["revision"]}'
        p['attachments']=[attachment_at(a,e) for a in e['attachments']]
        inbox.append(p)
    inbox.sort(key=lambda x:parse_time(x['received_at']))
    (out/'inbox.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in inbox),encoding='utf-8')
    dump(out/'clock.json',{'business_now':until,'timezone':'Asia/Shanghai'})
    dump(out/'identity-map.json',load(root,'controller/identity-map.json'))
    for source in SOURCES:
        dump(out/f'sources/{source}.json',source_at(root,source,until))
    return {'prepared_events':len(inbox),'business_now':until,'arm':arm,
            'mode':'point_in_time_material_only','agent_or_watch_executed':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixture',type=Path,default=DEFAULT)
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('stage')
    s.add_argument('--until',required=True)
    s.add_argument('--after')
    s.add_argument('--arm',choices=('raw','parsed'),required=True)
    s.add_argument('--out',type=Path,required=True)
    q=sub.add_parser('source')
    q.add_argument('--at',required=True)
    q.add_argument('--source',choices=SOURCES,required=True)
    q.add_argument('--if-none-match')
    a=p.parse_args()
    try:
        if a.command=='stage':
            result=stage(a.fixture,a.until,a.arm,a.out,a.after)
        else:
            verified_fixture(a.fixture)
            result=source_at(a.fixture,a.source,a.at,a.if_none_match)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError, OSError, KeyError) as error:
        p.exit(2,f'{error}\n')


if __name__=='__main__':
    main()
