from copy import deepcopy
import pytest
from app.workflow import run
from app.modules.m3_versions.rules import apply
from app.errors import DomainError

def test_real_policy_count(raw):assert len(run(raw,{},3)['policies'])==12
def test_real_cancel_reference(raw):
    p=run(raw,{},3)['policies'][0];assert p['cancelled']==['00002'] and p['changes']==[]
def test_real_change_order(raw):
    p=run(raw,{},3)['policies'][1];assert [r['effective'] for r in p['changes']]==['2026-07-01','2026-10-01']
def test_order_independent(raw):
    s=run(raw,{},2);a=apply(deepcopy(s));s['rows'].reverse();b=apply(s)
    assert {p['id']:[x['id'] for x in p['changes']] for p in a['policies']}=={p['id']:[x['id'] for x in p['changes']] for p in b['policies']}
def test_bad_cancel_isolated(raw):
    s=run(raw,{},2);s['rows'][2]['ref']='absent';r=apply(s);assert any(x['code']=='REFERENCE' for x in r['quarantine'])
def test_missing_issue_isolated(raw):
    s=run(raw,{},2);s['rows']=[r for r in s['rows'] if r['kind']!='issue'];r=apply(s);assert r['policies']==[]
def test_effective_outside_rejected(raw):
    s=run(raw,{},2);s['rows'][1]['effective']='2027-01-01';r=apply(s);assert any(q['code']=='RANGE' for q in r['quarantine'])
