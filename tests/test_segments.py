from decimal import Decimal
from app.workflow import run
from app.modules.m4_segments.rules import cut

def test_real_cancelled_whole_year(raw):
    seg=run(raw,{},4)['segments'][0];assert seg['days']==365 and Decimal(seg['exact'])==3650
def test_real_change_split(raw):
    seg=[r for r in run(raw,{},4)['segments'] if r['id']=='P002'];assert [r['days'] for r in seg]==[181,92,92]
def test_halfopen_conservation(raw):
    # TRAP-23
    s=run(raw,{},4);assert all(sum(r['days'] for r in s['segments'] if r['id']==p['id'])==365 for p in s['policies'])
def test_effective_not_input_order(raw):
    s=run(raw,{},3);p=s['policies'][1];p['changes'].reverse();p['changes'].sort(key=lambda x:(x['effective'],x['version']));assert cut(p)[1]['annual']=='7300'
def test_leap_year_denominator():
    p={'id':'L','base':{'start':'2024-01-01','end':'2025-01-01','annual_premium':'3660','id':'1','_line':2},'changes':[]};s=cut(p);assert s[0]['year_days']==366 and Decimal(s[0]['exact'])==3660
def test_cross_year_cut():
    p={'id':'L','base':{'start':'2023-12-31','end':'2024-01-02','annual_premium':'3650','id':'1','_line':2},'changes':[]};assert [s['year_days'] for s in cut(p)]==[365,366]
def test_no_zero_segments(raw):assert all(r['days']>0 for r in run(raw,{},4)['segments'])
