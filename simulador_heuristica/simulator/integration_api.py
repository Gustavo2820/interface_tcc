"""
Integration API for simulador_heuristica.

This module provides the OFFICIAL integration API for external consumers (such as the
Streamlit interface) to interact with the simulator's core logic without duplicating code.

All functions in this module delegate directly to existing simulator modules such as
StructureMap, Scenario, and Individual. No simulation logic is duplicated here.

This is the single source of truth for:
- Map parsing and manipulation
- Door extraction and grouping
- Individuals JSON handling
- Metrics parsing

Authors:
    Integration refactor - 2025
"""

import json
import types
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import warnings

from .structure_map import StructureMap
from .sim_ca_scenario import Scenario
from .constants import Constants


def parse_map_text(map_text: str) -> List[List[int]]:
    """
    Parse a map text string into a 2D matrix of integers.
    
    This is the official way to convert map.txt content into the numeric matrix
    format used by the simulator.
    
    Args:
        map_text: Multi-line string where each character represents a cell value
        
    Returns:
        2D list of integers representing the map structure
        
    Example:
        >>> map_text = "000\\n020\\n000"
        >>> matrix = parse_map_text(map_text)
        >>> matrix
        [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
    """
    lines = map_text.strip().split('\n')
    matrix = []
    for line in lines:
        row = []
        for ch in line:
            try:
                row.append(int(ch))
            except ValueError:
                # Non-numeric character: treat '2' as door, others as wall/empty
                row.append(2 if ch == '2' else 0)
        if row:  # skip empty lines
            matrix.append(row)
    return matrix


def extract_doors_from_matrix(matrix: List[List[int]]) -> List[Dict[str, Any]]:
    """
    Extract grouped door configurations from a map matrix.
    
    This function delegates directly to the simulator's Scenario.extract_doors_info
    method, which groups adjacent door cells (value 2) into single door configurations
    with row, col, size, and direction.
    
    Args:
        matrix: 2D list of integers representing the map
        
    Returns:
        List of door dictionaries with keys: 'row', 'col', 'size', 'direction'
        where direction is 'H' (horizontal) or 'V' (vertical)
        
    Example:
        >>> matrix = [[0,2,2,2,0], [0,0,0,0,0]]
        >>> doors = extract_doors_from_matrix(matrix)
        >>> doors
        [{'row': 0, 'col': 1, 'size': 3, 'direction': 'H'}]
    """
    # Create a minimal object with the structure_map.map attribute expected by extract_doors_info
    dummy = types.SimpleNamespace()
    dummy.structure_map = types.SimpleNamespace(map=matrix)
    
    # Delegate to the simulator's door extraction logic (no duplication)
    doors_info = Scenario.extract_doors_info(dummy)
    
    return doors_info


def extract_doors_from_map_text(map_text: str) -> List[Dict[str, Any]]:
    """
    Extract grouped door configurations directly from map text.
    
    Convenience wrapper that parses the map text and extracts doors in one call.
    This is the recommended way for integration code to extract doors from a map.
    
    Args:
        map_text: Multi-line string representing the map
        
    Returns:
        List of door dictionaries with keys: 'row', 'col', 'size', 'direction'
        
    Example:
        >>> map_text = "00000\\n02220\\n00000"
        >>> doors = extract_doors_from_map_text(map_text)
        >>> doors[0]['direction']
        'H'
    """
    matrix = parse_map_text(map_text)
    return extract_doors_from_matrix(matrix)


def expand_grouped_doors(grouped_doors: List[Union[Dict, Tuple]]) -> List[List[int]]:
    """
    Expand grouped door descriptors into explicit per-cell coordinates.
    
    Converts door dictionaries (grouped format) or legacy tuples into a list of
    [col, row] coordinate pairs for each door cell.
    
    Args:
        grouped_doors: List of door descriptors (dicts with row/col/size/direction
                      or legacy (x, y) tuples)
        
    Returns:
        List of [col, row] coordinate pairs (note: col first, then row for x,y convention)
        
    Example:
        >>> doors = [{'row': 0, 'col': 1, 'size': 3, 'direction': 'H'}]
        >>> coords = expand_grouped_doors(doors)
        >>> coords
        [[1, 0], [2, 0], [3, 0]]
    """
    expanded = []
    
    for entry in grouped_doors:
        if isinstance(entry, dict):
            # Grouped door descriptor
            row = int(entry.get('row', 0))
            col = int(entry.get('col', 0))
            size = int(entry.get('size', 1))
            direction = entry.get('direction', '')
            
            if direction == 'H':
                # Horizontal door: expand along columns
                for offset in range(size if size > 0 else 1):
                    expanded.append([col + offset, row])
            elif direction == 'V':
                # Vertical door: expand along rows
                for offset in range(size if size > 0 else 1):
                    expanded.append([col, row + offset])
            else:
                # Unknown direction: treat as single cell
                expanded.append([col, row])
                
        elif isinstance(entry, (tuple, list)):
            # Legacy tuple format (x, y) or [x, y]
            if len(entry) >= 2:
                expanded.append([int(entry[0]), int(entry[1])])
                
    return expanded


def generate_map_text_with_grouped_doors(map_text: str, grouped_doors: List[Dict[str, Any]]) -> str:
    """
    Generate new map text with specified grouped doors activated.
    
    This function:
    1. Parses the input map text
    2. Deactivates all existing doors (converts '2' to '0')
    3. Activates only the specified grouped doors
    4. Returns the new map as a text string
    
    Uses the simulator's door placement logic to ensure consistency.
    
    Args:
        map_text: Original map text
        grouped_doors: List of door dictionaries to activate
        
    Returns:
        New map text string with only the specified doors active
        
    Example:
        >>> map_text = "000\\n020\\n000"
        >>> doors = [{'row': 0, 'col': 1, 'size': 2, 'direction': 'H'}]
        >>> new_map = generate_map_text_with_grouped_doors(map_text, doors)
        >>> "220" in new_map
        True
    """
    lines = map_text.split('\n')
    
    # Step 1: Deactivate all existing doors
    for i, line in enumerate(lines):
        lines[i] = line.replace('2', '0')
    
    # Step 2: Activate specified doors using simulator's logic
    # Convert grouped doors to explicit cell positions and mark them
    for door in grouped_doors:
        if not isinstance(door, dict):
            continue
            
        row = int(door.get('row', 0))
        col = int(door.get('col', 0))
        size = int(door.get('size', 1))
        direction = door.get('direction', '')
        
        if direction == 'H':
            # Horizontal door
            for offset in range(size if size > 0 else 1):
                x = col + offset
                y = row
                if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                    line_list = list(lines[y])
                    line_list[x] = '2'
                    lines[y] = ''.join(line_list)
                    
        elif direction == 'V':
            # Vertical door
            for offset in range(size if size > 0 else 1):
                x = col
                y = row + offset
                if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                    line_list = list(lines[y])
                    line_list[x] = '2'
                    lines[y] = ''.join(line_list)
        else:
            # Single cell door (fallback)
            x = col
            y = row
            if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                line_list = list(lines[y])
                line_list[x] = '2'
                lines[y] = ''.join(line_list)
    
    return '\n'.join(lines)


def save_individuals_json(path: Union[str, Path], data: Union[Dict, List]) -> None:
    """
    Save individuals data to a JSON file in the canonical simulator format.
    
    Accepts both list-based format (array of individual dicts) and dict-based format
    (with 'caracterizations' key). Normalizes and writes in the format expected by
    the simulator.
    
    Args:
        path: File path where the JSON should be written
        data: Individuals data (dict with 'caracterizations' or list of individuals)
        
    Example:
        >>> data = {'caracterizations': [{'amount': 10, 'age': 30}]}
        >>> save_individuals_json('/tmp/individuals.json', data)
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Normalize data format
    if isinstance(data, list):
        # List format: wrap in caracterizations if needed
        output = {'caracterizations': data} if data and 'amount' not in data[0] else data
    elif isinstance(data, dict):
        # Dict format: use as-is if it has caracterizations, else wrap
        if 'caracterizations' not in data:
            output = {'caracterizations': [data]}
        else:
            output = data
    else:
        raise ValueError(f"Invalid individuals data type: {type(data)}")
    
    # Atomic write
    tmp_path = path.with_suffix('.tmp')
    try:
        with open(tmp_path, 'w') as f:
            json.dump(output, f, indent=2)
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def load_individuals_json(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load individuals data from a JSON file.
    
    Supports both formats:
    - List-based: array of individual dicts
    - Dict-based: {'caracterizations': [...]}
    
    Returns a normalized dict with 'caracterizations' key for consistency.
    
    Args:
        path: File path to read from
        
    Returns:
        Dict with 'caracterizations' key containing list of individuals
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Individuals file not found: {path}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Normalize to dict format with caracterizations
    if isinstance(data, list):
        return {'caracterizations': data}
    elif isinstance(data, dict):
        if 'caracterizations' not in data:
            return {'caracterizations': [data]}
        return data
    else:
        raise ValueError(f"Invalid individuals JSON structure in {path}")


def parse_metrics_from_output_dir(output_dir: Union[str, Path]) -> Dict[str, Any]:
    """
    Parse metrics from a simulator output directory.
    
    Searches for metrics.json and other result files in the output directory and
    extracts key metrics with normalized field names.
    
    Normalizes various metric key variations:
    - 'distancia_total', 'distance', 'qtdDistance' -> 'distance'
    - 'iterations', 'tempo_total', 'qtd_iteracoes' -> 'iterations'
    - 'num_doors', 'qtd_doors' -> 'num_doors'
    
    Args:
        output_dir: Path to the simulator output directory
        
    Returns:
        Dict with normalized metrics, or empty dict if no metrics found
        
    Example:
        >>> metrics = parse_metrics_from_output_dir('simulador_heuristica/output/exp_001')
        >>> 'distance' in metrics
        True
    """
    output_dir = Path(output_dir)
    
    if not output_dir.exists():
        return {'error': f'Output directory not found: {output_dir}'}
    
    metrics = {}
    
    # Search for metrics files
    metrics_files = list(output_dir.glob('metrics*.json')) + list(output_dir.glob('**/metrics*.json'))
    
    for metrics_file in metrics_files:
        try:
            with open(metrics_file, 'r') as f:
                data = json.load(f)
            
            # Extract and normalize distance
            distance_keys = ['distance', 'avg_distance', 'qtdDistance', 'qtd_distancia', 
                           'qtd_distance', 'distancia', 'total_distance', 'distancia_total']
            for key in distance_keys:
                if key in data and data[key] is not None:
                    try:
                        metrics['distance'] = float(data[key])
                        break
                    except (ValueError, TypeError):
                        pass
            
            # Extract and normalize iterations
            iterations_keys = ['iterations', 'tempo_total', 'total_time', 'qtd_iteracoes', 'iters']
            for key in iterations_keys:
                if key in data and data[key] is not None:
                    try:
                        metrics['iterations'] = int(data[key])
                        break
                    except (ValueError, TypeError):
                        pass
            
            # Extract and normalize num_doors
            doors_keys = ['num_doors', 'qtd_doors', 'doors_count']
            for key in doors_keys:
                if key in data and data[key] is not None:
                    try:
                        metrics['num_doors'] = int(data[key])
                        break
                    except (ValueError, TypeError):
                        pass
            
            # If we found metrics, we can stop searching
            if metrics:
                break
                
        except (json.JSONDecodeError, IOError) as e:
            # Skip files that can't be parsed
            continue
    
    # Add metadata
    if metrics:
        metrics['source_dir'] = str(output_dir)
    
    return metrics


def create_structure_map_from_text(map_text: str, label: str = "temp") -> StructureMap:
    """
    Create a StructureMap instance from map text.
    
    This is a helper for integration code that needs a StructureMap object
    without writing to disk first.
    
    Args:
        map_text: Map text content
        label: Label for the map (default: "temp")
        
    Returns:
        Initialized StructureMap instance
        
    Note:
        This creates a temporary file to satisfy StructureMap's file-based API.
        For production use, prefer writing the map file and using standard loading.
    """
    import tempfile
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(map_text)
        temp_path = f.name
    
    try:
        # Create and load the structure map
        structure_map = StructureMap(label, temp_path)
        structure_map.load_map()
        return structure_map
    finally:
        # Clean up the temporary file
        Path(temp_path).unlink(missing_ok=True)


# Backward compatibility helpers

def extract_door_positions_legacy(map_text: str) -> List[Tuple[int, int]]:
    """
    DEPRECATED: Extract door positions as (x, y) tuples (legacy format).
    
    This function is provided for backward compatibility only.
    New code should use extract_doors_from_map_text() which returns grouped doors.
    
    Args:
        map_text: Map text content
        
    Returns:
        List of (x, y) tuples for each door cell
        
    .. deprecated:: 2025
        Use :func:`extract_doors_from_map_text` and :func:`expand_grouped_doors` instead.
    """
    warnings.warn(
        "extract_door_positions_legacy is deprecated. "
        "Use extract_doors_from_map_text() and expand_grouped_doors() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Extract grouped doors and expand to per-cell coordinates
    grouped = extract_doors_from_map_text(map_text)
    expanded = expand_grouped_doors(grouped)
    
    # Convert [col, row] to (col, row) tuples for legacy compatibility
    return [(coord[0], coord[1]) for coord in expanded]
