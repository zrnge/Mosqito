# Mosqito – Domain Masquerading & Homoglyph Generator 🦟

![Mosqito Logo](mosqito_logo.png)

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

