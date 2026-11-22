TITLE='保险保全追溯与保费补退核算'
SHORT='endorsement'
RULE_VERSION='2026.11.17-v1'
MODULES=[('m1_ingest', '保单采信'), ('m2_mapping', '责任映射'), ('m3_versions', '保全选版'), ('m4_segments', '承保切片'), ('m5_calculate', '保费重算'), ('m6_reconcile', '补退对账'), ('m7_archive', '结案归档')]
REQUIRED=['id', 'policy_id', 'version', 'kind', 'effective', 'start', 'end', 'annual_premium', 'paid', 'cover']
NUMERIC=['version', 'annual_premium', 'paid']
DATES=['effective', 'start', 'end']
TIMES=[]
