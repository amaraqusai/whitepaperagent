"""
Entry Point for Whitepaper Agent
=================================
This wrapper delegates all commands to the CLI in the src/ directory.
"""

import sys
from pathlib import Path

# Add src to the Python path
src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    from src.cli import build_parser, DISPATCH, _banner
    
    _banner()
    parser = build_parser()
    args = parser.parse_args()
    DISPATCH[args.command](args)
