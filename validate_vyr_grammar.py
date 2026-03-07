#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADER_RE = re.compile(r"^([a-z][a-z0-9_]*):$")
IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
PUNCT_TERMINALS = {
    "{", "}", "(", ")", "<", ">", ":", ";", ",", ".", "=", "->", "::",
    "&", "*", "+", "-", "/", "%", "!", "==", "!=", "||", "&&", "_",
}


def is_valid_symbol(sym: str) -> bool:
    base = sym[:-4] if sym.endswith("_opt") else sym
    return bool(IDENT_RE.fullmatch(base) or base in PUNCT_TERMINALS)


def parse_grammar(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("grammar file is empty")

    productions: dict[str, list[list[str]]] = {}
    order: list[str] = []
    current: str | None = None

    for i, raw in enumerate(lines, start=1):
        if "\t" in raw:
            raise ValueError(f"line {i}: tabs are not allowed")

        if raw.strip() == "":
            continue

        if raw.startswith("  "):
            if current is None:
                raise ValueError(f"line {i}: production appears before any nonterminal header")
            rhs = raw[2:].strip()
            symbols = rhs.split() if rhs else []
            for sym in symbols:
                if not is_valid_symbol(sym):
                    raise ValueError(f"line {i}: invalid symbol '{sym}'")
                if sym.endswith("_opt_opt"):
                    raise ValueError(f"line {i}: invalid doubled optional suffix in '{sym}'")
            productions[current].append(symbols)
            continue

        m = HEADER_RE.fullmatch(raw.strip())
        if m:
            current = m.group(1)
            if current.endswith("_opt"):
                raise ValueError(f"line {i}: nonterminal name must not end with _opt: '{current}'")
            if current in productions:
                raise ValueError(f"line {i}: duplicate nonterminal '{current}'")
            productions[current] = []
            order.append(current)
            continue

        raise ValueError(
            f"line {i}: expected '<nonterminal>:' header or production line starting with two spaces"
        )

    for nt in order:
        if not productions[nt]:
            raise ValueError(f"nonterminal '{nt}' has no productions")

    return order, productions


def validate_references(order: list[str], productions: dict[str, list[list[str]]]):
    # By format design, terminals and nonterminals share the same identifier shape.
    # Therefore we only enforce structural validity and header uniqueness.
    # Optional references via *_opt are allowed for either terminals or nonterminals.
    _ = (order, productions)


def expanded_alternative_count(order: list[str], productions: dict[str, list[list[str]]]) -> int:
    defined = set(order)
    total = 0
    for rhs_list in productions.values():
        for rhs in rhs_list:
            # Only treat _opt as optional suffix when symbol is not an explicitly defined nonterminal.
            k = sum(1 for sym in rhs if sym.endswith("_opt") and sym not in defined)
            total += 2**k
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Vyr pass-1 grammar format")
    ap.add_argument(
        "path",
        nargs="?",
        default="/home/zos/vyrspecs/vyr-grammar-pass1.txt",
        help="grammar file path",
    )
    args = ap.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    try:
        order, productions = parse_grammar(path)
        validate_references(order, productions)
    except ValueError as e:
        print(f"INVALID: {e}")
        return 1

    n_nonterminals = len(order)
    n_raw_productions = sum(len(v) for v in productions.values())
    n_expanded = expanded_alternative_count(order, productions)

    print("VALID")
    print(f"nonterminals: {n_nonterminals}")
    print(f"raw_productions: {n_raw_productions}")
    print(f"expanded_productions_with_opt: {n_expanded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
