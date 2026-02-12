# Akamai Sensor Data Structure (Sanitized)

## Overview

The sensor data payload is a long string sent via POST to `/_sec/cp_challenge/verify`. It contains all collected browser signals encoded in a custom format.

## General Structure

```
{version}|{device_data}|{browser_data}|{behavior_data}|{timing_data}|{checksum}
```

Each section is pipe-delimited (`|`), and values within sections are comma-separated.

## Section Breakdown

### Version Section
- Sensor script version identifier
- API key / site identifier

### Device Data
- Screen dimensions (`width,height,availWidth,availHeight`)
- Color depth and pixel depth
- Device memory and CPU cores
- Touch support flag

### Browser Data
- User-Agent hash
- Plugin count and list hash
- Language and timezone
- Canvas fingerprint hash
- WebGL renderer hash
- Automation detection flags

### Behavior Data
- Mouse event count and coordinate samples
- Keyboard event count
- Scroll event count
- Touch event count
- Focus/blur event count

### Timing Data
- Navigation timing entries
- Script execution duration
- DOM ready timestamp
- First paint timestamp

### Checksum
- Integrity check covering all previous sections
- Prevents modification of individual values

## Size

A typical sensor data payload is 2,000-5,000 characters, depending on the amount of behavioral data collected.

## Notes

- The exact format varies between Akamai deployments
- The encoding scheme is not publicly documented
- Field positions may shift between script versions
- This document describes the general pattern, not exact byte offsets
