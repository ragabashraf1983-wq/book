import os
from pathlib import Path
from typing import List, Optional

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def write_text_file(path: Path, content: str):
    ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def list_markdown_files(path: Path) -> List[Path]:
    if not path.exists():
        return []
    return list(path.glob("*.md"))

def copy_file(src: Path, dst: Path):
    ensure_dir(dst.parent)
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())
