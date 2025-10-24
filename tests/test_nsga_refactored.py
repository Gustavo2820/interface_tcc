"""
Integration test for NSGA after refactoring to use integration_api.

This test verifies that the refactored NSGA integration maintains identical
behavior to the previous implementation, now delegating to the official
simulator integration_api instead of duplicating logic.
"""

import pytest
import json
from pathlib import Path
from interface.services.nsga_integration import NSGAIntegration
from interface.services.simulator_integration import SimulatorIntegration


class TestNSGAIntegrationRefactored:
    """Test NSGA integration after refactoring."""
    
    def test_extract_door_positions_uses_integration_api(self):
        """Verify extract_door_positions_from_map delegates to integration_api."""
        nsga = NSGAIntegration(simulator_integration=None)
        
        # Test map with known door configuration
        map_text = "00000\n02220\n00000"
        doors = nsga.extract_door_positions_from_map(map_text)
        
        # Should return grouped door dicts
        assert isinstance(doors, list)
        assert len(doors) == 1
        assert isinstance(doors[0], dict)
        assert doors[0]['direction'] == 'H'
        assert doors[0]['size'] == 3
    
    def test_map_generation_consistency(self):
        """Verify map generation produces consistent results."""
        from interface.services.nsga_integration import EvacuationProblem
        
        sim_integration = SimulatorIntegration()
        nsga = NSGAIntegration(sim_integration)
        
        map_template = "00000\n00000\n00000"
        individuals = {'caracterizations': [{'amount': 1, 'age': 30}]}
        doors = [{'row': 1, 'col': 1, 'size': 3, 'direction': 'H'}]
        
        problem = EvacuationProblem(
            sim_integration,
            map_template,
            individuals,
            doors,
            {}
        )
        
        # Generate map with doors
        result_map = problem._generate_map_with_doors(doors)
        
        # Verify doors are in correct position
        lines = result_map.split('\n')
        assert lines[1] == "02220"
    
    def test_door_expansion_in_save_results(self):
        """Verify save_results correctly expands doors using integration_api."""
        # This is tested indirectly through the full NSGA flow
        # but we can verify the expansion logic works correctly
        from simulador_heuristica.simulator import integration_api
        
        grouped = [
            {'row': 0, 'col': 1, 'size': 2, 'direction': 'H'},
            {'row': 2, 'col': 0, 'size': 3, 'direction': 'V'}
        ]
        
        expanded = integration_api.expand_grouped_doors(grouped)
        
        # Should have 5 total door cells (2 H + 3 V)
        assert len(expanded) == 5
        
        # Verify horizontal door cells
        assert [1, 0] in expanded
        assert [2, 0] in expanded
        
        # Verify vertical door cells
        assert [0, 2] in expanded
        assert [0, 3] in expanded
        assert [0, 4] in expanded
    
    def test_backward_compatibility_with_tuple_doors(self):
        """Verify system still handles legacy tuple-format doors."""
        from interface.services.nsga_integration import EvacuationProblem
        from simulador_heuristica.simulator import integration_api
        
        # Mix of grouped dicts and legacy tuples
        mixed_doors = [
            {'row': 0, 'col': 0, 'size': 2, 'direction': 'H'},
            (5, 5)
        ]
        
        expanded = integration_api.expand_grouped_doors(mixed_doors)
        
        # Should handle both formats
        assert len(expanded) == 3
        assert [0, 0] in expanded
        assert [1, 0] in expanded
        assert [5, 5] in expanded
    
    def test_integration_api_availability(self):
        """Verify integration_api is properly imported."""
        from interface.services import nsga_integration
        
        # Should have imported integration_api at module level
        assert hasattr(nsga_integration, 'integration_api')
        
        # Should not be None if import succeeded
        if nsga_integration.integration_api is not None:
            # Verify key functions are available
            assert hasattr(nsga_integration.integration_api, 'extract_doors_from_map_text')
            assert hasattr(nsga_integration.integration_api, 'expand_grouped_doors')
            assert hasattr(nsga_integration.integration_api, 'generate_map_text_with_grouped_doors')


class TestSimulatorIntegrationRefactored:
    """Test SimulatorIntegration after removing duplicated StructureMap."""
    
    def test_structure_map_imported_from_simulator(self):
        """Verify StructureMap is imported from simulator package."""
        from interface.services import simulator_integration
        
        # Should import StructureMap from simulator
        assert hasattr(simulator_integration, 'StructureMap')
        
        # Verify it's the official simulator class
        from simulador_heuristica.simulator.structure_map import StructureMap as OfficialStructureMap
        assert simulator_integration.StructureMap is OfficialStructureMap
    
    def test_integration_api_imported(self):
        """Verify integration_api is available in simulator_integration."""
        from interface.services import simulator_integration
        
        assert hasattr(simulator_integration, 'integration_api')
        
        # Verify it has expected functions
        if simulator_integration.integration_api:
            assert callable(simulator_integration.integration_api.parse_map_text)
            assert callable(simulator_integration.integration_api.extract_doors_from_map_text)


class TestNoCodeDuplication:
    """Verify that no simulation logic is duplicated in integration files."""
    
    def test_nsga_integration_delegates_door_extraction(self):
        """Verify nsga_integration delegates door extraction to integration_api."""
        import inspect
        from interface.services.nsga_integration import NSGAIntegration
        
        # Get source of extract_door_positions_from_map
        source = inspect.getsource(NSGAIntegration.extract_door_positions_from_map)
        
        # Should call integration_api, not implement its own logic
        assert 'integration_api.extract_doors_from_map_text' in source
        
        # Should have deprecation warning for fallback
        assert 'deprecated' in source.lower() or 'legacy' in source.lower()
    
    def test_no_inline_door_grouping_logic(self):
        """Verify no inline door grouping algorithm in integration files."""
        nsga_file = Path(__file__).parent.parent / 'interface' / 'services' / 'nsga_integration.py'
        
        if nsga_file.exists():
            content = nsga_file.read_text()
            
            # Should reference integration_api for door operations
            assert 'integration_api' in content
            
            # Old inline grouping pattern should be gone or marked deprecated
            # (checking for the old dummy = types.SimpleNamespace() pattern
            # that was used before integration_api)
            if 'dummy = types.SimpleNamespace()' in content:
                # If it exists, should be in fallback/deprecated section
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'dummy = types.SimpleNamespace()' in line:
                        # Check nearby lines for deprecation markers
                        context = '\n'.join(lines[max(0, i-5):min(len(lines), i+5)])
                        assert 'deprecated' in context.lower() or 'fallback' in context.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
