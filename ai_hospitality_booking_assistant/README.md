# AI Hospitality Booking Assistant — Prototype

## Overview
A Python CLI prototype of a hospitality booking assistant. It demonstrates a simple state-machine conversation for **restaurant** and **hotel** bookings.

> All availability and prices are mock/sample data. This prototype does not connect to a real business, payment system, or reservation platform.

## Features
- Restaurant booking flow: date → time → party size → availability → confirmation.
- Hotel booking flow: check-in/check-out → room type → guests → availability → confirmation.
- Mock availability dataset stored in `mock_availability.json`.
- Basic validation:
  - Date must not be in the past.
  - Date format must be `YYYY-MM-DD`.
  - Time format must be `HH:MM`.
  - Party size must be an integer from 1–20.
  - Hotel check-out must be after check-in.
- Mock confirmation ID after successful confirmation.
- State-machine logic implemented with explicit states.

## Project Structure
```text
ai_hospitality_booking_assistant/
├── app.py
├── mock_availability.json
├── flow_diagram.md
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.9+
- No external packages are required.

## How to Run
1. Open a terminal in this project folder.
2. Run:

```bash
python app.py
```

3. Select Restaurant or Hotel.
4. Enter the requested booking details.
5. The assistant checks the mock dataset.
6. Confirm or cancel the booking.

## Example Restaurant Test
Use:
- Date: `2026-08-20`
- Time: `19:30`
- Guests: `4`
- Confirmation: `yes`

This should find a matching mock slot.

## Example Validation Tests
Try:
- A date such as `2020-01-01` → rejected because it is in the past.
- Party size `0` → rejected.
- Party size `25` → rejected.
- Time `25:99` → rejected.
- Hotel check-out earlier than check-in → rejected.

## State Machine
The main states are:

`START → DATE → TIME/ROOM → PARTY/GUESTS → CHECK_AVAILABILITY → CONFIRM → DONE`

If availability is not found:

`CHECK_AVAILABILITY → CANCEL → DONE`

## Limitations
This is intentionally a prototype:
- No database.
- No real API.
- No authentication.
- No payment processing.
- No natural-language AI/NLP model.
- Availability is fixed sample data.
- Hotel booking uses the selected check-in date for the mock availability lookup.

## Possible Future Improvements
- Add a web chat UI using Streamlit.
- Add fuzzy/NLP input such as “tomorrow at 7:30 for 4 people.”
- Add SQLite/PostgreSQL.
- Add real-time availability APIs.
- Add booking modification and cancellation.
- Add email/SMS confirmation.
- Add an LLM layer while keeping the state machine as the safety/control layer.

## Learning Resource
The task-provided YouTube search for Python chatbot conversation flow can be used as a learning reference:
https://www.youtube.com/results?search_query=python+chatbot+conversation+flow+tutorial
