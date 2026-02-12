# Akamai Bot Manager v2 — Signal Categories

## Overview

Akamai Bot Manager v2 collects **100+ signals** from the browser environment, organized into the following categories. These signals are encoded into sensor data and sent to the server for validation.

## 1. Browser Fingerprint Signals

| Signal | What it checks |
|--------|---------------|
| User-Agent string | Browser and OS identification |
| Navigator properties | `appName`, `appVersion`, `platform`, `vendor` |
| Plugin enumeration | Installed browser plugins and MIME types |
| Screen properties | `width`, `height`, `availWidth`, `availHeight`, `colorDepth`, `pixelDepth` |
| Timezone offset | `Date.getTimezoneOffset()` |
| Language settings | `navigator.language`, `navigator.languages` |
| Cookie support | `navigator.cookieEnabled` |
| Do Not Track | `navigator.doNotTrack` |

## 2. Hardware Signals

| Signal | What it checks |
|--------|---------------|
| Device memory | `navigator.deviceMemory` |
| Hardware concurrency | `navigator.hardwareConcurrency` (CPU cores) |
| WebGL renderer | GPU model via `WEBGL_debug_renderer_info` |
| WebGL vendor | GPU vendor string |
| Touch support | `maxTouchPoints`, touch event listeners |
| Battery API | Charging status, level (where available) |

## 3. Canvas Fingerprinting

Akamai renders specific text strings and gradients to a hidden canvas element, then hashes the pixel data. Different GPU/driver/OS combinations produce unique hashes, making this a strong fingerprint signal.

## 4. Behavioral Signals

| Signal | What it checks |
|--------|---------------|
| Mouse movements | Coordinates, velocity, acceleration patterns |
| Click events | Position, timing, frequency |
| Keyboard events | Key codes, timing between keystrokes |
| Scroll events | Direction, speed, patterns |
| Touch events | Touch points, gestures (mobile) |
| Focus/blur | Tab switching, window focus changes |

## 5. Timing Signals

| Signal | What it checks |
|--------|---------------|
| Navigation timing | `performance.timing` entries |
| Resource timing | Script load times |
| First paint | `performance.getEntriesByType('paint')` |
| Script execution time | How long the sensor script takes to execute |
| DOM ready timing | Time from navigation start to DOM interactive |

## 6. JavaScript Environment

| Signal | What it checks |
|--------|---------------|
| Prototype integrity | Whether native prototypes have been modified |
| Function arity | `Function.prototype.toString` behavior |
| Error messages | Format of error messages (differs by engine) |
| Automation detection | `navigator.webdriver`, `__selenium_unwrapped` |
| Chrome DevTools | Detection of open developer tools |
| Headless indicators | `chrome.runtime`, `Permissions` API behavior |

## 7. Network Signals

| Signal | What it checks |
|--------|---------------|
| Connection type | `navigator.connection.type` |
| Effective type | `navigator.connection.effectiveType` |
| Round-trip time | `navigator.connection.rtt` |
| Downlink speed | `navigator.connection.downlink` |

## Notes

- Not all signals are collected on every page load; some are conditional
- The specific signals and their encoding change between Akamai deployments
- Server-side validation may weight certain signals more heavily than others
- TLS fingerprinting happens at the network layer, separate from JavaScript signals
