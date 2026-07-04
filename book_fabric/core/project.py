from pathlib import Path
from typing import Dict, Any
from .files import ensure_dir, write_text_file

class Project:
    def __init__(self, project_name: str, base_dir: Path = Path("projects")):
        self.project_name = project_name
        self.root = base_dir / project_name
        self.dirs = {
            "project": self.root / "00_Project",
            "sources": self.root / "10_Sources",
            "analysis": self.root / "20_Analysis",
            "planning": self.root / "30_Planning",
            "chapters": self.root / "40_Chapters",
            "reviews": self.root / "50_Reviews",
            "appendices": self.root / "60_Appendices",
            "final": self.root / "70_Final",
            "archive": self.root / "99_Archive",
        }

    def create(self):
        for path in self.dirs.values():
            ensure_dir(path)
        
        # Create mandatory project files
        self.write_project_file("DEVSTATE.md", "# DEVSTATE\nProject: " + self.project_name)
        self.write_project_file("MASTER_TOC.md", "# Master Table of Contents")
        self.write_project_file("ROADMAP.md", "# Roadmap")
        self.write_project_file("CHANGELOG.md", "# Changelog")
        self.write_project_file("STYLE_GUIDE.md", "# Style Guide")
        self.write_project_file("SOURCE_POLICY.md", "# Source Use Policy")
        self.write_project_file("QUALITY_CHECKLIST.md", "# Quality Checklist")
        self.write_project_file("AGENT_ROSTER.md", "# Agent Roster")
        self.write_project_file("MODEL_POLICY.md", "# Model Policy")

    def write_project_file(self, filename: str, content: str):
        write_text_file(self.dirs["project"] / filename, content)

    def get_dir(self, key: str) -> Path:
        return self.dirs[key]

    def exists(self) -> bool:
        return self.root.exists()
