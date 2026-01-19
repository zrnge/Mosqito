# Mosqito 🦟
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/use-defensive%20security-orange.svg)
![Static Badge](https://img.shields.io/badge/Mosqito-1.2-orange)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

<img src="mosqito_logo.png" alt="drawing" style="width:400px; place-items: center;"/>

**Mosqito is a defensive cybersecurity tool for detecting Unicode homoglyph and IDN-based domain impersonation and phishing risks.**

---

## Overview

Unicode homoglyphs are frequently abused in phishing and brand impersonation attacks by replacing ASCII characters with visually similar Unicode characters.

Mosqito helps security professionals:
- Detect Unicode-based domain masquerading
- Generate potential homoglyph impersonation variants
- Analyze suspicious domains during SOC triage
- Understand IDN and Punycode abuse techniques

Mosqito is designed **strictly for defensive security research, detection engineering, and education**.

---

## Features

- Unicode homoglyph domain variant generation
- Masquerade detection for single domains
- Visual normalization and impersonation detection
- Risk scoring for prioritization
- IDN / Punycode identification
- Colorized terminal output
  - 🟢 Green: clean / low risk
  - 🟠 Orange: suspicious / malicious-looking
- Single-file, dependency-free Python tool

---

## Installation

Clone the repository:

```bash
git clone https://github.com/zrnge/Mosqito.git
cd Mosqito
```
---
Mosqito requires Python 3.9 or higher.
No additional dependencies are required.
---
# Usage
## General Syntax
```bash
python mosqito.py <domain> [options]
```
---

## Options
| Option                    | Description                                                | Default  |
| ------------------------- | ---------------------------------------------------------- | -------- |
| `-m, --max-changes <int>` | Maximum homoglyph substitutions per label                  | `2`      |
| `--punycode`              | Display IDNA / Punycode representation                     | Disabled |
| `--check`                 | Analyze a domain for masquerading indicators               | Disabled |
| `--compare <domain>`      | Legitimate domain to compare against (used with `--check`) | None     |

---
## Examples
### Generate Homoglyph Variants
```bash
python mosqito.py google.com
```
Generates visually similar Unicode-based variants of google.com.
---
### Limit Substitutions (Higher Realism)
```bash
python mosqito.py google.com --max-changes 1
```
Restricts output to the most realistic impersonation domains.
---
### Show Punycode Representation
```bash
python mosqito.py google.com --punycode
```
Displays the IDN / ASCII-compatible encoding used by DNS and browsers.
---
### Masquerade Detection Mode
```bash
python mosqito.py --check gοοgle.com
```
Check whether a domain is likely impersonating another.
---

### Compare Against a Legitimate Domain
```bash
python mosqito.py --check gοοgle.com --compare google.com
```
This flags high-confidence visual impersonation.

# Disclaimer

Mosqito is intended **solely for defensive cybersecurity research, education, and detection engineering**.

It must **not** be used for phishing, impersonation, fraud, or any malicious activity.
The authors assume no responsibility for misuse of this tool.

Use responsibly and in compliance with applicable laws and policies.

