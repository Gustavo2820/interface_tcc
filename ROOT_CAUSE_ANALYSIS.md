# Root Cause Analysis: Cached NSGA-II IndexError with 3-Objective Mode

## Executive Summary

The IndexError `list assignment index out of range` in `sim_ca_wall_map.py` is **NOT** caused by `use_three_objectives=True`. The error occurs because the map contains an **undocumented cell value '9'** that is not handled by the wall_map initialization logic, causing some rows to have fewer columns than expected.

## Root Cause

### The Bug
In `simulador_heuristica/unified/sim_ca_wall_map.py`, method `load_map()`:

```python
for j in range(self.len_col):
    if (self.structure_map.map[i][j] == Constants.M_WALL or 
        self.structure_map.map[i][j] == Constants.M_OBJECT):
        self.wall_direction(walls, i, j)
        wall_map_row.append(0)
    elif (self.structure_map.map[i][j] == Constants.M_EMPTY or 
          self.structure_map.map[i][j] == Constants.M_DOOR or 
          self.structure_map.map[i][j] == Constants.M_OBJECT or 
          self.structure_map.map[i][j] == Constants.M_VOID):
        wall_map_row.append(Constants.M_EMPTY)
    # ← BUG: If neither condition matches, nothing is appended!
```

### The Data
- Map file `sim_cache_adadad/map.txt` contains 303 cells with value '9'
- Value '9' is **not defined** in `Constants`: {M_EMPTY=0, M_WALL=1, M_DOOR=2, M_OBJECT=3, M_VOID=4}
- When a cell has value 9, NEITHER condition is true, so nothing is appended
- This causes `wall_map_row` to be shorter than `self.len_col` (50)
- Later, when trying to assign `self.map[row][col]`, if `col` >= actual row length, IndexError occurs

### Evidence
```
sim_ca_wall_map: self.map has 50 rows
sim_ca_wall_map: self.map[0] has 50 cols
sim_ca_wall_map: CRITICAL: col_idx=45 >= len(self.map[4])=45  ← Row 4 only has 45 cols!
sim_ca_wall_map: CRITICAL: col_idx=45 >= len(self.map[5])=41  ← Row 5 only has 41 cols!
```

## Why it Appeared with Cached NSGA-II + 3-Objective Mode

This is **coincidental**, not causal:

1. **Standard NSGA-II** (pymoo-based) might use different maps or door configurations that don't expose the bug
2. **Cached NSGA-II** uses the simulator's native map loading path
3. **3-objective mode** enables multiple scenario seeds (`[1, 2, 3, 4, 5]`), causing more simulations and earlier bug trigger
4. The specific map `sim_cache_adadad` was likely created/modified recently and contains the problematic '9' values

## The Correct Fix

### Option 1: Handle Unknown Values (Defensive)
Treat any unknown value as M_EMPTY:

```python
for j in range(self.len_col):
    if (self.structure_map.map[i][j] == Constants.M_WALL or 
        self.structure_map.map[i][j] == Constants.M_OBJECT):
        self.wall_direction(walls, i, j)
        wall_map_row.append(0)
    else:
        # Default: treat everything else as empty (defensive programming)
        wall_map_row.append(Constants.M_EMPTY)
```

### Option 2: Define Value 9 (If it's intended)
If '9' represents obstacles or special terrain:

```python
# In sim_ca_constants.py
M_OBSTACLE = 9

# In sim_ca_wall_map.py
if (self.structure_map.map[i][j] in [Constants.M_WALL, Constants.M_OBJECT, Constants.M_OBSTACLE]):
    self.wall_direction(walls, i, j)
    wall_map_row.append(0)
else:
    wall_map_row.append(Constants.M_EMPTY)
```

### Recommendation
**Option 1** (defensive) because:
- Unknown values should not crash the system
- Treats them as navigable space (conservative assumption)
- Backward compatible with existing maps
- No changes to Constants needed

## Testing Strategy

### 1. Unit Tests
```python
def test_wall_map_with_unknown_values():
    """Test that wall_map handles unknown cell values gracefully."""
    # Create a structure_map with value 9
    # Call wall_map.load_map()
    # Assert no IndexError
    # Assert map dimensions are correct
```

### 2. Integration Tests for Both Modes

**2-Objective Mode:**
```json
{
  "nsga_config": {
    "use_three_objectives": false,
    "population_size": 10,
    "generations": 5
  },
  "simulation_params": {
    "scenario_seed": [1],
    "simulation_seed": 42
  }
}
```

**3-Objective Mode:**
```json
{
  "nsga_config": {
    "use_three_objectives": true,
    "population_size": 10,
    "generations": 5
  },
  "simulation_params": {
    "scenario_seed": [1, 2, 3],
    "simulation_seed": 42
  }
}
```

### 3. Map Validation Tests
Test with maps of different sizes and door configurations:
- 5x5 (minimum)
- 25x25 (small)
- 50x50 (medium, the failing case)
- 100x100 (maximum)
- Various door counts: 1, 5, 10, 20, 30+
- Edge cases: doors on boundaries, corners

### 4. Regression Tests
- Run standard NSGA-II (pymoo) with same config → should still work
- Run cached NSGA-II with 2-obj mode → should work
- Run cached NSGA-II with 3-obj mode → should work
- Compare results quality (non-regression)

## Impact Analysis

### What Changes
- **File**: `simulador_heuristica/unified/sim_ca_wall_map.py`
- **Method**: `load_map()`
- **Lines**: ~3 lines changed

### What Doesn't Change
- `use_three_objectives` flag logic ← UNCHANGED
- NSGA-II algorithm ← UNCHANGED  
- Door placement logic ← UNCHANGED
- Simulation logic ← UNCHANGED
- Integration API ← UNCHANGED

### Backward Compatibility
✅ **Fully preserved**:
- Standard NSGA-II continues to work
- Cached NSGA-II with 2-obj continues to work
- Existing maps without '9' values continue to work
- Performance unchanged

## Validation Checklist

- [ ] Apply fix to `sim_ca_wall_map.py`
- [ ] Clear Python bytecode cache: `find . -name "*.pyc" -delete`
- [ ] Test wall_map initialization with `test_wall_map_direct.py`
- [ ] Run cached NSGA-II with 3-obj mode on `sim_cache_adadad`
- [ ] Run cached NSGA-II with 2-obj mode on same map
- [ ] Run standard NSGA-II with 3-obj mode
- [ ] Test with different map sizes (5x5, 25x25, 100x100)
- [ ] Test with various door configurations
- [ ] Verify Pareto front quality is reasonable

## Conclusion

**The bug has nothing to do with `use_three_objectives` or cached vs. standard NSGA-II.**

It's a latent defect in `wall_map.load_map()` that was exposed by:
1. A specific map containing undocumented value '9'
2. Cached NSGA-II using the native simulator map loading path
3. 3-objective mode triggering more simulations, hitting the bug earlier

**Fix**: Make `load_map()` defensive by treating unknown values as M_EMPTY.
**Impact**: Minimal, isolated to wall_map initialization.
**Compatibility**: 100% backward compatible.
