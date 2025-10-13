# src/parser.py

from typing import List, Tuple, Optional


def parse_command(line: str) -> Optional[Tuple[str, List[str]]]:
    """
    Return (COMMAND, args) or None for blank/comment-only lines.
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    parts = s.split()
    cmd, args = parts[0], parts[1:]
    cmd = cmd.upper()
    return cmd, args