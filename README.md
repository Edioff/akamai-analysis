# Akamai Bot Manager v2 — Technical Analysis

![Security Research](https://img.shields.io/badge/Security-Research-red?style=flat-square)
![JavaScript](https://img.shields.io/badge/JavaScript-Reverse%20Engineering-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-Analysis%20Tools-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> Deep technical analysis of Akamai Bot Manager v2's detection mechanisms, based on reverse-engineering 512KB of obfuscated JavaScript and documenting the full bot detection pipeline.

## Overview

This repository contains a detailed case study of how Akamai Bot Manager v2 works under the hood. The analysis was conducted as part of a web scraping project targeting an e-commerce site protected by Akamai, and documents the complete bot detection pipeline from initial script loading to server-side validation.

**This is not a bypass tool.** It's a technical analysis documenting what Akamai collects, how it processes signals, and how it decides whether a visitor is human or automated. The goal is educational — understanding enterprise-grade bot detection helps build better security and better scrapers.

## The Challenge

The target site deployed Akamai Bot Manager v2, which is considered one of the most sophisticated bot detection systems in production. Key characteristics:

- **512KB of obfuscated JavaScript** loaded on every page
- **100+ browser signals** collected per session
- **Multi-layer validation** combining client-side and server-side checks
- **Dynamic script generation** — the detection script changes between deployments
- **Cookie-based challenge system** using `_abck` and `bm_sz` cookies

## My Approach

### Phase 1: JavaScript Deobfuscation
- Captured the Akamai sensor script (`akamai_sensor.js`)
- Deobfuscated string arrays, control flow flattening, and dead code
- Identified 200+ functions organized into detection modules

### Phase 2: Signal Mapping
- Documented every browser signal Akamai collects
- Categorized signals into groups: browser fingerprint, hardware, behavior, timing
- Mapped how signals are encoded into the sensor data payload

### Phase 3: Protocol Analysis
- Traced the full request flow from page load to validated session
- Documented the `_abck` cookie lifecycle
- Identified the sensor data POST endpoint and payload format
- Analyzed server-side validation responses

### Phase 4: Findings Documentation
- Compiled an 11-page technical report
- Created flow diagrams of the detection pipeline
- Documented the string decryption mechanism
- Catalogued the pixel tracking system

## Key Findings

### Signal Collection Categories

| Category | Signals | Examples |
|----------|---------|---------|
| Browser fingerprint | 20+ | User-Agent, plugins, screen resolution, color depth |
| Hardware | 10+ | Device memory, CPU cores, GPU renderer, touch support |
| Behavioral | 15+ | Mouse movements, keystrokes, scroll patterns, timing |
| JavaScript environment | 25+ | Prototype chains, function arity, error messages |
| Timing | 10+ | Navigation timing, paint timing, performance entries |
| Network | 5+ | Connection type, RTT, downlink speed |

### Detection Pipeline

```
Page Load
    |
    v
Akamai Script Loads (512KB obfuscated JS)
    |
    v
String Array Decryption (runtime decode of 500+ strings)
    |
    v
Signal Collection (100+ browser/device/behavior signals)
    |
    v
Sensor Data Generation (encoded payload with all signals)
    |
    v
POST to /_sec/cp_challenge/verify (sensor data submission)
    |
    v
Server Validates -> Sets _abck cookie
    |
    v
Subsequent requests carry _abck cookie for validation
```

### Interesting Technical Details

- **String obfuscation:** All strings are stored in a rotated array and decoded at runtime using a custom function with numeric offsets
- **Timing traps:** The script measures execution time of certain operations to detect if code is being debugged or running in a non-standard environment
- **Canvas fingerprinting:** Renders specific text and gradients to a canvas element and hashes the result
- **WebGL fingerprinting:** Queries GPU renderer and vendor strings via WebGL
- **Prototype poisoning detection:** Checks if native JavaScript prototypes have been modified

## Repository Contents

```
akamai-analysis/
├── README.md                           # This file
├── docs/
│   └── technical_report.pdf            # Full 11-page technical report
├── analysis/
│   ├── signal_categories.md            # Categorized list of all collected signals
│   ├── cookie_lifecycle.md             # _abck cookie flow documentation
│   └── detection_pipeline.md           # Step-by-step detection flow
└── examples/
    ├── string_decryption.py            # Generic example of Akamai's string obfuscation pattern
    └── sensor_structure.md             # Sensor data payload structure (sanitized)
```

## Scope & Ethics

- This analysis was performed on a **legitimate client engagement** for data extraction
- **No proprietary client code** is included in this repository
- All code examples are **generic patterns**, not site-specific implementations
- The goal is **educational**: understanding how bot detection works at an enterprise level
- This work demonstrates expertise in **JavaScript reverse engineering** and **security analysis**

## What I Learned

1. **Enterprise anti-bot is deep** — Akamai doesn't just check User-Agent. It validates 100+ signals across multiple layers.
2. **Obfuscation is not security** — With patience and the right tools, any client-side JavaScript can be understood.
3. **The arms race is real** — Detection scripts evolve constantly. Any bypass is temporary.
4. **TLS fingerprinting is the hardest barrier** — Server-side TLS validation is harder to bypass than any client-side JavaScript check.

## Related

- [oreillyauto-scraper](https://github.com/Edioff/oreillyauto-scraper) — The scraper built using insights from this analysis

## Author

**Johan Cruz** — Data Engineer & Web Scraping Specialist
- GitHub: [@Edioff](https://github.com/Edioff)
- Specializing in anti-bot bypass, web scraping at scale, and data engineering
- Available for freelance projects

## License

MIT
