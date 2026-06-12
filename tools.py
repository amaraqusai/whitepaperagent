"""Custom CrewAI Tools for Whitepaper Pipeline."""

import os
import re
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ── Input Schemas ─────────────────────────────────────────────────────

class FileWriterInput(BaseModel):
    """Input schema for FileWriterTool."""

    filepath: str = Field(..., description="Destination file path.")
    content: str = Field(..., description="Text content to write.")


class FilePathInput(BaseModel):
    """Input schema for tools that accept a single file path."""

    filepath: str = Field(..., description="Path to the target file.")


class TextInput(BaseModel):
    """Input schema for tools that accept raw text."""

    text: str = Field(..., description="Text content to analyse.")


# ── Tool 1: FileWriterTool ────────────────────────────────────────────

class FileWriterTool(BaseTool):
    """Write text content to any file, creating directories as needed."""

    name: str = "file_writer"
    description: str = (
        "Writes content to a file path. Creates parent directories "
        "automatically. Returns confirmation or error message."
    )
    args_schema: Type[BaseModel] = FileWriterInput

    def _run(self, filepath: str, content: str) -> str:
        """Write *content* to *filepath* and return a status string."""
        try:
            dest = Path(filepath)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            return f"SUCCESS: wrote {len(content)} chars to {dest}"
        except OSError as exc:
            return f"ERROR: {exc}"


# ── Tool 2: LaTeXValidatorTool ────────────────────────────────────────

class LaTeXValidatorTool(BaseTool):
    r"""Validate balanced \\begin/\\end environments in a .tex file."""

    name: str = "latex_validator"
    description: str = (
        "Reads a .tex file and checks that every \\begin{env} has a "
        "matching \\end{env}. Returns a validation report."
    )
    args_schema: Type[BaseModel] = FilePathInput

    def _run(self, filepath: str) -> str:
        """Return a plain-text validation report."""
        if not os.path.isfile(filepath):
            return f"ERROR: {filepath} not found."
        begin_re = re.compile(r"\\begin\{([^}]+)\}")
        end_re = re.compile(r"\\end\{([^}]+)\}")
        stack: list[tuple[int, str]] = []
        errors: list[str] = []
        with open(filepath, "r", encoding="utf-8") as fh:
            for num, line in enumerate(fh, 1):
                if line.strip().startswith("%"):
                    continue
                for env in begin_re.findall(line):
                    stack.append((num, env))
                for env in end_re.findall(line):
                    if not stack:
                        errors.append(f"L{num}: unmatched \\end{{{env}}}")
                    else:
                        ln, top = stack.pop()
                        if top != env:
                            errors.append(
                                f"L{num}: \\end{{{env}}} vs "
                                f"\\begin{{{top}}} at L{ln}"
                            )
        while stack:
            ln, env = stack.pop()
            errors.append(f"L{ln}: unclosed \\begin{{{env}}}")
        if errors:
            return "FAIL – " + "; ".join(errors)
        return "PASS – all environments balanced."


# ── Tool 3: BibTeXLookupTool ─────────────────────────────────────────

class BibTeXLookupTool(BaseTool):
    """Look up citation keys and titles from a .bib file."""

    name: str = "bibtex_lookup"
    description: str = (
        "Reads a BibTeX .bib file and returns every citation key "
        "paired with its title field."
    )
    args_schema: Type[BaseModel] = FilePathInput

    def _run(self, filepath: str) -> str:
        """Parse *filepath* and return ``key: title`` lines."""
        if not os.path.isfile(filepath):
            return f"ERROR: {filepath} not found."
        entry_re = re.compile(r"@\w+\{([^,\s]+)\s*,")
        title_re = re.compile(r"title\s*=\s*\{(.+?)\}", re.IGNORECASE)
        entries: list[str] = []
        current_key: str | None = None
        with open(filepath, "r", encoding="utf-8") as fh:
            for line in fh:
                key_m = entry_re.match(line.strip())
                if key_m:
                    current_key = key_m.group(1)
                title_m = title_re.search(line)
                if title_m and current_key:
                    entries.append(f"{current_key}: {title_m.group(1)}")
                    current_key = None
        if not entries:
            return "No entries found."
        return f"Found {len(entries)} entries:\n" + "\n".join(entries)


# ── Tool 4: WordCountTool ────────────────────────────────────────────

class WordCountTool(BaseTool):
    """Count words in a block of text to estimate page length."""

    name: str = "word_counter"
    description: str = (
        "Counts words in the supplied text. Useful for estimating "
        "page length (~250 words per page)."
    )
    args_schema: Type[BaseModel] = TextInput

    def _run(self, text: str) -> str:
        """Return word count and estimated pages."""
        words = len(text.split())
        pages = round(words / 250, 1)
        return f"Words: {words} | Estimated pages (~250 w/p): {pages}"
