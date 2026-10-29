#!/usr/bin/env python3
"""Small local validator for canon/data state. No external dependencies."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
b = json.loads((root / 'data' / 'larpidia_world_bible.json').read_text(encoding='utf-8'))
known = {'approved', 'proposed', 'needs_decision'}
problems=[]

def traverse(node,path='root'):
    if isinstance(node,dict):
        if 'status' in node and 'value' in node and node['status'] not in known:
            problems.append(f'Unknown status at {path}: {node["status"]}')
        for k,v in node.items():traverse(v,path+'.'+str(k))
    elif isinstance(node,list):
        for i,v in enumerate(node):traverse(v,path+f'[{i}]')

traverse(b)
check=lambda expr, message: problems.append(message) if not expr else None
check(b['identity']['official_name']['value']=='Larpidie','The official name changed.')
check(any(i['name']=='Paraland' for i in b['geography']['islands']['value']),'Paraland missing.')
check(len(b['governance']['co_rulers']['value'])==4,'Expected four co-rulers.')
check(len(b['mobility']['rail_lines']['value'])==3,'Expected three rail lines.')
check(b['geography']['main_island_area_km2']['value']['min']==150,'Minimum area changed.')
religions=b['identity']['religion']['value']['proposed_distribution_percent']
check(sum(religions.values())==100,'Religion percentages do not sum to 100%.')
print('Validace kanonu:', 'OK' if not problems else 'CHYBY')
for p in problems:print(' -',p)
raise SystemExit(1 if problems else 0)
