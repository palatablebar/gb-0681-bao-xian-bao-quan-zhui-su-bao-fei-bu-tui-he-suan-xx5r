from datetime import date
from decimal import Decimal
import calendar

def cut(policy):
    base=policy['base'];start=date.fromisoformat(base['start']);end=date.fromisoformat(base['end'])
    changes=policy['changes'];points={start,end}
    for r in changes:
        d=date.fromisoformat(r['effective'])
        if start<d<end:points.add(d)
    for year in range(start.year+1,end.year+1):
        d=date(year,1,1)
        if start<d<end:points.add(d)
    result=[];points=sorted(points)
    for left,right in zip(points,points[1:]):
        active=base
        for r in changes:
            if r['effective']<=left.isoformat():active=r
        days=(right-left).days;denominator=366 if calendar.isleap(left.year) else 365
        result.append({'id':policy['id'],'source':active['id'],'line':active['_line'],'start':left.isoformat(),'end':right.isoformat(),'days':days,'annual':str(active['annual_premium']),'year_days':denominator,'exact':str(Decimal(str(active['annual_premium']))*days/denominator)})
    return result

def apply(state):
    state['segments']=[s for p in state['policies'] for s in cut(p)];return state
