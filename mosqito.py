#!/usr/bin/env python3

import argparse
import itertools
import idna
from typing import List, Dict


# ASCII BANNER

def print_banner():
    banner = r"""
              \  /
               \/
        ==>>== () ==<<==
               /\
              /  \

        M O S Q I T O
   Domain Masquerading Analyzer
    """
    print(banner)

# HOMOGLYPH DEFINITIONS

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
    "z": ["ᴢ", "ż"]
}


# CORE LOGIC

def enrich_char(c: str) -> List[str]:
    """Return all visual variants for a character."""
    return [c] + HOMOGLYPHS.get(c.lower(), [])


def generate_variants(label: str, max_changes: int) -> set:
    """Generate domain label variants with controlled substitutions."""
    pools = [enrich_char(c) for c in label]
    results = set()

    for combo in itertools.product(*pools):
        diff = sum(1 for i in range(len(label)) if combo[i] != label[i])
        if 0 < diff <= max_changes:
            results.add("".join(combo))

    return results


def risk_score(original: str, variant: str) -> int:
    """Heuristic risk score based on visual deception."""
    score = 0
    for o, v in zip(original, variant):
        if o != v:
            if ord(v) > 127:
                score += 3
            elif v.isdigit():
                score += 2
            else:
                score += 1
    return score


def to_punycode(domain: str) -> str:
    """Convert Unicode domain to Punycode (IDNA)."""
    try:
        return idna.encode(domain).decode()
    except idna.IDNAError:
        return None

# MAIN ENTRY POINT

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Mosqito: Advanced Unicode domain masquerading generator (defensive)"
    )

    parser.add_argument(
        "domain",
        help="Target domain (e.g., google.com)"
    )

    parser.add_argument(
        "-m", "--max-changes",
        type=int,
        default=2,
        help="Maximum homoglyph substitutions per label (default: 2)"
    )

    parser.add_argument(
        "--punycode",
        action="store_true",
        help="Include Punycode (IDNA) output"
    )

    args = parser.parse_args()

    try:
        label, tld = args.domain.split(".", 1)
    except ValueError:
        raise SystemExit("Error: Invalid domain format (expected: label.tld)")

    variants = generate_variants(label, args.max_changes)
    sorted_variants = sorted(
        variants,
        key=lambda x: risk_score(label, x),
        reverse=True
    )

    print(f"Original: {args.domain}")
    print(f"Generated variants: {len(sorted_variants)}\n")

    for v in sorted_variants:
        domain = f"{v}.{tld}"
        score = risk_score(label, v)

        print(f"{domain}  [risk={score}]")

        if args.punycode:
            pc = to_punycode(domain)
            if pc:
                print(f"  -> {pc}")


if __name__ == "__main__":
    main()
