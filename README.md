# GuardProbe

A small reusable **local AI security evaluation CLI** built in Python, inspired by Promptfoo and Garak. Built for the ASCL AI Security Training A4 capstone. GuardProbe submits configured probes to a local Ollama model, checks responses with transparent deterministic detectors, repeats tests, and exports JSON and standalone HTML evidence.

## Architecture

- `cli.py`: command-line argument parsing.
- `ollama_client.py`: local-only Ollama HTTP chat API client.
- `detectors.py`: reusable assertions (forbidden text, required text, refusal heuristic, scope check).
- `evaluator.py`: test execution, repeatability, output and error tracking.
- `reporting.py`: human-readable HTML and machine-readable JSON reports.
- `configs/safety_tests.json`: editable model, system message and test-case configuration.
- `tests/test_detectors.py`: automated unit tests.

**Original contribution:** lightweight dependency-free local runner, configurable test assertions, repeated checks, localhost-only endpoint guard, and shareable self-contained reports.

## Requirements

Python 3.10+ and a running Ollama service with `llama3.2` pulled.

```bash
ollama serve     # use another terminal if needed
ollama list
```

## Run

From this repository directory:

```bash
python3 -m unittest discover -s tests -v
python3 -m guardprobe --config configs/safety_tests.json --repeat 1 --output reports/latest
python3 -m guardprobe --model qwen2.5:3b --repeat 2 --output reports/qwen
```

Open `reports/latest/results.html` in a browser. JSON output is saved beside it. Config entries include `id`, `category`, `prompt`, and an `assertion` with a `type` and related fields. Supported detector types: `must_not_contain`, `must_contain`, `must_refuse`, `must_stay_in_scope`.

## Expected output

Terminal status for each case, summary counts, `reports/latest/results.json` and `reports/latest/results.html`. Counts depend on model behavior; **results must be obtained from a real run, not invented**.

## Security and evaluation limitations

- Run only on locally controlled models and benign test fixtures; the demo `BLUE-42` value is intentionally fictitious.
- Tests for dangerous content use high-level safety/refusal checks, not harmful synthesis instructions. This does not implement the full substance-specific rubric of the A4 handout.
- Refusal detection is a keyword-based heuristic and may misclassify answers; manually review findings.
- A passing test is not proof of general model safety or production readiness.
- Models may still perform network actions independently; localhost-only target URL is not complete network isolation.
- Never put real secrets in system prompts, and validate privileged actions server-side.

## Extension ideas

Add a YAML parser, additional detector plugins, human review annotations, stronger semantic grading, CI, and per-test severity labels.
