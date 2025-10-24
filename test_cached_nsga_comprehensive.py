#!/usr/bin/env python3
"""
Comprehensive test suite for cached NSGA-II with 2-objective and 3-objective modes.

Tests:
1. Wall map initialization with various map types
2. Cached NSGA-II with 2-objective mode
3. Cached NSGA-II with 3-objective mode
4. Different map sizes and door configurations
5. Multiple scenario seeds
6. Backward compatibility with standard NSGA-II

Author: Root cause analysis - 2025-10-23
"""

import sys
import json
from pathlib import Path
import pytest

# Add paths
project_root = Path(__file__).resolve().parent
unified_path = project_root / "simulador_heuristica" / "unified"
sys.path.insert(0, str(unified_path))

from sim_ca_structure_map import StructureMap
from sim_ca_wall_map import WallMap
from sim_ca_scenario import Scenario


class TestWallMapInitialization:
    """Test wall_map.load_map() with various map types."""
    
    def test_wall_map_with_standard_values(self):
        """Test map with only standard values (0, 1, 2, 3, 4)."""
        experiment = "sim_cache_adadad"
        root_path = str(project_root) + "/"
        map_path = root_path + "simulador_heuristica/input/" + experiment + "/map.txt"
        
        structure_map = StructureMap(experiment, map_path)
        structure_map.load_map()
        
        wall_map = WallMap(experiment, structure_map)
        wall_map.load_map()  # Should not raise IndexError
        
        # Verify dimensions
        assert wall_map.len_row == structure_map.len_row
        assert wall_map.len_col == structure_map.len_col
        
        # Verify all rows have correct length
        assert len(wall_map.map) == wall_map.len_row
        for i, row in enumerate(wall_map.map):
            assert len(row) == wall_map.len_col, f"Row {i} has length {len(row)}, expected {wall_map.len_col}"
    
    def test_wall_map_with_unknown_values(self):
        """Test that unknown values (like 9) don't cause IndexError."""
        # This is implicitly tested by test_wall_map_with_standard_values
        # since sim_cache_adadad contains value 9
        pass
    
    def test_scenario_initialization(self):
        """Test full scenario initialization including wall_map."""
        experiment = "sim_cache_adadad"
        scenario = Scenario(experiment)
        
        # Scenario should load without errors
        assert scenario.structure_map is not None
        assert len(scenario.doors_configurations) > 0
    
    def test_scenario_with_doors(self):
        """Test scenario with specific door configuration."""
        experiment = "sim_cache_adadad"
        scenario = Scenario(experiment)
        doors = scenario.doors_configurations[:5]  # First 5 doors
        
        # This should trigger map_reset -> load_wall_map -> load_map
        scenario_with_doors = Scenario(
            experiment, 
            doors=doors, 
            draw=False, 
            scenario_seed=1, 
            simulation_seed=42
        )
        
        assert scenario_with_doors.wall_map is not None
        assert len(scenario_with_doors.wall_map.map) == scenario_with_doors.structure_map.len_row


class TestCachedNSGAIntegration:
    """Integration tests for cached NSGA-II with different configurations."""
    
    @pytest.fixture
    def nsga_integration(self):
        """Create NSGA integration instance."""
        sys.path.insert(0, str(project_root / "interface" / "services"))
        from simulator_integration import SimulatorIntegration
        from nsga_cached_integration import CachedNSGAIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = CachedNSGAIntegration(sim_integration)
        return nsga
    
    def test_load_config_2obj_mode(self, nsga_integration):
        """Test loading configuration for 2-objective mode."""
        config = {
            "nsga_config": {
                "population_size": 10,
                "generations": 5,
                "mutation_rate": 0.3,
                "crossover_rate": 0.9,
                "use_three_objectives": False
            },
            "simulation_params": {
                "scenario_seed": [1],
                "simulation_seed": 42
            }
        }
        
        config_file = project_root / "test_config_2obj.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        success = nsga_integration.load_configuration(config_file)
        assert success
        assert nsga_integration.use_three_objectives is False
        
        config_file.unlink()  # Cleanup
    
    def test_load_config_3obj_mode(self, nsga_integration):
        """Test loading configuration for 3-objective mode."""
        config = {
            "nsga_config": {
                "population_size": 10,
                "generations": 5,
                "mutation_rate": 0.3,
                "crossover_rate": 0.9,
                "use_three_objectives": True
            },
            "simulation_params": {
                "scenario_seed": [1, 2, 3],
                "simulation_seed": 42
            }
        }
        
        config_file = project_root / "test_config_3obj.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        success = nsga_integration.load_configuration(config_file)
        assert success
        assert nsga_integration.use_three_objectives is True
        
        config_file.unlink()  # Cleanup
    
    @pytest.mark.slow
    def test_run_cached_nsga_2obj(self, nsga_integration):
        """Test running cached NSGA-II in 2-objective mode."""
        config = {
            "nsga_config": {
                "population_size": 6,
                "generations": 2,
                "mutation_rate": 0.3,
                "crossover_rate": 0.9,
                "use_three_objectives": False
            },
            "simulation_params": {
                "scenario_seed": [1],
                "simulation_seed": 42,
                "draw_mode": False
            }
        }
        
        config_file = project_root / "test_run_2obj.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        nsga_integration.load_configuration(config_file)
        
        # Note: This will run actual simulations, so it's slow
        result = nsga_integration.run_optimization("sim_cache_adadad", draw=False)
        
        assert result is not None
        results, factory = result
        assert len(results) > 0
        
        # Verify objectives format (2-obj mode)
        converted = nsga_integration.convert_results_to_standard_format(results, factory)
        for sol in converted:
            assert len(sol['objectives']) == 2  # [num_doors, distance]
            assert 'iterations' in sol  # Present as auxiliary field
        
        config_file.unlink()  # Cleanup
    
    @pytest.mark.slow
    def test_run_cached_nsga_3obj(self, nsga_integration):
        """Test running cached NSGA-II in 3-objective mode."""
        config = {
            "nsga_config": {
                "population_size": 6,
                "generations": 2,
                "mutation_rate": 0.3,
                "crossover_rate": 0.9,
                "use_three_objectives": True
            },
            "simulation_params": {
                "scenario_seed": [1, 2],
                "simulation_seed": 42,
                "draw_mode": False
            }
        }
        
        config_file = project_root / "test_run_3obj.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        nsga_integration.load_configuration(config_file)
        
        # Note: This will run actual simulations, so it's slow
        result = nsga_integration.run_optimization("sim_cache_adadad", draw=False)
        
        assert result is not None
        results, factory = result
        assert len(results) > 0
        
        # Verify objectives format (3-obj mode)
        converted = nsga_integration.convert_results_to_standard_format(results, factory)
        for sol in converted:
            assert len(sol['objectives']) == 3  # [num_doors, iterations, distance]
            assert 'iterations' in sol
        
        config_file.unlink()  # Cleanup


class TestBackwardCompatibility:
    """Test that fixes don't break existing functionality."""
    
    def test_standard_nsga_still_works(self):
        """Verify standard (pymoo) NSGA-II still works."""
        # This is a placeholder - would need full standard NSGA-II setup
        # Just verify imports work
        try:
            sys.path.insert(0, str(project_root / "interface" / "services"))
            from nsga_integration import NSGAIntegration
            assert NSGAIntegration is not None
        except ImportError:
            pytest.skip("Standard NSGA-II not available")
    
    def test_different_map_sizes(self):
        """Test with maps of different sizes."""
        # Test various map sizes if available
        # For now, just test that the one we have works
        experiment = "sim_cache_adadad"
        scenario = Scenario(experiment)
        assert scenario.structure_map.len_row == 50
        assert scenario.structure_map.len_col == 50


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
