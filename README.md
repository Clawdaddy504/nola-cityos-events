# NOLA CityOS Events

Merged JSON endpoint for live New Orleans event discovery.

## Endpoint

- `https://clawdaddy504.github.io/nola-cityos-events/events.json`

## Sources

Currently merges:
- WWOZ Livewire
- OffBeat Calendar

## Top-level schema

```json
{
  "count": 277,
  "generated_at": "2026-04-27T07:09:00+00:00",
  "events": [ ... ]
}
```

## Event schema

Each event object currently includes:

```json
{
  "id": "0661fa9352a610c6da03ee4120c5a0b601611431",
  "source": "wwoz",
  "title": "Johnny Jackson Jr. Gospel Is Alive! Celebration",
  "venue": "Rock of Ages Baptist Church",
  "venue_url": "https://www.wwoz.org/organizations/rock-ages-baptist-church",
  "event_url": "https://www.wwoz.org/events/1334456",
  "date_text": "Monday, April 27",
  "time_text": "9:30am",
  "start": "2026-04-27T09:30:00+00:00",
  "description": "Venue: Rock of Ages Baptist Church | Date: Monday, April 27 | Time: 9:30am"
}
```

## Field notes

- `id`: source-specific stable identifier/hash
- `source`: current upstream source (`wwoz` or `offbeat`)
- `title`: event title
- `venue`: venue or location name
- `venue_url`: upstream venue page when available
- `event_url`: canonical upstream event URL
- `date_text`: display-friendly date from source
- `time_text`: display-friendly time from source
- `start`: normalized ISO-8601 datetime when available
- `description`: compact human-readable summary

## Update cadence

This endpoint is refreshed automatically every 3 hours via GitHub Actions.
