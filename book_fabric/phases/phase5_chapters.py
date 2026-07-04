from pathlib import Path
from book_fabric.core.files import read_text_file, write_text_file
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState

def run_phase5(project, router: LLMRouter, chapter_id: str, chapter_title: str):
    state = ProjectState(project)
    architecture = read_text_file(project.get_dir("planning") / "BOOK_ARCHITECTURE.md")
    evidence_map = read_text_file(project.get_dir("planning") / "EVIDENCE_MAP.md")
    
    # 1. Draft
    draft_prompt = f"Draft Chapter {chapter_id}: {chapter_title}. Use this architecture and evidence map as a guide.\n\nArchitecture:\n{architecture}\n\nEvidence Map:\n{evidence_map}\n\nFollow the standard chapter template: Objectives, Prerequisites, Intro, Core Concepts, Application, Examples, Summary, References."
    draft = router.generate("writing", draft_prompt, system_prompt="You are the Writing Agent.")
    
    # 2. Consultation Loop (Simplified for MVP)
    reviewers = ["Domain Expert", "Methodologist", "Critic", "Style Editor", "Consistency Agent"]
    reviews = ""
    for rev in reviewers:
        rev_prompt = f"Review the following chapter draft for {rev} criteria. Find weaknesses and suggest improvements.\n\nDraft:\n{draft}"
        review = router.generate("review", rev_prompt, system_prompt=f"You are the {rev} agent.")
        reviews += f"## {rev} Review\n{review}\n\n"
    
    # 3. Revision
    revision_prompt = f"Revise the chapter draft based on these reviews:\n\n{reviews}\n\nOriginal Draft:\n{draft}"
    final_draft = router.generate("writing", revision_prompt, system_prompt="You are the Writing Agent.")
    
    # 4. Save
    chapter_path = project.get_dir("chapters") / f"Chapter_{chapter_id}_{chapter_title.replace(' ', '_')}.md"
    write_text_file(chapter_path, final_draft)
    
    review_path = project.get_dir("reviews") / f"Chapter_{chapter_id}_Review.md"
    write_text_file(review_path, reviews)
    
    # Update state
    current_dev = state.get_devstate()
    updated_dev = current_dev.replace("Current Phase: PHASE 4", "Current Phase: PHASE 5")
    updated_dev = updated_dev.replace("Next Task: Chapter Production", f"Next Task: Chapter {chapter_id} Complete")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 5, "status": "IN_PROGRESS", "last_chapter": chapter_id})
