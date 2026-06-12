"""
Quality & Compliance Checker Functions
=======================================
Reusable checker functions for validating Python syntax,
LaTeX citation integrity, environment balance, and asset existence.
"""

import os
import re
import ast


def check_python_syntax(filepath):
    """Checks if a Python file has valid syntax."""
    if not os.path.exists(filepath):
        print(f"[-] Python check: {filepath} does not exist.")
        return False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f"[+] Python check: {filepath} syntax is valid.")
        return True
    except SyntaxError as e:
        print(f"[-] Python check: {filepath} has syntax error: {e}")
        return False
    except Exception as e:
        print(f"[-] Python check: Failed to read {filepath}: {e}")
        return False


def get_bib_keys(bib_path):
    """Extracts all citation keys from a .bib file."""
    keys = set()
    if not os.path.exists(bib_path):
        print(f"[-] BibTeX check: {bib_path} does not exist.")
        return keys
    entry_pattern = re.compile(r'@\w+\s*\{\s*([^,\s]+)\s*,')
    try:
        with open(bib_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = entry_pattern.match(line.strip())
                if match:
                    keys.add(match.group(1))
        print(f"[+] BibTeX check: Loaded {len(keys)} citation keys from {bib_path}.")
        return keys
    except Exception as e:
        print(f"[-] BibTeX check: Failed to parse {bib_path}: {e}")
        return keys


def check_latex_citations(tex_path, bib_keys):
    r"""Verifies that all \cite{} keys in the .tex file exist in the .bib file."""
    if not os.path.exists(tex_path):
        print(f"[-] LaTeX check: {tex_path} does not exist.")
        return False
    cite_pattern = re.compile(r'\\cite\{([^}]+)\}')
    missing = []
    total = 0
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                if line.strip().startswith('%'):
                    continue
                for key_group in cite_pattern.findall(line):
                    for key in key_group.split(','):
                        key = key.strip()
                        total += 1
                        if key not in bib_keys:
                            missing.append((line_no, key))
        if missing:
            print(f"[-] LaTeX check: {len(missing)} missing citations in {tex_path}:")
            for ln, k in missing:
                print(f"    Line {ln}: '{k}' not in references.bib")
            return False
        print(f"[+] LaTeX check: All {total} citations resolved.")
        return True
    except Exception as e:
        print(f"[-] LaTeX check: Failed to read {tex_path}: {e}")
        return False


def check_latex_environments(tex_path):
    r"""Checks for matching \begin{env} and \end{env} tags."""
    if not os.path.exists(tex_path):
        return False
    begin_pat = re.compile(r'\\begin\{([^}]+)\}')
    end_pat = re.compile(r'\\end\{([^}]+)\}')
    stack = []
    errors = 0
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                if line.strip().startswith('%'):
                    continue
                for env in begin_pat.findall(line):
                    stack.append((line_no, env))
                for env in end_pat.findall(line):
                    if not stack:
                        print(f"[-] Unmatched \\end{{{env}}} at line {line_no}")
                        errors += 1
                    else:
                        ln, last = stack.pop()
                        if last != env:
                            print(f"[-] \\end{{{env}}} at line {line_no} vs \\begin{{{last}}} at line {ln}")
                            errors += 1
        while stack:
            ln, env = stack.pop()
            print(f"[-] Unclosed \\begin{{{env}}} at line {ln}")
            errors += 1
        if errors == 0:
            print("[+] LaTeX check: All environments balanced.")
            return True
        print(f"[-] LaTeX check: {errors} environment mismatches.")
        return False
    except Exception as e:
        print(f"[-] LaTeX check: Failed to verify environments: {e}")
        return False


def check_assets(asset_list):
    """Checks if all required graphics assets exist."""
    ok = True
    for asset in asset_list:
        if os.path.exists(asset):
            print(f"[+] Asset check: Found {asset}.")
        else:
            print(f"[-] Asset check: Missing {asset}.")
            ok = False
    return ok
