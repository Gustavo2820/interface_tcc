<!-- .github/copilot-instructions.md -->
# Guidance for AI coding agents working on this repository

This repository implements evacuation simulation and optimization (NSGA-II, brute-force) with a Streamlit-based UI. The file below gives short, actionable facts that help an AI agent be productive immediately.

Keep guidance concise: prefer concrete file/command references and examples from the codebase.

1) Big-picture architecture (what to touch first)
- UI / Integration layer: `interface/` — Streamlit app and page modules. The primary entry is `interface/App.py` which configures layout, CSS and the top-level menu. Use this when making UI changes.
- Integration services: `interface/services/` — thin adaptors between the UI and simulation/optimization modules. Key files:
  - `interface/services/map_creation_integration.py` — map conversion, validation, and PNG↔map helpers. It imports `modulo_criacao_mapas` by appending its path to sys.path.
  - `interface/services/nsga_integration.py` — glue between Streamlit and the NSGA-II flow. It depends on `simulador_heuristica` and `pymoo`. It defines `EvacuationProblem` (pymoo Problem shim) and `NSGAIntegration` helper methods.
  - `interface/services/simulator_integration.py` — invoker for the simulator CLI, prepares inputs under `simulador_heuristica/input/<experiment>` and reads outputs from `simulador_heuristica/output/<experiment>`.
- Core simulation/heuristics: `simulador_heuristica/` — contains simulator, heuristics, and unified config formats. Treat it as a separate package imported with -m (see simulator invocation in services).

2) Important workflows & run commands (verified by reading integration code)
- Run the Streamlit UI: from repo root run `streamlit run interface/App.py` (App uses Streamlit APIs and expects project structure to be intact).
- Run the simulator CLI (used by integrations): the `SimulatorIntegration.run_simulator_cli` builds a command similar to:
  python -m simulador_heuristica.simulator.main -e <experiment_name> [-d] [-m <scenario_seed>] [-s <simulation_seed>]
  Always set CWD to the project root (services use cwd=project_root when running the command).
- NSGA-II via pymoo: `interface/services/nsga_integration.py` constructs a `NSGA2` object and calls `minimize(problem, algorithm, termination=('n_gen', generations))`. Ensure `pymoo` is installed and available in the same interpreter that runs Streamlit.

3) Project-specific conventions and patterns
- Path manipulation: integration services append package folders to sys.path at runtime to import modules (e.g. `sys.path.append(str(map_creation_module))` and adding `simulador_heuristica` subpaths). Avoid moving code that assumes these relative imports without updating sys.path logic.
- Temporary experiment data: NSGA and simulator create temporary experiment folders under `temp_nsga/` and `simulador_heuristica/input/<experiment>` respectively. Cleaning happens after evaluation but integrations expect this structure—use the integration helpers (`SimulatorIntegration.prepare_experiment_from_uploads`) to stage files.
- Map format: simulator map files are plain text (`map.txt`) with single-character terrain codes (e.g., '2' = door). `nsga_integration.EvacuationProblem._generate_map_with_doors` edits these maps by replacing characters. When writing map generators/editors, follow the same char encoding.
- Database: `interface/services/simulator_integration.py` uses a SQLite DB and expects tables like `Simulacao`, `Mapa`, `Resultado`; migrations are not provided — be cautious when writing DB code.

4) Dependencies & environment notes
- Python packages that appear required at runtime: streamlit, numpy, PIL (Pillow), pymoo. Check and update `requirements.txt` if adding new packages.
- The NSGA integration prints debug messages and uses Streamlit UI methods (e.g., `st.info`, `st.error`) — run under Streamlit to see full feedback.

5) Integration and extension tips (quick patterns)
- To add a new simulation-driven feature in the UI:
  1. Add a Streamlit page file under `interface/pages/` and import any services from `interface/services`.
  2. Use service singletons exported at the bottom of each integration file (e.g., `map_creation_service`) instead of re-instantiating.
 3. Stage files through `SimulatorIntegration.prepare_experiment_from_uploads` so the simulator can find inputs.

- To add a new optimization algorithm alongside NSGA-II:
  - Create a new integration module similar to `nsga_integration.py` following the pattern: configuration loader, Problem adapter, algorithm setup, run and save_results.
  - Reuse `SimulatorIntegration` to run and read results. Keep algorithm code isolated from file staging.

6) Debugging pointers (what to inspect first when things fail)
- Import errors for `pymoo` or other libs: `nsga_integration.py` populates sys.path and prints debug traces — run the Streamlit app to view `st.error` messages and printed tracebacks.
- Simulator invocation: inspect `interface/services/simulator_integration.py::run_simulator_cli` for the exact command and working directory. If outputs are missing, check `simulador_heuristica/output/<experiment>` and `subprocess.CompletedProcess` captures stdout/stderr.
- Map validation/conversion: `map_creation_integration.validate_map_image` enforces size bounds (5x5 min, 100x100 max) and checks for compatible colors. Use the same RGB palette when generating maps.

7) Files to reference for concrete examples
- `docs/ARCHITECTURE.md` — high level architecture, data flows and patterns (factory, strategy, cache notes).
- `interface/App.py` — Streamlit entry and UI reset logic (clears session_state and st.cache).
- `interface/services/nsga_integration.py` — full example of Problem adapter and use of pymoo.
- `interface/services/simulator_integration.py` — how experiments are staged and the exact CLI invocation.
- `interface/services/map_creation_integration.py` — map PNG↔map.txt conversions and validation rules.

If any section is unclear or you'd like me to expand with examples (e.g., exact Streamlit run command in context of a virtualenv or a minimal reproduction for running NSGA evaluations locally), tell me which area and I'll iterate.

-- End of file
