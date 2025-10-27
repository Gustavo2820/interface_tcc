#!/usr/bin/env python3
"""
Scan uploads/nsga_ii/*.json and replace any solution that has num_doors == 0 or (num_doors==0 and distance==0)
with a penalized distance and iterations, and annotate with 'penalized_zero_doors': true.
Writes files in-place but creates a .bak copy first.
"""
import json
from pathlib import Path

PENALTY_DISTANCE = 1e9
DEFAULT_MAX_ITERS = 1200

uploads = Path('uploads') / 'nsga_ii'
if not uploads.exists():
    print('No uploads/nsga_ii folder found.')
    raise SystemExit(1)

for f in sorted(uploads.glob('*.json')):
    print('Processing', f)
    data = json.loads(f.read_text())
    changed = False
    if isinstance(data, list):
        for sol in data:
            num_doors = sol.get('num_doors')
            dist = sol.get('distance') if sol.get('distance') is not None else sol.get('distancia') or sol.get('dist')
            iters = sol.get('iterations') or sol.get('iteracoes') or sol.get('qtd_iteracoes')
            if num_doors is None and isinstance(sol.get('objectives'), list) and len(sol.get('objectives')) >= 1:
                num_doors = sol['objectives'][0]
            if (num_doors == 0) or (num_doors == 0 and (dist == 0 or dist is None)):
                # apply penalty
                if iters is None:
                    sol['iterations'] = DEFAULT_MAX_ITERS
                else:
                    sol['iterations'] = int(iters)
                sol['distance'] = PENALTY_DISTANCE
                sol['distancia'] = PENALTY_DISTANCE
                sol['penalized_zero_doors'] = True
                changed = True
    if changed:
        bak = f.with_suffix(f'.json.bak')
        if not bak.exists():
            f.replace(bak)
            # write modified data to original filename
            f.write_text(json.dumps(data, indent=2))
            print('Updated', f, '-> backup at', bak)
        else:
            print('Backup already exists for', f, '; skipping overwrite.')
    else:
        print('No changes needed for', f)
print('Done.')
