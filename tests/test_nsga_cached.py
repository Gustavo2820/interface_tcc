"""
Tests for cached NSGA-II integration.

This test suite verifies that the cached NSGA-II implementation from
simulador_heuristica/unified can be properly integrated with the interface
while maintaining compatibility with the standard pymoo workflow.
"""

import pytest
import json
import tempfile
from pathlib import Path

# Try to import the cached NSGA integration
try:
    from interface.services.nsga_cached_integration import (
        CachedNSGAIntegration,
        get_cached_nsga_integration,
        CACHED_NSGA_AVAILABLE
    )
    from interface.services.simulator_integration import SimulatorIntegration
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Cached NSGA imports not available: {e}")
    IMPORTS_AVAILABLE = False
    pytest.skip("Cached NSGA-II not available", allow_module_level=True)


class TestCachedNSGAIntegration:
    """Test cached NSGA-II integration adapter."""
    
    def test_imports_available(self):
        """Verify cached NSGA-II can be imported."""
        assert IMPORTS_AVAILABLE, "Cached NSGA-II imports should be available"
    
    def test_create_integration(self):
        """Test creating CachedNSGAIntegration instance."""
        sim_integration = SimulatorIntegration()
        cached_nsga = CachedNSGAIntegration(sim_integration)
        
        assert cached_nsga is not None
        assert cached_nsga.simulator_integration == sim_integration
        assert cached_nsga.config is None  # Not loaded yet
    
    def test_load_unified_config(self):
        """Test loading unified configuration format."""
        sim_integration = SimulatorIntegration()
        cached_nsga = CachedNSGAIntegration(sim_integration)
        
        # Create temp config
        config_data = {
            'nsga_config': {
                'population_size': 20,
                'generations': 50,
                'mutation_rate': 0.3
            },
            'simulation_params': {
                'scenario_seed': [1, 2, 3],
                'simulation_seed': 42
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            result = cached_nsga.load_configuration(Path(temp_path))
            
            assert result is True
            assert cached_nsga.config is not None
            assert cached_nsga.config['population_size'] == 20
            assert cached_nsga.config['generations'] == 50
            assert cached_nsga.simulation_params['scenario_seed'] == [1, 2, 3]
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_load_legacy_config(self):
        """Test loading legacy configuration format."""
        sim_integration = SimulatorIntegration()
        cached_nsga = CachedNSGAIntegration(sim_integration)
        
        # Legacy format
        config_data = {
            'population_size': 10,
            'generations': 30,
            'mutation_rate': 0.4
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            result = cached_nsga.load_configuration(Path(temp_path))
            
            assert result is True
            assert cached_nsga.config['population_size'] == 10
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_prepare_instance(self):
        """Test preparing Instance object for cached NSGA-II."""
        sim_integration = SimulatorIntegration()
        cached_nsga = CachedNSGAIntegration(sim_integration)
        
        # Load a minimal config
        cached_nsga.config = {'population_size': 10, 'generations': 5, 'mutation_rate': 0.3}
        cached_nsga.simulation_params = {'scenario_seed': 1, 'simulation_seed': 2}
        
        instance = cached_nsga.prepare_instance(
            experiment_name='test_experiment',
            draw=False,
            scenario_seed=[1, 2],
            simulation_seed=42
        )
        
        assert instance is not None
        assert instance.experiment == 'test_experiment'
        assert instance.draw == False
        assert instance.scenario_seed == [1, 2]
        assert instance.simulation_seed == 42
    
    def test_singleton_pattern(self):
        """Test that get_cached_nsga_integration returns singleton."""
        sim_integration = SimulatorIntegration()
        
        instance1 = get_cached_nsga_integration(sim_integration)
        instance2 = get_cached_nsga_integration(sim_integration)
        
        assert instance1 is instance2


class TestNSGAIntegrationWithCached:
    """Test NSGAIntegration with cached workflow selection."""
    
    def test_nsga_integration_has_use_cached_flag(self):
        """Verify NSGAIntegration has use_cached flag."""
        from interface.services.nsga_integration import NSGAIntegration
        from interface.services.simulator_integration import SimulatorIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        assert hasattr(nsga, 'use_cached')
        assert nsga.use_cached == False  # Default to standard
    
    def test_set_use_cached_method(self):
        """Test setting cached NSGA-II mode."""
        from interface.services.nsga_integration import NSGAIntegration, CACHED_NSGA_AVAILABLE
        from interface.services.simulator_integration import SimulatorIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        # Try to enable cached mode
        result = nsga.set_use_cached(True)
        
        if CACHED_NSGA_AVAILABLE:
            assert result == True
            assert nsga.use_cached == True
        else:
            assert result == False
            assert nsga.use_cached == False
    
    def test_run_optimization_with_flag(self):
        """Test that run_optimization respects use_cached flag."""
        from interface.services.nsga_integration import NSGAIntegration, CACHED_NSGA_AVAILABLE
        from interface.services.simulator_integration import SimulatorIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        # Load minimal config
        config_data = {
            'nsga_config': {
                'population_size': 5,
                'generations': 2,
                'mutation_rate': 0.3
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            nsga.load_configuration(Path(temp_path))
            
            # Test standard mode (should fail gracefully without setup)
            nsga.set_use_cached(False)
            result = nsga.run_optimization()
            assert result is None  # Expected: no problem/algorithm configured
            
            # Test cached mode (should fail gracefully without experiment)
            if CACHED_NSGA_AVAILABLE:
                nsga.set_use_cached(True)
                result = nsga.run_optimization()
                # Should fail because no experiment_name provided
                assert result is None
        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestBackwardCompatibility:
    """Test that standard NSGA-II still works after cached integration."""
    
    def test_standard_nsga_unchanged(self):
        """Verify standard NSGA-II workflow is unchanged."""
        from interface.services.nsga_integration import NSGAIntegration
        from interface.services.simulator_integration import SimulatorIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        # Should default to standard mode
        assert nsga.use_cached == False
        
        # Standard methods should still exist
        assert hasattr(nsga, 'load_configuration')
        assert hasattr(nsga, 'setup_optimization')
        assert hasattr(nsga, 'run_optimization')
        assert hasattr(nsga, 'save_results')
        assert hasattr(nsga, 'extract_door_positions_from_map')
    
    def test_standard_config_still_loads(self):
        """Test that standard configuration still loads correctly."""
        from interface.services.nsga_integration import NSGAIntegration
        from interface.services.simulator_integration import SimulatorIntegration
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        config_data = {
            'nsga_config': {
                'population_size': 10,
                'generations': 20,
                'crossover_rate': 0.9,
                'mutation_rate': 0.1
            },
            'simulation_params': {
                'scenario_seed': 1,
                'simulation_seed': 2
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            result = nsga.load_configuration(Path(temp_path))
            assert result == True
            assert nsga.config is not None
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
