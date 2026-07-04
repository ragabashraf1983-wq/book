from pathlib import Path
from book_fabric.core.files import list_markdown_files, read_text_file, write_text_file
from book_fabric.core.state import ProjectState

def run_phase9(project):
    state = ProjectState(project)
    chapters_dir = project.get_dir("chapters")
    chapter_files = sorted(list_markdown_files(chapters_dir))
    
    final_content = f"# {project.project_name}\n\n"
    
    for cf in chapter_files:
        final_content += f"## {cf.stem}\n\n"
        final_content += read_text_file(cf) + "\n\n"
    
    final_filename = f"final_{project.project_name}.md"
    write_text_file(project.get_dir("final") / final_filename, final_content)
    
    # Update state
    current_dev = state.get_devstate()
    updated_dev = current_dev.replace("Current Phase: PHASE 5", "Current Phase: PHASE 9")
    updated_dev = updated_dev.replace("Next Task: Chapter Production", "Next Task: COMPLETE")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 9, "status": "COMPLETED"})
