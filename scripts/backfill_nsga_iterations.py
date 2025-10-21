#!/usr/bin/env python3
"""
Backfill iterations in an uploads/nsga_ii results JSON using consolidated metrics
produced by NSGA aggregation under simulador_heuristica/output/<sim_name>/metrics.json

Usage: python scripts/backfill_nsga_iterations.py <uploads/nsga_ii/results_...json>
"""
import sys
import json
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: backfill_nsga_iterations.py <results_file>")
    sys.exit(2)

results_path = Path(sys.argv[1])
if not results_path.exists():
    print(f"File not found: {results_path}")
    sys.exit(2)

# infer sim_name from filename: results_<simname>_timestamp.json
parts = results_path.stem.split('_')
if len(parts) >= 2 and parts[0] == 'results':
    sim_name = parts[1]
else:
    print("Unable to infer simulation name from file; please provide file named results_<simname>_*.json")
    sys.exit(2)

consolidated_path = Path('simulador_heuristica') / 'output' / sim_name / 'metrics.json'
if not consolidated_path.exists():
    print(f"Consolidated metrics not found at {consolidated_path}; nothing to backfill")
    sys.exit(0)

try:
    cons = json.loads(consolidated_path.read_text())
    evs = cons.get('evaluations', [])
except Exception as e:
    print(f"Failed to read consolidated metrics: {e}")
    sys.exit(1)

try:
    raw_results = json.loads(results_path.read_text())
except Exception as e:
    print(f"Failed to read results file: {e}")
    sys.exit(1)

def _eval_distance(e):
    for k in ('distancia_total','distancia','distance','dist'):
        if k in e and e.get(k) is not None:
            try:
                return float(e.get(k))
            except Exception:
                try:
                    return float(str(e.get(k)).replace(',','.'))
                except Exception:
                    return None
    return None

changed = False
for r in raw_results:
    if r.get('iterations') is None:
        r_num = r.get('num_doors')
        r_dist = None
        try:
            if isinstance(r.get('objectives'), (list,tuple)) and len(r.get('objectives')) >= 2:
                r_dist = float(r.get('objectives')[1])
        except Exception:
            r_dist = None

        matched_iter = None
        for e in evs:
            try:
                ev_num = e.get('num_doors')
                ev_dist = _eval_distance(e)
                if ev_num is not None and r_num is not None and int(ev_num) == int(r_num):
                    if r_dist is not None and ev_dist is not None:
                        try:
                            if abs(float(ev_dist) - float(r_dist)) <= max(1e-6, 0.001 * abs(float(r_dist))):
                                matched_iter = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters') or e.get('tempo_total')
                                break
                        except Exception:
                            continue
                    else:
                        matched_iter = e.get('iterations') or e.get('qtd_iteracoes') or e.get('iters') or e.get('tempo_total')
                        break
            except Exception:
                continue

        if matched_iter is not None:
            try:
                r['iterations'] = int(matched_iter)
            except Exception:
                r['iterations'] = matched_iter
            changed = True

if changed:
    # atomic rewrite
    tmp = results_path.with_suffix('.tmp')
    tmp.write_text(json.dumps(raw_results, indent=2))
    tmp.replace(results_path)
    print(f"Backfilled iterations into {results_path}")
else:
    print("No matches found; no changes made")

print("Done")
