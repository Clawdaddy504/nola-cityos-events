#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone

SOURCES = [
    'https://clawdaddy504.github.io/wwoz-livewire-rss/events.json',
    'https://clawdaddy504.github.io/offbeat-calendar-rss/events.json'
]

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def main():
    all_events = []
    for url in SOURCES:
        try:
            data = fetch_json(url)
            all_events.extend(data.get('events', []))
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Standardize and sort
    # We want a reliable 'start' timestamp for sorting
    # WWOZ and OffBeat now both include ISO 'start' in our standardized JSON format
    def sort_key(e):
        return e.get('start') or '9999-12-31'

    all_events.sort(key=sort_key)

    output = {
        'count': len(all_events),
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'events': all_events
    }

    with open('docs/events.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    main()
