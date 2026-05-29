#!/usr/bin/env python3
import hashlib
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SOURCES = [
    'https://clawdaddy504.github.io/wwoz-livewire-rss/events.json',
    'https://clawdaddy504.github.io/offbeat-calendar-rss/events.json'
]
NOLA_SHOW_URL = 'https://nola.show/events.json'

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def stable_id(*parts):
    raw = '|'.join(str(part or '').strip().lower() for part in parts)
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()

def normalize_nola_show_event(event):
    event_name = (event.get('event_name') or '').strip()
    venue_name = (event.get('venue_name') or '').strip()
    start = event.get('event_date')

    if not event_name or not venue_name or not start:
        return None

    ticket_link = event.get('ticket_link')
    ticket_price = event.get('ticket_price')
    door_price = event.get('door_price')
    price_parts = []

    if ticket_price and ticket_price != 'null':
        price_parts.append(f"Ticket: {ticket_price}")

    if door_price and door_price != 'null':
        price_parts.append(f"Door: {door_price}")

    description_parts = [
        f"Venue: {venue_name}",
        f"Starts: {start}"
    ]

    if price_parts:
        description_parts.append(' | '.join(price_parts))

    return {
        'id': f"nola-show-{event.get('id') or stable_id(event_name, venue_name, start)}",
        'source': 'nola_show',
        'title': event_name,
        'venue': venue_name,
        'event_url': ticket_link or f"https://nola.show/index.html?venue={urllib.parse.quote(venue_name)}",
        'start': start,
        'description': ' | '.join(description_parts)
    }

def fetch_nola_show_events():
    data = fetch_json(NOLA_SHOW_URL)

    if not isinstance(data, list):
        return []

    events = [normalize_nola_show_event(event) for event in data]
    return [event for event in events if event]

def main():
    all_events = []
    source_health = []

    for url in SOURCES:
        try:
            data = fetch_json(url)
            events = data.get('events', [])
            all_events.extend(events)
            source_health.append({
                'source': url,
                'status': 'ok',
                'count': len(events)
            })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            source_health.append({
                'source': url,
                'status': 'error',
                'error': str(e)
            })

    try:
        nola_show_events = fetch_nola_show_events()
        all_events.extend(nola_show_events)
        source_health.append({
            'source': NOLA_SHOW_URL,
            'status': 'ok',
            'count': len(nola_show_events)
        })
    except Exception as e:
        print(f"Error fetching {NOLA_SHOW_URL}: {e}")
        source_health.append({
            'source': NOLA_SHOW_URL,
            'status': 'error',
            'error': str(e)
        })

    # Standardize and sort
    # We want a reliable 'start' timestamp for sorting
    # WWOZ and OffBeat now both include ISO 'start' in our standardized JSON format
    def sort_key(e):
        return e.get('start') or '9999-12-31'

    all_events.sort(key=sort_key)

    output = {
        'count': len(all_events),
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_health': source_health,
        'events': all_events
    }

    with open('docs/events.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    main()
