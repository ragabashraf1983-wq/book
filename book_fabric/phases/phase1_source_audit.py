from pathlib import Path
from book_fabric.core.files import list_markdown_files, read_text_file, write_text_file
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState

def run_phase1(project, router: LLMRouter):
    state = ProjectState(project)
    sources_dir = project.get_dir("sources")
    source_files = list_markdown_files(sources_dir)
    
    manifest_content = "# SOURCE MANIFEST\n\n"
    synthesis_content = "# SOURCE SYNTHESIS\n\n"
    
    for src in source_files:
        content = read_text_file(src)
        prompt = f"Analyze the following source document and provide: title, word count, chapter structure, major topics, domain, and reliability note.\n\nContent:\n{content[:10000]}" # Truncate for MVP
        
        analysis = router.generate("extraction", prompt, system_prompt="You are a Source Analyst agent.")
        manifest_content += f"## {src.name}\n{analysis}\n\n"
        
        # Basic synthesis
        synth_prompt = f"Summarize the key concepts and arguments from this source for a book synthesis:\n\n{content[:10000]}"
        synthesis_content += f"## {src.name}\n{router.generate('extraction', synth_prompt)}\n\n"

    write_text_file(project.get_dir("analysis") / "SOURCE_MANIFEST.md", manifest_content)
    write_text_file(project.get_dir("analysis") / "SOURCE_SYNTHESIS.md", synthesis_content)
    
    # Update state
    current_dev = state.get_devstate()
    # Simple replacement for MVP
    updated_dev = current_dev.replace("Current Phase: PHASE 0", "Current Phase: PHASE 1")
    updated_dev = updated_dev.replace("Next Task: Source Audit", "Next Task: Book Architecture")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 1, "status": "COMPLETED"})
