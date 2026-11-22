from decimal import Decimal
from app.workflow import run
from app.modules.m5_calculate.rules import allocate

def test_real_cancelled_amount(raw):
    r=run(raw,{})['calculations'][0];assert r['expected']=='3650.00' and r['difference']=='0.00'
def test_real_increase_then_decrease(raw):
    r=run(raw,{})['calculations'][1];assert r['expected']=='5030.00' and r['difference']=='1380.00'
def test_actual_sum(raw):
    s=run(raw,{});assert sum(Decimal(r['expected']) for r in s['calculations'])==Decimal(s['business']['total'])
def test_largest_remainder_conserves():
    # TRAP-24
    assert allocate(['.3333']*3)==[Decimal('.34'),Decimal('.33'),Decimal('.33')]
def test_naive_rounding_counterexample():
    assert sum(allocate(['.3333']*3))==Decimal('1.00') and sum(Decimal('.3333').quantize(Decimal('.01')) for _ in range(3))==Decimal('.99')
def test_zero_amount_allocation():assert allocate(['0','0'])==[Decimal('0.00'),Decimal('0.00')]
def test_segments_total_matches_policy(raw):
    s=run(raw,{});assert all(sum(Decimal(x['premium']) for x in r['segments'])==Decimal(r['expected']) for r in s['calculations'])
