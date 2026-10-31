"""Command-line entry point."""
import argparse
import json
from pathlib import Path
from .evaluator import evaluate
from .reporting import save


def main():
    parser = argparse.ArgumentParser(prog='guardprobe', description='Test local LLM guardrails and export evidence')
    parser.add_argument('--config', default='configs/safety_tests.json', help='JSON test configuration')
    parser.add_argument('--model', default=None, help='Ollama model override')
    parser.add_argument('--repeat', type=int, default=1, help='Times per test (1-20)')
    parser.add_argument('--timeout', type=int, default=120, help='Seconds per model request')
    parser.add_argument('--output', default='reports/latest', help='Report directory')
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.config).read_text(encoding='utf-8'))
        report = evaluate(config, model=args.model, repeats=args.repeat, timeout=args.timeout)
        json_path, html_path = save(report, args.output)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f'GuardProbe error: {exc}\n')
    print('\nSUMMARY:', report['summary'])
    print(f'Reports: {json_path} and {html_path}')
    return 0 if report['summary']['errors'] == 0 else 1
