from pathlib import Path
from book_fabric.core.project import Project
from book_fabric.core.files import copy_file

def run_phase0(project_name: str, source_files: list[Path], book_params: dict):
    project = Project(project_name)
    project.create()
    
    # Copy sources
    sources_dir = project.get_dir("sources")
    for src in source_files:
        copy_file(src, sources_dir / src.name)
    
    # Initial DEVSTATE
    from book_fabric.core.state import ProjectState
    state = ProjectState(project)
    
    data = {
        "project_title": book_params.get("title", "Unknown"),
        "current_phase": "PHASE 0",
        "completed_phases": [],
        "current_task": "Project Initialization",
        "next_task": "Source Audit",
        "sources_loaded": "\n".join([f.name for f in source_files]),
        "agents_created": "None",
        "model_used": "N/A",
        "chapter_status": "None",
        "last_checkpoint": "Initial creation",
        "unresolved_issues": "None",
        "failed_tasks": "None",
        "resume_instructions": "Start Phase 1"
    }
    state.update_devstate(state.generate_devstate_markdown(data))
    state.save_resume_state({"phase": 0, "status": "COMPLETED"})
    
    return project
