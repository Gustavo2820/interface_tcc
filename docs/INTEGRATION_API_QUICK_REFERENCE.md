# Integration API Quick Reference

## Import

```python
from simulador_heuristica.simulator import integration_api
```

---

## Map Operations

### Parse Map Text
```python
matrix = integration_api.parse_map_text(map_text)
# Returns: List[List[int]]
```

### Extract Doors (Grouped)
```python
doors = integration_api.extract_doors_from_map_text(map_text)
# Returns: [{'row': int, 'col': int, 'size': int, 'direction': 'H'|'V'}, ...]
```

### Expand Doors to Coordinates
```python
coords = integration_api.expand_grouped_doors(grouped_doors)
# Returns: [[col, row], [col, row], ...]
```

### Generate Map with Doors
```python
new_map = integration_api.generate_map_text_with_grouped_doors(
    original_map_text, 
    grouped_doors_list
)
# Returns: str (new map text)
```

---

## Individuals Operations

### Save Individuals
```python
integration_api.save_individuals_json(path, data)
# Accepts: dict or list
# Normalizes to canonical format
```

### Load Individuals
```python
data = integration_api.load_individuals_json(path)
# Returns: {'caracterizations': [...]}
```

---

## Metrics Operations

### Parse Metrics from Output
```python
metrics = integration_api.parse_metrics_from_output_dir(output_dir)
# Returns: {'distance': float, 'iterations': int, 'num_doors': int, ...}
```

---

## Utility Functions

### Create StructureMap from Text
```python
structure_map = integration_api.create_structure_map_from_text(map_text, label)
# Returns: StructureMap instance
```

---

## Example Usage

### Complete NSGA Door Flow

```python
from simulador_heuristica.simulator import integration_api

# 1. Load map
with open('map.txt', 'r') as f:
    map_text = f.read()

# 2. Extract existing doors
doors = integration_api.extract_doors_from_map_text(map_text)
print(f"Found {len(doors)} door configurations")

# 3. Modify doors (e.g., NSGA selection)
selected_doors = doors[:2]  # Select first 2 doors

# 4. Generate new map
new_map = integration_api.generate_map_text_with_grouped_doors(
    map_text, 
    selected_doors
)

# 5. Get per-cell coordinates for display
coords = integration_api.expand_grouped_doors(selected_doors)

# 6. Save for simulation
with open('output_map.txt', 'w') as f:
    f.write(new_map)
```

### Parse Simulation Results

```python
from simulador_heuristica.simulator import integration_api

# Parse metrics after simulation
metrics = integration_api.parse_metrics_from_output_dir(
    'simulador_heuristica/output/experiment_001'
)

if 'error' not in metrics:
    print(f"Distance: {metrics['distance']}")
    print(f"Iterations: {metrics['iterations']}")
    print(f"Doors: {metrics['num_doors']}")
```

### Handle Individuals Data

```python
from simulador_heuristica.simulator import integration_api

# Create individuals data
individuals_data = {
    'caracterizations': [
        {'amount': 100, 'age': 30, 'speed': 1.5},
        {'amount': 50, 'age': 50, 'speed': 1.2}
    ]
}

# Save
integration_api.save_individuals_json('individuals.json', individuals_data)

# Load (normalizes format automatically)
loaded = integration_api.load_individuals_json('individuals.json')
```

---

## Migration from Old Code

### Before (Duplicated Logic)
```python
# OLD: Manual door extraction
doors = []
lines = map_text.split('\n')
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '2':
            doors.append((x, y))
```

### After (Using API)
```python
# NEW: Use integration API
doors = integration_api.extract_doors_from_map_text(map_text)
coords = integration_api.expand_grouped_doors(doors)
```

### Before (Duplicated StructureMap)
```python
# OLD: Import duplicated class
from interface.services.simulator_integration import StructureMap
```

### After (Using Official Class)
```python
# NEW: Import from simulator
from simulador_heuristica.simulator.structure_map import StructureMap
```

---

## Error Handling

```python
from simulador_heuristica.simulator import integration_api

try:
    doors = integration_api.extract_doors_from_map_text(map_text)
except Exception as e:
    print(f"Error extracting doors: {e}")
    doors = []

try:
    data = integration_api.load_individuals_json(path)
except FileNotFoundError:
    print("Individuals file not found")
except json.JSONDecodeError:
    print("Invalid JSON format")
```

---

## Key Benefits

✅ **Single Source of Truth** - All logic in one place  
✅ **No Duplication** - Delegates to simulator modules  
✅ **Backward Compatible** - Handles both new and old formats  
✅ **Well Tested** - 26+ tests covering all functions  
✅ **Clear API** - Simple, documented functions  
✅ **Type Hints** - Full type annotations for IDE support

---

## See Also

- [Integration Refactor Summary](./INTEGRATION_REFACTOR_SUMMARY.md) - Full refactoring details
- [API Reference](../simulador_heuristica/simulator/integration_api.py) - Source code with docstrings
- [Tests](../tests/test_integration_api.py) - Usage examples in tests
