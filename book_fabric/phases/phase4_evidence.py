from pathlib import Path
from book_fabric.core.files import read_text_file, write_text_file
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState

def run_phase4(project, router: LLMRouter):
    state = ProjectState(project)
    architecture = read_text_file(project.get_dir("planning") / "BOOK_ARCHITECTURE.md")
    synthesis = read_text_file(project.get_dir("analysis") / "SOURCE_SYNTHESIS.md")
    
    prompt = f"Based on this architecture and source synthesis, create an EVIDENCE MAP. For each chapter, identify which sources to use, key concepts, and claims requiring verification.\n\nArchitecture:\n{architecture}\n\nSynthesis:\n{synthesis}"
    
    evidence_map = router.generate("planning", prompt, system_prompt="You are a Citation/Source Agent.")
    write_text_file(project.get_dir("planning") / "EVIDENCE_MAP.md", evidence_map)
    
    # Update state
    current_dev = state.get_devstate()
    updated_dev = current_dev.replace("Current Phase: PHASE 3", "Current Phase: PHASE 4")
    updated_dev = updated_dev.replace("Next Task: Evidence Map", "Next Task: Chapter Production")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 4, "status": "COMPLETED"})
