"""
Tests for simulador_heuristica.simulator.integration_api module.

This test suite verifies that the unified integration API correctly delegates
to simulator modules and provides consistent behavior for:
- Map parsing
- Door extraction and grouping
- Door expansion
- Map generation with grouped doors
- Individuals JSON handling
- Metrics parsing
"""

import pytest
import json
import tempfile
from pathlib import Path

# Import the integration API
from simulador_heuristica.simulator import integration_api


class TestMapParsing:
    """Test map text parsing functions."""
    
    def test_parse_simple_map(self):
        """Test parsing a simple 3x3 map."""
        map_text = "000\n020\n000"
        matrix = integration_api.parse_map_text(map_text)
        
        assert len(matrix) == 3
        assert len(matrix[0]) == 3
        assert matrix[1][1] == 2  # door in center
        assert matrix[0][0] == 0  # empty corner
    
    def test_parse_map_with_walls(self):
        """Test parsing a map with walls (1) and doors (2)."""
        map_text = "111\n121\n111"
        matrix = integration_api.parse_map_text(map_text)
        
        assert matrix[0][0] == 1  # wall
        assert matrix[1][1] == 2  # door
    
    def test_parse_map_strips_whitespace(self):
        """Test that leading/trailing whitespace is handled."""
        map_text = "  000  \n  020  \n  000  "
        matrix = integration_api.parse_map_text(map_text)
        
        # Should only parse numeric content
        assert len(matrix) == 3


class TestDoorExtraction:
    """Test door extraction and grouping functions."""
    
    def test_extract_horizontal_door(self):
        """Test extraction of a horizontal door."""
        map_text = "00000\n02220\n00000"
        doors = integration_api.extract_doors_from_map_text(map_text)
        
        assert len(doors) == 1
        door = doors[0]
        assert door['direction'] == 'H'
        assert door['row'] == 1
        assert door['col'] == 1
        assert door['size'] == 3
    
    def test_extract_vertical_door(self):
        """Test extraction of a vertical door."""
        map_text = "020\n020\n020\n000"
        doors = integration_api.extract_doors_from_map_text(map_text)
        
        assert len(doors) == 1
        door = doors[0]
        assert door['direction'] == 'V'
        assert door['row'] == 0
        assert door['col'] == 1
        assert door['size'] == 3
    
    def test_extract_multiple_doors(self):
        """Test extraction of multiple grouped doors."""
        map_text = "02220\n00000\n20002"
        doors = integration_api.extract_doors_from_map_text(map_text)
        
        # Should find 3 doors: one H door of size 3, and two single doors
        assert len(doors) == 3
        
        # First should be the horizontal group
        h_door = [d for d in doors if d.get('direction') == 'H']
        assert len(h_door) == 1
        assert h_door[0]['size'] == 3
    
    def test_extract_from_matrix(self):
        """Test extraction directly from a matrix."""
        matrix = [[0, 2, 2, 0], [0, 0, 0, 0]]
        doors = integration_api.extract_doors_from_matrix(matrix)
        
        assert len(doors) == 1
        assert doors[0]['direction'] == 'H'
        assert doors[0]['size'] == 2


class TestDoorExpansion:
    """Test door expansion from grouped format to per-cell coordinates."""
    
    def test_expand_horizontal_door(self):
        """Test expanding a horizontal door."""
        grouped = [{'row': 1, 'col': 2, 'size': 3, 'direction': 'H'}]
        expanded = integration_api.expand_grouped_doors(grouped)
        
        expected = [[2, 1], [3, 1], [4, 1]]
        assert expanded == expected
    
    def test_expand_vertical_door(self):
        """Test expanding a vertical door."""
        grouped = [{'row': 0, 'col': 1, 'size': 4, 'direction': 'V'}]
        expanded = integration_api.expand_grouped_doors(grouped)
        
        expected = [[1, 0], [1, 1], [1, 2], [1, 3]]
        assert expanded == expected
    
    def test_expand_multiple_doors(self):
        """Test expanding multiple grouped doors."""
        grouped = [
            {'row': 0, 'col': 1, 'size': 2, 'direction': 'H'},
            {'row': 2, 'col': 0, 'size': 2, 'direction': 'V'}
        ]
        expanded = integration_api.expand_grouped_doors(grouped)
        
        # Should have 4 total cells (2 + 2)
        assert len(expanded) == 4
        assert [1, 0] in expanded
        assert [2, 0] in expanded
        assert [0, 2] in expanded
        assert [0, 3] in expanded
    
    def test_expand_legacy_tuples(self):
        """Test backward compatibility with legacy tuple format."""
        legacy = [(1, 2), (3, 4)]
        expanded = integration_api.expand_grouped_doors(legacy)
        
        assert expanded == [[1, 2], [3, 4]]
    
    def test_expand_mixed_formats(self):
        """Test expansion with mixed grouped and tuple formats."""
        mixed = [
            {'row': 0, 'col': 0, 'size': 2, 'direction': 'H'},
            (5, 5)
        ]
        expanded = integration_api.expand_grouped_doors(mixed)
        
        assert len(expanded) == 3
        assert [0, 0] in expanded
        assert [1, 0] in expanded
        assert [5, 5] in expanded


class TestMapGeneration:
    """Test map generation with grouped doors."""
    
    def test_generate_map_with_horizontal_door(self):
        """Test generating a map with a horizontal door."""
        original = "00000\n00000\n00000"
        doors = [{'row': 1, 'col': 1, 'size': 3, 'direction': 'H'}]
        
        result = integration_api.generate_map_text_with_grouped_doors(original, doors)
        lines = result.split('\n')
        
        assert lines[1] == "02220"
    
    def test_generate_map_with_vertical_door(self):
        """Test generating a map with a vertical door."""
        original = "000\n000\n000\n000"
        doors = [{'row': 0, 'col': 1, 'size': 3, 'direction': 'V'}]
        
        result = integration_api.generate_map_text_with_grouped_doors(original, doors)
        lines = result.split('\n')
        
        assert lines[0][1] == '2'
        assert lines[1][1] == '2'
        assert lines[2][1] == '2'
        assert lines[3][1] == '0'
    
    def test_generate_replaces_existing_doors(self):
        """Test that existing doors are replaced."""
        original = "020\n000\n000"
        doors = [{'row': 2, 'col': 1, 'size': 1, 'direction': 'H'}]
        
        result = integration_api.generate_map_text_with_grouped_doors(original, doors)
        lines = result.split('\n')
        
        # Original door should be deactivated
        assert lines[0] == "000"
        # New door should be activated
        assert lines[2][1] == '2'


class TestIndividualsJSON:
    """Test individuals JSON save/load functions."""
    
    def test_save_and_load_dict_format(self):
        """Test saving and loading dict-based individuals format."""
        data = {
            'caracterizations': [
                {'amount': 10, 'age': 30, 'speed': 1.5},
                {'amount': 5, 'age': 50, 'speed': 1.0}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            integration_api.save_individuals_json(temp_path, data)
            loaded = integration_api.load_individuals_json(temp_path)
            
            assert 'caracterizations' in loaded
            assert len(loaded['caracterizations']) == 2
            assert loaded['caracterizations'][0]['amount'] == 10
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_save_list_format_normalizes(self):
        """Test that list format is normalized to dict format."""
        data = [
            {'amount': 10, 'age': 30},
            {'amount': 5, 'age': 50}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            integration_api.save_individuals_json(temp_path, data)
            loaded = integration_api.load_individuals_json(temp_path)
            
            # Should be wrapped in caracterizations
            assert 'caracterizations' in loaded
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_load_nonexistent_file_raises(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            integration_api.load_individuals_json('/nonexistent/path.json')


class TestMetricsParsing:
    """Test metrics parsing from output directories."""
    
    def test_parse_metrics_with_standard_keys(self):
        """Test parsing metrics with standard key names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / 'metrics.json'
            metrics_data = {
                'distance': 150.5,
                'iterations': 42,
                'num_doors': 3
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f)
            
            result = integration_api.parse_metrics_from_output_dir(tmpdir)
            
            assert result['distance'] == 150.5
            assert result['iterations'] == 42
            assert result['num_doors'] == 3
    
    def test_parse_metrics_with_legacy_keys(self):
        """Test parsing metrics with legacy/alternate key names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / 'metrics.json'
            metrics_data = {
                'distancia_total': 200.0,
                'qtd_iteracoes': 50,
                'qtd_doors': 2
            }
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f)
            
            result = integration_api.parse_metrics_from_output_dir(tmpdir)
            
            # Should normalize to standard keys
            assert result['distance'] == 200.0
            assert result['iterations'] == 50
            assert result['num_doors'] == 2
    
    def test_parse_nonexistent_directory(self):
        """Test parsing from a nonexistent directory."""
        result = integration_api.parse_metrics_from_output_dir('/nonexistent/dir')
        
        assert 'error' in result


class TestBackwardCompatibility:
    """Test backward compatibility features."""
    
    def test_legacy_door_extraction_deprecated(self):
        """Test that legacy extraction function issues deprecation warning."""
        map_text = "020\n020\n000"
        
        with pytest.warns(DeprecationWarning):
            positions = integration_api.extract_door_positions_legacy(map_text)
        
        # Should still work but return tuple format
        assert len(positions) > 0
        assert isinstance(positions[0], tuple)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_map(self):
        """Test handling of empty map."""
        map_text = ""
        matrix = integration_api.parse_map_text(map_text)
        assert matrix == []
    
    def test_map_with_no_doors(self):
        """Test extraction from map with no doors."""
        map_text = "000\n000\n000"
        doors = integration_api.extract_doors_from_map_text(map_text)
        assert doors == []
    
    def test_expand_empty_list(self):
        """Test expanding empty door list."""
        expanded = integration_api.expand_grouped_doors([])
        assert expanded == []
    
    def test_generate_map_with_no_doors(self):
        """Test generating map with no doors specified."""
        original = "020\n000"
        result = integration_api.generate_map_text_with_grouped_doors(original, [])
        
        # All doors should be deactivated
        assert '2' not in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
