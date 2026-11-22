from decimal import Decimal,ROUND_DOWN,ROUND_HALF_UP

def allocate(values):
    values=[Decimal(str(v)) for v in values]
    total=sum(values,Decimal(0)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    floors=[v.quantize(Decimal('.01'),rounding=ROUND_DOWN) for v in values]
    residual=int((total-sum(floors))/Decimal('.01'))
    ranks=sorted(range(len(values)),key=lambda i:(-(values[i]-floors[i]),i))
    for i in ranks[:residual]:floors[i]+=Decimal('.01')
    return floors

def apply(state):
    calculations=[];total=Decimal(0);paidtotal=Decimal(0)
    for p in state['policies']:
        segments=[s for s in state['segments'] if s['id']==p['id']]
        allocated=allocate([s['exact'] for s in segments]);expected=sum(allocated,Decimal(0))
        paid=sum((Decimal(str(r['paid'])) for r in state['rows'] if r['policy_id']==p['id']),Decimal(0))
        for s,value in zip(segments,allocated):s['premium']=str(value)
        calculations.append({'id':p['id'],'line':p['base']['_line'],'code':'SUPPLEMENT' if expected>paid else 'REFUND' if expected<paid else 'EVEN','expected':str(expected),'paid':str(paid),'difference':str(expected-paid),'segments':segments})
        total+=expected;paidtotal+=paid
    state['calculations']=calculations;state['business']={'total':str(total),'paid':str(paidtotal),'difference':str(total-paidtotal),'unit':'CNY'};return state
