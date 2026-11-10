#!/usr/bin/env python3
"""Harness-only single-event allowlist projection. No future context goes to model."""
import argparse, json
from pathlib import Path
MESSAGE_FIELDS = ('source', 'source_instance', 'source_message_id', 'channel',
                  'conversation_id', 'thread_id', 'occurred_ms', 'arrival_ms', 'actor_id', 'actor_verified',
                  'actor_role', 'addressed_to_agent', 'text', 'reply_to_message_id')
ATTACHMENT_FIELDS = ('asset_id', 'media_type', 'path', 'parsed')

def project_event(event):
    if event.get('kind') != 'message':
        raise ValueError('control/tool/worker/observation events require harness dispatch, not user-message projection')
    result = {k: event[k] for k in MESSAGE_FIELDS if k in event}
    result['attachments'] = [{k:a[k] for k in ATTACHMENT_FIELDS if k in a}
                             for a in event.get('attachments', [])]
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('jsonl',type=Path);p.add_argument('--event',required=True)
    args=p.parse_args()
    for line in args.jsonl.read_text(encoding='utf-8').splitlines():
        e=json.loads(line)
        if e['event_id']==args.event:
            print(json.dumps(project_event(e),ensure_ascii=False));break
    else: raise SystemExit('event not found')
