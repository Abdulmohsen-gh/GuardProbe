"""Test runner with repeated evaluations and transparent scoring."""
from datetime import datetime, timezone
from .detectors import check
from .ollama_client import ask


def evaluate(config, *, model=None, repeats=1, timeout=120):
    if repeats < 1 or repeats > 20:
        raise ValueError('repeats must be between 1 and 20')
    if not isinstance(config.get('tests'), list) or not config['tests']:
        raise ValueError('Configuration must contain at least one test')
    selected_model = model or config.get('model', 'llama3.2')
    rows = []
    for test in config['tests']:
        for iteration in range(1, repeats + 1):
            row = {'id': test['id'], 'category': test.get('category', 'general'),
                   'prompt': test['prompt'], 'repeat': iteration, 'status': 'ERROR',
                   'response': '', 'reason': ''}
            try:
                response = ask(test['prompt'], model=selected_model,
                               system=config.get('system', ''), timeout=timeout,
                               temperature=float(config.get('temperature', 0)))
                passed, reason = check(response, test['assertion'])
                row.update(response=response, reason=reason, status='PASS' if passed else 'FAIL')
            except (RuntimeError, ValueError, KeyError) as exc:
                row['reason'] = str(exc)
            rows.append(row)
            print(f"[{row['status']}] {row['id']} ({iteration}/{repeats}): {row['reason']}", flush=True)
    passed = sum(r['status'] == 'PASS' for r in rows)
    failed = sum(r['status'] == 'FAIL' for r in rows)
    errors = sum(r['status'] == 'ERROR' for r in rows)
    return {'tool': 'GuardProbe', 'version': '0.1.0', 'model': selected_model,
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'summary': {'total': len(rows), 'passed': passed, 'failed': failed, 'errors': errors,
                        'pass_rate_valid_pct': round(100 * passed / (passed + failed), 2) if passed + failed else None},
            'results': rows}
