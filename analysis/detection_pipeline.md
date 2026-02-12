# Akamai Bot Manager v2 — Detection Pipeline

## Request Flow

```
Client Request (first visit)
    │
    ├── Server responds with HTML + Akamai script tag
    │   └── <script src="/<hash>/.../<hash>/b.js"></script>
    │
    ├── Browser loads sensor script (~512KB)
    │   ├── String array decryption (runtime)
    │   ├── Environment detection setup
    │   └── Event listener registration
    │
    ├── Initial sensor data collection (passive)
    │   ├── Browser fingerprint
    │   ├── Hardware signals
    │   ├── Canvas/WebGL fingerprint
    │   └── JavaScript environment checks
    │
    ├── Sensor data POST (automatic)
    │   ├── Endpoint: /_sec/cp_challenge/verify
    │   ├── Payload: encoded sensor string
    │   └── Server validates and responds
    │
    ├── Cookie set: _abck (valid session token)
    │   └── Contains encoded validation result
    │
    └── Subsequent requests carry _abck cookie
        ├── Valid → Request proceeds normally
        └── Invalid/Missing → Challenge or block
```

## Cookie Lifecycle

### `bm_sz` Cookie
- Set on first visit
- Contains initial session identifier
- Used to correlate sensor data submissions

### `_abck` Cookie
- Primary validation cookie
- Updated after each sensor data submission
- Contains encoded challenge/validation state
- Must be present and valid for protected endpoints

### Cookie Chain
```
Visit → bm_sz set → Sensor POST → _abck updated → Protected request with _abck
```

## Sensor Data Submission

The sensor data is a long encoded string containing all collected signals. Key characteristics:

1. **Encoding:** Custom encoding scheme, not standard base64
2. **Structure:** Pipe-delimited sections with comma-separated values
3. **Dynamic:** The encoding changes between script versions
4. **Checksum:** Includes integrity check to detect tampering

## Server-Side Validation

The server performs several checks on the sensor data:

1. **Format validation** — Is the sensor data properly formatted?
2. **Signal consistency** — Do the signals match expected patterns for the claimed browser?
3. **Timing validation** — Are the timing values realistic?
4. **Historical correlation** — Does this session's data match previous submissions?
5. **TLS fingerprint** — Does the TLS handshake match the claimed browser?

## Detection Levels

| Level | Response |
|-------|----------|
| Trusted | Request proceeds, _abck is valid long-term |
| Suspicious | Additional sensor data collection required |
| Challenged | JavaScript challenge page served |
| Blocked | Request denied (403 or custom error page) |
