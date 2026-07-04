from pathlib import Path
from book_fabric.core.files import read_text_file, write_text_file
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState

def run_phase2(project, router: LLMRouter, book_params: dict):
    state = ProjectState(project)
    
    # Read synthesis to inform architecture
    synthesis = read_text_file(project.get_dir("analysis") / "SOURCE_SYNTHESIS.md")
    
    prompt = f"""
    Design a book architecture based on the following parameters:
    Title: {book_params.get('title')}
    Subject: {book_params.get('subject')}
    Audience: {book_params.get('audience')}
    Style: {book_params.get('style')}
    Length: {book_params.get('length')}
    Chapter Count: {book_params.get('chapters')}
    
    Source Synthesis:
    {synthesis}
    
    Provide a detailed structure with Parts, Chapters, and Subsections.
    """
    
    architecture = router.generate("planning", prompt, system_prompt="You are an Architect agent.")
    toc = router.generate("planning", f"Create a MASTER_TOC.md based on this architecture:\n{architecture}", system_prompt="You are an Architect agent.")
    
    write_text_file(project.get_dir("planning") / "BOOK_ARCHITECTURE.md", architecture)
    write_text_file(project.get_dir("project") / "MASTER_TOC.md", toc)
    
    # Update state
    current_dev = state.get_devstate()
    updated_dev = current_dev.replace("Current Phase: PHASE 1", "Current Phase: PHASE 2")
    updated_dev = updated_dev.replace("Next Task: Book Architecture", "Next Task: Agent Roster")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 2, "status": "COMPLETED"})
