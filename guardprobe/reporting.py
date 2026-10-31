"""JSON and self-contained HTML reports."""
import html
import json
from pathlib import Path


def save(report, destination):
    directory = Path(destination)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = report['summary']
    cells = []
    for row in report['results']:
        cols = (row['id'], row['category'], str(row['repeat']), row['status'], row['prompt'], row['response'], row['reason'])
        cells.append('<tr>' + ''.join(f'<td><pre>{html.escape(str(c))}</pre></td>' for c in cols) + '</tr>')
    document = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>GuardProbe Report</title>
<style>body{{font:15px system-ui;margin:2rem;color:#182336;background:#f7f9fc}}h1{{color:#146f60}}
.summary{{padding:1rem;background:white;border:1px solid #ddd;border-radius:12px;margin-bottom:1rem}}
table{{border-collapse:collapse;width:100%;background:white}}th,td{{border:1px solid #ddd;padding:9px;text-align:left;vertical-align:top}}
th{{background:#e8f2ef}}pre{{white-space:pre-wrap;word-break:break-word;font:12px ui-monospace}}</style>
<h1>GuardProbe | Local AI Security Evaluation</h1><div class="summary"><b>Model:</b> {html.escape(report['model'])}<br>
<b>Run:</b> {html.escape(report['timestamp_utc'])}<br><b>Total:</b> {summary['total']} &nbsp;
<b>Passed:</b> {summary['passed']} &nbsp;<b>Failed:</b> {summary['failed']} &nbsp;<b>Errors:</b> {summary['errors']}
<br><b>Pass rate (valid tests):</b> {summary['pass_rate_valid_pct']}%</div>
<p>Heuristic results require human review. PASS does not establish general model safety.</p>
<table><thead><tr><th>ID</th><th>Category</th><th>Repeat</th><th>Status</th><th>Prompt</th><th>Response</th><th>Reason</th></tr></thead>
<tbody>{''.join(cells)}</tbody></table></html>'''
    (directory / 'results.html').write_text(document, encoding='utf-8')
    return directory / 'results.json', directory / 'results.html'
