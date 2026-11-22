from collections import defaultdict
from decimal import Decimal
from app.errors import DomainError

def apply(state):
    groups=defaultdict(list);bad=[]
    for r in state['rows']:
        if r['kind'] not in ('issue','change','cancel') or r['start']>=r['end'] or not r['start']<=r['effective']<r['end'] or Decimal(str(r['annual_premium']))<0 or Decimal(str(r['paid']))<0:
            bad.append((r,'RANGE'));continue
        groups[r['policy_id']].append(r)
    policies=[]
    for pid,events in groups.items():
        issues=[r for r in events if r['kind']=='issue']
        if len(issues)!=1:
            bad.extend((r,'REFERENCE') for r in events);continue
        base=issues[0];targets={r['id']:r for r in events if r['kind']=='change'};cancelled=set()
        for r in events:
            if r['kind']=='cancel':
                target=targets.get(r['ref'])
                if target is None or r['effective']<target['effective']:bad.append((r,'REFERENCE'))
                else:cancelled.add(r['ref'])
        chosen={}
        for r in events:
            if r['kind']!='change' or r['id'] in cancelled:continue
            key=(r['effective'],r['cover'])
            if key in chosen and r['version']==chosen[key]['version'] and r['annual_premium']!=chosen[key]['annual_premium']:
                raise DomainError('VERSION','同一生效日存在矛盾批单')
            if key not in chosen or Decimal(str(r['version']))>Decimal(str(chosen[key]['version'])):chosen[key]=r
        policies.append({'id':pid,'base':base,'changes':sorted(chosen.values(),key=lambda x:(x['effective'],x['version'])),'cancelled':sorted(cancelled)})
    bad_lines={r['_line'] for r,_ in bad}
    for r,code in bad:state['quarantine'].append({'line':r['_line'],'id':r['id'],'code':code,'raw':r['_raw']})
    state['rows']=[r for r in state['rows'] if r['_line'] not in bad_lines]
    state['policies']=policies;return state
