import json
from pathlib import Path
from typing import Dict, Any, Optional
from .files import read_text_file, write_text_file

class ProjectState:
    def __init__(self, project: 'Project'):
        self.project = project
        self.devstate_path = project.get_dir("project") / "DEVSTATE.md"
        self.resume_path = project.get_dir("project") / "RESUME_STATE.json"

    def load_resume_state(self) -> Dict[str, Any]:
        if not self.resume_path.exists():
            return {}
        try:
            with open(self.resume_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_resume_state(self, state: Dict[str, Any]):
        with open(self.resume_path, 'w') as f:
            json.dump(state, f, indent=2)

    def update_devstate(self, content: str):
        write_text_file(self.devstate_path, content)

    def get_devstate(self) -> str:
        return read_text_file(self.devstate_path)

    def generate_devstate_markdown(self, data: Dict[str, Any]) -> str:
        # Helper to convert state dictionary to the mandatory DEVSTATE.md format
        lines = [
            f"# DEVSTATE: {data.get('project_title', 'Unknown')}",
            f"\n**Current Phase:** {data.get('current_phase', 'N/A')}",
            f"**Completed Phases:** {', '.join(data.get('completed_phases', []))}",
            f"**Current Task:** {data.get('current_task', 'N/A')}",
            f"**Next Task:** {data.get('next_task', 'N/A')}",
            f"\n### Source Files Loaded\n{data.get('sources_loaded', 'None')}",
            f"\n### Agents Created\n{data.get('agents_created', 'None')}",
            f"\n### Model Used\n{data.get('model_used', 'N/A')}",
            f"\n### Chapter Status\n{data.get('chapter_status', 'None')}",
            f"\n### Last Checkpoint\n{data.get('last_checkpoint', 'N/A')}",
            f"\n### Unresolved Issues\n{data.get('unresolved_issues', 'None')}",
            f"\n### Failed Tasks\n{data.get('failed_tasks', 'None')}",
            f"\n### Resume Instructions\n{data.get('resume_instructions', 'N/A')}"
        ]
        return "\n".join(lines)
