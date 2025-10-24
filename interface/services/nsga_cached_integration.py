"""
Integration module for cached NSGA-II from simulador_heuristica/unified.

This module provides an adapter to use the cached NSGA-II implementation
(from unified folder) with the interface, maintaining compatibility with
the standard pymoo-based NSGA-II workflow.

IMPORTANT: This module REUSES the existing cached NSGA-II implementation
from simulador_heuristica/unified/mh_ga_factory.py and mh_ga_nsgaii.py.
No duplication of algorithm logic - only integration adapters.

Key differences from standard NSGA-II:
- Uses custom Gene/Chromosome classes
- Has built-in simulation result caching (avoids re-running identical simulations)
- Returns 3 objectives: [num_doors, iterations, distance]
- Uses custom crossover and mutation operators

Authors:
    Cached NSGA-II integration - 2025
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np

from .logger import default_log as logger

# Add unified path to sys.path
project_root = Path(__file__).resolve().parents[2]
unified_path = project_root / "simulador_heuristica" / "unified"
if str(unified_path) not in sys.path:
    sys.path.insert(0, str(unified_path))

# Import the cached NSGA-II implementation from unified folder
try:
    from mh_ga_instance import Instance
    from mh_ga_factory import Factory, selector
    from mh_ga_nsgaii import nsgaii as cached_nsgaii
    logger.info("Successfully imported cached NSGA-II from unified folder")
except ImportError as e:
    logger.error(f"Failed to import cached NSGA-II: {e}")
    Instance = None
    Factory = None
    selector = None
    cached_nsgaii = None


class CachedNSGAIntegration:
    """
    Integration adapter for cached NSGA-II implementation.
    
    This class adapts the cached NSGA-II from simulador_heuristica/unified
    to work with the interface's input/output formats.
    """
    
    def __init__(self, simulator_integration):
        """
        Initialize cached NSGA integration.
        
        Args:
            simulator_integration: SimulatorIntegration instance
        """
        self.simulator_integration = simulator_integration
        self.config = None
        self.simulation_params = {}
        self.use_three_objectives = False  # Flag for 3-objective mode
    
    def load_configuration(self, config_file: Path) -> bool:
        """
        Load configuration for cached NSGA-II.
        
        Supports both unified format and legacy format.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Detect format
            if 'nsga_config' in config:
                # Unified format
                logger.info("Detected unified configuration format")
                nsga_config = config['nsga_config']
                self.simulation_params = config.get('simulation_params', {})
                self.config = nsga_config
                
                # Check for 3-objective mode flag
                self.use_three_objectives = nsga_config.get('use_three_objectives', False)
                if self.use_three_objectives:
                    logger.info("✓ 3-objective mode ENABLED (num_doors, iterations, distance)")
                else:
                    logger.info("Using 2-objective mode (num_doors, distance) with iterations as auxiliary")
            else:
                # Legacy format
                logger.info("Detected legacy configuration format")
                self.config = config
                self.simulation_params = {}
                self.use_three_objectives = config.get('use_three_objectives', False)
            
            # Validate required keys
            required_keys = ['population_size', 'generations', 'mutation_rate']
            if not all(key in self.config for key in required_keys):
                logger.error("Configuration missing required keys")
                return False
            
            logger.info(f"Configuration loaded: pop={self.config['population_size']}, "
                       f"gen={self.config['generations']}, "
                       f"mut={self.config['mutation_rate']}")
            return True
            
        except Exception as e:
            logger.exception(f"Error loading configuration: {e}")
            return False
    
    def prepare_instance(
        self, 
        experiment_name: str,
        draw: bool = False,
        scenario_seed: Optional[List[int]] = None,
        simulation_seed: int = 0
    ) -> Any:
        """
        Prepare an Instance object for cached NSGA-II.
        
        Args:
            experiment_name: Name of the experiment
            draw: Whether to draw simulation frames
            scenario_seed: List of scenario seeds (for multiple runs)
            simulation_seed: Simulation seed
            
        Returns:
            Instance object for cached NSGA-II
        """
        if Instance is None:
            raise RuntimeError("Cached NSGA-II not available (import failed)")
        
        # Default to single scenario seed if not provided
        if scenario_seed is None:
            scenario_seed = [self.simulation_params.get('scenario_seed', 0)]
        elif not isinstance(scenario_seed, list):
            scenario_seed = [scenario_seed]
        
        if simulation_seed is None:
            simulation_seed = self.simulation_params.get('simulation_seed', 0)
        
        return Instance(
            experiment=experiment_name,
            draw=draw,
            scenario_seed=scenario_seed,
            simulation_seed=simulation_seed
        )
    
    def run_optimization(
        self,
        experiment_name: str,
        draw: bool = False
    ) -> Optional[List]:
        """
        Run cached NSGA-II optimization.
        
        Args:
            experiment_name: Name of the experiment
            draw: Whether to draw simulation frames
            
        Returns:
            List of Chromosome objects (Pareto front) or None on error
        """
        if cached_nsgaii is None or Factory is None or selector is None:
            logger.error("Cached NSGA-II not available")
            return None
        
        if not self.config:
            logger.error("Configuration not loaded")
            return None
        
        try:
            # Prepare instance
            scenario_seed = self.simulation_params.get('scenario_seed', [0])
            if not isinstance(scenario_seed, list):
                scenario_seed = [scenario_seed]
            
            simulation_seed = self.simulation_params.get('simulation_seed', 0)
            
            instance = self.prepare_instance(
                experiment_name=experiment_name,
                draw=draw,
                scenario_seed=scenario_seed,
                simulation_seed=simulation_seed
            )
            
            # Create factory with caching
            logger.info("Creating Factory with simulation caching...")
            factory = Factory(instance)
            
            # Run cached NSGA-II
            population_size = self.config['population_size']
            mutation_prob = self.config['mutation_rate']
            max_generations = self.config['generations']
            
            logger.info(f"Starting cached NSGA-II: pop={population_size}, "
                       f"mut={mutation_prob}, gen={max_generations}")
            
            results = cached_nsgaii(
                factory=factory,
                selector=selector,
                population_size=population_size,
                mutation_probability=mutation_prob,
                max_generations=max_generations
            )
            
            logger.info(f"Cached NSGA-II completed: {len(results)} solutions in Pareto front")
            logger.info(f"Cache statistics: {len(factory.cache)} simulations cached")
            
            return results, factory
            
        except Exception as e:
            logger.exception(f"Error running cached NSGA-II: {e}")
            return None
    
    def convert_results_to_standard_format(
        self,
        results: List,
        factory: Any
    ) -> List[Dict[str, Any]]:
        """
        Convert cached NSGA-II results to standard interface format.
        
        The cached NSGA-II returns Chromosome objects with:
        - gene: Gene object with configuration (boolean array)
        - obj: [num_doors, iterations, distance]
        - generation: birth generation
        
        This converts to the format expected by the results page.
        
        When use_three_objectives=False (default):
        - objectives: [num_doors, distance] (2 objectives for compatibility)
        - iterations: stored as auxiliary metric
        
        When use_three_objectives=True:
        - objectives: [num_doors, iterations, distance] (3 objectives)
        - iterations is a true optimization objective
        
        Args:
            results: List of Chromosome objects
            factory: Factory instance (to decode genes)
            
        Returns:
            List of solution dictionaries
        """
        from simulador_heuristica.simulator import integration_api
        
        converted = []
        
        for i, chromosome in enumerate(results):
            # Extract data from chromosome
            gene_config = chromosome.gene.configuration
            num_doors, iterations, distance = chromosome.obj
            generation = chromosome.generation
            
            # Decode gene to get door configurations
            doors_grouped = factory.uncode(chromosome.gene)
            
            # Expand grouped doors to per-cell coordinates
            try:
                doors_expanded = integration_api.expand_grouped_doors(doors_grouped)
            except Exception as e:
                logger.warning(f"Failed to expand doors for solution {i}: {e}")
                doors_expanded = []
            
            # Build objectives array based on mode
            if self.use_three_objectives:
                # 3-objective mode: all three are optimization objectives
                objectives_array = [int(num_doors), int(iterations), float(distance)]
            else:
                # 2-objective mode: iterations is auxiliary
                objectives_array = [int(num_doors), float(distance)]
            
            # Build result object (compatible with standard NSGA format)
            result_obj = {
                "solution_id": i,
                "gene": list(gene_config),
                "door_positions": doors_expanded,  # Primary key: expanded coords
                "door_positions_grouped": doors_grouped,  # Secondary key: grouped format
                "objectives": objectives_array,
                "num_doors": int(num_doors),
                "iterations": int(iterations),  # Always present as field
                "distance": float(distance),
                "generation": int(generation),
                "algorithm": f"NSGA-II-Cached-{len(objectives_array)}obj"
            }
            
            converted.append(result_obj)
        
        mode_str = "3-objective" if self.use_three_objectives else "2-objective"
        logger.info(f"Converted {len(converted)} cached NSGA-II results to standard format ({mode_str} mode)")
        return converted
    
    def save_results(
        self,
        results: List,
        factory: Any,
        output_file: Path
    ) -> bool:
        """
        Save cached NSGA-II results to file.
        
        Args:
            results: List of Chromosome objects
            factory: Factory instance
            output_file: Path to output file
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Convert to standard format
            converted = self.convert_results_to_standard_format(results, factory)
            
            # Atomic write
            tmp_path = output_file.with_suffix('.tmp')
            try:
                with open(tmp_path, 'w') as f:
                    json.dump(converted, f, indent=2)
                tmp_path.replace(output_file)
                logger.info(f"Saved cached NSGA-II results to {output_file}")
                return True
            finally:
                if tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
                    
        except Exception as e:
            logger.exception(f"Error saving cached NSGA-II results: {e}")
            return False


# Singleton instance
_cached_nsga_integration_singleton = None

def get_cached_nsga_integration(simulator_integration):
    """
    Get or create the cached NSGA integration singleton.
    
    Args:
        simulator_integration: SimulatorIntegration instance
        
    Returns:
        CachedNSGAIntegration instance
    """
    global _cached_nsga_integration_singleton
    if _cached_nsga_integration_singleton is None:
        _cached_nsga_integration_singleton = CachedNSGAIntegration(simulator_integration)
    return _cached_nsga_integration_singleton
