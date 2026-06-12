import os
import sys
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
    
    # Matches @type{key, ...
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
    missing_citations = []
    total_cites = 0
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                # Ignore comments
                if line.strip().startswith('%'):
                    continue
                matches = cite_pattern.findall(line)
                for key_group in matches:
                    # Citations can be comma-separated: \cite{key1,key2}
                    for key in key_group.split(','):
                        key = key.strip()
                        total_cites += 1
                        if key not in bib_keys:
                            missing_citations.append((line_no, key))
        
        if missing_citations:
            print(f"[-] LaTeX check: Found {len(missing_citations)} missing citations in {tex_path}:")
            for line_no, key in missing_citations:
                print(f"    Line {line_no}: Citation key '{key}' not found in references.bib")
            return False
        else:
            print(f"[+] LaTeX check: All {total_cites} citations in {tex_path} are resolved in references.bib.")
            return True
    except Exception as e:
        print(f"[-] LaTeX check: Failed to read {tex_path}: {e}")
        return False

def check_latex_environments(tex_path):
    r"""Checks for matching \begin{env} and \end{env} tags in the LaTeX file."""
    if not os.path.exists(tex_path):
        return False
    
    begin_pattern = re.compile(r'\\begin\{([^}]+)\}')
    end_pattern = re.compile(r'\\end\{([^}]+)\}')
    stack = []
    errors = 0
    
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                if line.strip().startswith('%'):
                    continue
                
                # Check begins
                for env in begin_pattern.findall(line):
                    stack.append((line_no, env))
                
                # Check ends
                for env in end_pattern.findall(line):
                    if not stack:
                        print(f"[-] LaTeX check: Line {line_no} has \\end{{{env}}} without matching \\begin.")
                        errors += 1
                    else:
                        last_line, last_env = stack.pop()
                        if last_env != env:
                            print(f"[-] LaTeX check: Line {line_no} has \\end{{{env}}} matching \\begin{{{last_env}}} on line {last_line}.")
                            errors += 1
        
        while stack:
            line_no, env = stack.pop()
            print(f"[-] LaTeX check: Unclosed \\begin{{{env}}} on line {line_no}")
            errors += 1
            
        if errors == 0:
            print(f"[+] LaTeX check: All LaTeX environments are properly balanced.")
            return True
        else:
            print(f"[-] LaTeX check: Found {errors} environment mismatches.")
            return False
    except Exception as e:
        print(f"[-] LaTeX check: Failed to verify environments: {e}")
        return False

def check_assets():
    """Checks if all required graphics assets exist."""
    required_assets = [
        "figures/soc_control_room.png",
        "figures/anomalies_over_time.pdf",
        "figures/performance_plot.pdf"
    ]
    all_exist = True
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"[+] Asset check: Found {asset}.")
        else:
            print(f"[-] Asset check: Missing {asset}.")
            all_exist = False
    return all_exist

def main():
    print("=" * 60)
    print("      AUTOMATED PROJECT QUALITY & COMPLIANCE CHECKER")
    print("=" * 60)
    
    success = True
    
    # 1. Check Python files
    print("\n--- 1. Python Code Quality Check ---")
    python_files = [
        "agent_system.py",
        "scripts/generate_graph.py",
        "scripts/generate_graph_anomalies.py"
    ]
    for py_file in python_files:
        if not check_python_syntax(py_file):
            success = False
            
    # 2. Check LaTeX syntax & citations
    print("\n--- 2. LaTeX Source Check ---")
    bib_keys = get_bib_keys("references.bib")
    if not check_latex_citations("main.tex", bib_keys):
        success = False
    if not check_latex_environments("main.tex"):
        success = False
        
    # 3. Check Assets
    print("\n--- 3. Asset Verification ---")
    if not check_assets():
        success = False
        
    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: All quality and compliance checks passed!")
        sys.exit(0)
    else:
        print("FAILURE: Code quality or document consistency errors found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
