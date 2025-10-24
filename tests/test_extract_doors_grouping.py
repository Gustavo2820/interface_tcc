"""
Test for door extraction and grouping.

This test verifies that NSGAIntegration correctly delegates to the
integration_api for door extraction, which in turn calls the simulator's
extract_doors_info logic.
"""
import pytest
from interface.services.nsga_integration import NSGAIntegration


def test_extract_doors_grouping_horizontal():
    # Map with a horizontal block of three door cells at row 1, cols 1-3
    map_template = """
00000
022220
00000
"""
    nsga = NSGAIntegration(simulator_integration=None)
    doors = nsga.extract_door_positions_from_map(map_template)
    # Expect one grouped door configuration
    assert isinstance(doors, list)
    assert len(doors) == 1
    d = doors[0]
    assert isinstance(d, dict)
    assert d.get('direction') == 'H'
    assert d.get('row') == 1
    assert d.get('col') == 1
    # the map line '022220' contains four consecutive '2' chars -> size 4
    assert int(d.get('size', 0)) == 4
