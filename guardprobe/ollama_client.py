"""HTTP client for a local Ollama server. No third-party dependencies."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def ask(prompt, *, model='llama3.2', base_url='http://127.0.0.1:11434', system='', timeout=120, temperature=0):
    if not base_url.startswith(('http://127.0.0.1:', 'http://localhost:', 'http://[::1]:')):
        raise ValueError('Only local Ollama endpoints are allowed')
    messages = []
    if system:
        messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': prompt})
    payload = json.dumps({'model': model, 'messages': messages, 'stream': False,
                          'options': {'temperature': temperature}}).encode('utf-8')
    request = Request(base_url.rstrip('/') + '/api/chat', data=payload,
                      headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.load(response)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f'Ollama connection failed: {exc}') from exc
    return body.get('message', {}).get('content', '')
