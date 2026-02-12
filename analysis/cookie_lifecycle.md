# Akamai Bot Manager v2 — Cookie Lifecycle

## Cookies Used

### `bm_sz`
- **Set by:** Server on first request
- **Purpose:** Initial session tracking
- **Lifetime:** Session
- **Contains:** Encrypted session identifier and initial classification

### `_abck`
- **Set by:** Server after sensor data validation
- **Purpose:** Primary bot detection validation token
- **Lifetime:** Persistent (typically 1 year expiry)
- **Contains:** Encoded validation state

### `ak_bmsc`
- **Set by:** Server
- **Purpose:** Additional session tracking
- **Lifetime:** Session
- **Contains:** Session metadata

## Lifecycle Flow

```
1. First Request
   ┌─────────────────────────────────────────┐
   │ GET /page HTTP/1.1                       │
   │                                          │
   │ Response:                                │
   │   Set-Cookie: bm_sz=<initial_value>      │
   │   Set-Cookie: _abck=<challenge_state>    │
   │   Body: HTML + <script src="b.js">       │
   └─────────────────────────────────────────┘

2. Sensor Script Executes
   ┌─────────────────────────────────────────┐
   │ Browser loads and executes sensor script │
   │ Collects 100+ signals                   │
   │ Encodes into sensor data string          │
   └─────────────────────────────────────────┘

3. Sensor Data Submission
   ┌─────────────────────────────────────────┐
   │ POST /_sec/cp_challenge/verify           │
   │ Cookie: bm_sz=...; _abck=...            │
   │ Body: {sensor_data: "<encoded_string>"}  │
   │                                          │
   │ Response:                                │
   │   Set-Cookie: _abck=<validated_state>    │
   └─────────────────────────────────────────┘

4. Protected Request
   ┌─────────────────────────────────────────┐
   │ GET /api/products HTTP/1.1               │
   │ Cookie: bm_sz=...; _abck=<valid>        │
   │                                          │
   │ Server checks _abck validity             │
   │ → Valid: 200 OK                          │
   │ → Invalid: 403 or challenge              │
   └─────────────────────────────────────────┘
```

## _abck Cookie States

The `_abck` cookie value indicates the current validation state:

| Pattern | Meaning |
|---------|---------|
| Contains `~0~` | Initial state, no sensor data received |
| Contains `~-1~` | Challenge required, awaiting sensor data |
| Contains `~0~-1~` | Sensor received but not yet validated |
| Valid hash pattern | Fully validated session |

## Multiple Submissions

Akamai may require **multiple sensor data submissions** before granting a valid `_abck`:

1. First submission → Initial signals collected
2. Second submission → Behavioral signals (after user interaction)
3. Third submission → Additional validation (if suspicious)

Each submission updates the `_abck` cookie with a new validation state.

## Expiration and Renewal

- `_abck` has a long expiry (1 year) but the **validation state** expires much sooner
- After state expiration, the sensor script re-collects and re-submits
- Rate-limited submissions may trigger challenges or blocks
