#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mosqito - Unicode Homoglyph Domain Masquerading Analyzer
Author: https://github.com/zrnge
License: MIT
Purpose: Defensive detection of Unicode-based domain impersonation
"""

import argparse
import itertools
import sys
import unicodedata
from typing import Dict, List

# ASCII Banner

BANNER = r"""
 _______  _______  _______  _______ __________________ _______ 
(       )(  ___  )(  ____ \(  ___  )\__   __/\__   __/(  ___  )
| () () || (   ) || (    \/| (   ) |   ) (      ) (   | (   ) |
| || || || |   | || (_____ | |   | |   | |      | |   | |   | |
| |(_)| || |   | |(_____  )| |   | |   | |      | |   | |   | |
| |   | || |   | |      ) || | /\| |   | |      | |   | |   | |
| )   ( || (___) |/\____) || (_\ \ |___) (___   | |   | (___) |
|/     \|(_______)\_______)(____\/_)\_______/   )_(   (_______)
                                                               

 Mosqito - Domain Masquerading Analyzer
"""


# Terminal Colors

class Color:
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    RESET = "\033[0m"

def colorize(text: str, suspicious: bool) -> str:
    if suspicious:
        return f"{Color.ORANGE}{text}{Color.RESET}"
    return f"{Color.GREEN}{text}{Color.RESET}"


# Enriched Homoglyph Mapping

HOMOGLYPHS: Dict[str, List[str]] = {
    "a": ["а", "ɑ", "α", "à", "á", "â", "ä", "ã", "å"],
    "b": ["Ь", "ʙ"],
    "c": ["с", "ϲ", "ç"],
    "d": ["ԁ", "ɗ"],
    "e": ["е", "ε", "ē", "ė", "ë", "ê", "é"],
    "g": ["ɡ", "ɢ"],
    "h": ["һ", "ḥ"],
    "i": ["і", "ı", "ɩ", "í", "ï"],
    "j": ["ј"],
    "k": ["κ", "к"],
    "l": ["ⅼ", "ӏ", "1", "|"],
    "m": ["ｍ", "ṃ"],
    "n": ["ո", "ń"],
    "o": ["ο", "о", "օ", "0", "ö", "ó", "ò", "ô"],
    "p": ["р", "ρ"],
    "q": ["ԛ"],
    "r": ["г", "ṛ"],
    "s": ["ѕ", "ʂ"],
    "t": ["τ", "т"],
    "u": ["υ", "ս", "ü", "ú"],
    "v": ["ѵ", "ν"],
    "w": ["ѡ"],
    "x": ["х", "χ"],
    "y": ["у", "γ"],
    "z": ["ᴢ", "ż"],
}

REVERSE_HOMOGLYPHS = {
    glyph: ascii_char
    for ascii_char, glyphs in HOMOGLYPHS.items()
    for glyph in glyphs
}

# -----------------------------
# Utility Functions
# -----------------------------
def is_ascii(s: str) -> bool:
    return all(ord(c) < 128 for c in s)

def to_punycode(domain: str):
    try:
        return domain.encode("idna").decode()
    except Exception:
        return None

def normalize_visual(domain: str) -> str:
    return "".join(REVERSE_HOMOGLYPHS.get(c, c) for c in domain)

def calculate_risk(domain: str) -> int:
    score = 0
    for c in domain:
        if ord(c) > 127:
            score += 3
        if c in {"0", "1", "|"}:
            score += 2
        if c in REVERSE_HOMOGLYPHS:
            score += 3
    return score


# Variant Generation

def generate_variants(label: str, max_changes: int):
    positions = [
        (i, HOMOGLYPHS[c])
        for i, c in enumerate(label)
        if c in HOMOGLYPHS
    ]

    variants = set()

    for r in range(1, max_changes + 1):
        for combo in itertools.combinations(positions, r):
            indexes, replacements = zip(*combo)
            for product in itertools.product(*replacements):
                chars = list(label)
                for idx, rep in zip(indexes, product):
                    chars[idx] = rep
                variants.add("".join(chars))

    return variants


# Masquerade Detection

def check_domain(domain: str, compare: str = None):
    findings = []
    risk = 0

    if not is_ascii(domain):
        findings.append("Contains non-ASCII Unicode characters")
        risk += 3

    normalized = unicodedata.normalize("NFKC", domain)
    if normalized != domain:
        findings.append("Unicode normalization alters the domain")
        risk += 2

    visual = normalize_visual(domain)
    if visual != domain:
        findings.append(f"Visually resolves to: {visual}")
        risk += 4

    puny = to_punycode(domain)
    if puny and puny.startswith("xn--"):
        findings.append(f"IDN punycode detected: {puny}")
        risk += 2

    if compare and visual == compare:
        findings.append(f"Visually impersonates: {compare}")
        risk += 4

    status = "SUSPICIOUS" if risk >= 5 else "CLEAN"

    return {
        "domain": domain,
        "status": status,
        "risk": risk,
        "findings": findings,
    }


# CLI

def main():
    parser = argparse.ArgumentParser(
        description="Mosqito - Unicode Homoglyph Domain Masquerading Analyzer"
    )

    parser.add_argument("domain", nargs="?", help="Target domain (e.g. google.com)")
    parser.add_argument("-m", "--max-changes", type=int, default=2)
    parser.add_argument("--punycode", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--compare", help="Legitimate domain to compare against")

    args = parser.parse_args()

    if not args.domain:
        parser.print_help()
        sys.exit(1)

    print(BANNER)

    
    # Detection Mode
    
    if args.check:
        result = check_domain(args.domain, args.compare)
        suspicious = result["status"] == "SUSPICIOUS"

        print(f"Domain: {result['domain']}")
        print(f"Status: {colorize(result['status'], suspicious)}")
        print(f"Risk Score: {result['risk']}/10\n")

        if result["findings"]:
            print("Findings:")
            for f in result["findings"]:
                print(f"- {f}")
        else:
            print("No suspicious indicators detected.")
        return

    
    # Generation Mode
   
    try:
        label, tld = args.domain.split(".", 1)
    except ValueError:
        print("Error: Invalid domain format (expected: label.tld)")
        sys.exit(1)

    variants = generate_variants(label, args.max_changes)

    for v in sorted(variants):
        full = f"{v}.{tld}"
        risk = calculate_risk(full)
        suspicious = risk >= 5

        line = f"{full}  [risk={risk}]"
        print(colorize(line, suspicious))

        if args.punycode:
            puny = to_punycode(full)
            if puny and puny != full:
                print(f"  -> {puny}")

if __name__ == "__main__":
    main()
