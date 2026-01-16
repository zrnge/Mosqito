# Mosqito – Domain Masquerading & Homoglyph Generator 🦟

<img src="mosqito_logo.png" alt="drawing" style="width:200px;"/>

Mosqito is a cybersecurity research and defensive tool designed to generate visually confusable domain variants. It helps security teams, threat analysts, and SOC engineers detect potential phishing, impersonation, and brand abuse attempts by enumerating domains that exploit Unicode homoglyphs, diacritics, and digit-letter substitutions.

---

## Overview

**Mosqito** is a Unicode-aware domain masquerading generator designed for:

- **Cybersecurity research**
- **Threat modeling**
- **Defensive detection engineering**
- **SOC & DFIR teams**

It generates **visually confusable domain variants** using real-world homoglyphs, diacritics, and digit lookalikes.

---

## Why This Tool Exists

Phishing campaigns exploit:

- Unicode homoglyphs across scripts (Latin, Cyrillic, Greek, Armenian)
- Diacritic abuse (`o` → `ó`, `ö`)
- Digit–letter confusion (`l` ↔ `1`, `o` ↔ `0`)
- Mixed-script domains
- IDNA / Punycode

**Mosqito** enumerates plausible masquerades for proactive detection and training.

---

## Features

- Unicode homoglyph substitution
- Diacritic enrichment
- Digit–letter confusion
- Controlled substitution depth
- Risk scoring per variant
- Punycode conversion
- Deterministic, auditable output

---

## Installation

### Requirements

- Python 3.9+
- `idna` library

```bash
pip install idna
```
### Usage
| Argument | Required | Description                                                                       |
| -------- | -------- | --------------------------------------------------------------------------------- |
|  domain  |   Yes    | Target domain to analyze. Must be in the format `label.tld` (e.g., `google.com`). |

| Option     | Long Form             | Description                                                                                                              | Default  |
| ---------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------- |
| `-m <int>` | `--max-changes <int>` | Maximum number of character substitutions allowed per domain label. Limits combinatorial explosion and controls realism. | `2`      |
| *(none)*   | `--punycode`          | Display the IDNA / Punycode representation for each generated domain variant.                                            | Disabled |

```bash
--max-changes 1   # Very strict, high realism
--max-changes 2   # Balanced (default)
--max-changes 3   # Broad coverage (use with caution)
```
```bash
--punycode
```
When enabled, Mosqito outputs the ASCII-compatible encoding
used by DNS and browsers for Unicode domains.

Example:
``
gοοgle.com
  -> xn--ggle-55da.com
``

This is useful for:

- DNS monitoring
- Certificate Transparency analysis
- Browser behavior validation

### Basic Execution

Generate all plausible masquerading variants using default settings:
```bash
python mosqito.py google.com
```

### Restrict to One Character Change

Generate only the most realistic impersonation domains:
```bash
python mosqito.py google.com --max-changes 1
```

### Include Punycode Output

Generate variants and show their DNS-compatible encodings:
```bash
python mosqito.py google.com --punycode
```

Combine Options
```bash
python mosqito.py google.com --max-changes 1 --punycode
```

---

## Disclaimer

Mosqito is intended **solely for defensive cybersecurity research, education, and detection engineering**.

It must **not** be used for phishing, impersonation, fraud, or any malicious activity.
The authors assume no responsibility for misuse of this tool.

Use responsibly and in compliance with applicable laws and policies.

