import os
from pathlib import Path
from book_fabric.core.project import Project
from book_fabric.core.llm import LLMRouter
from book_fabric.phases.phase0_project import run_phase0
from book_fabric.phases.phase1_source_audit import run_phase1
from book_fabric.phases.phase2_architecture import run_phase2
from book_fabric.phases.phase3_agents import run_phase3
from book_fabric.phases.phase4_evidence import run_phase4
from book_fabric.phases.phase5_chapters import run_phase5
from book_fabric.phases.phase9_final import run_phase9

def main():
    # Configuration
    router = LLMRouter(Path("book_fabric/config/models.yaml"))
    
    # Project parameters
    project_name = "Example_Book"
    book_params = {
        "title": "The Art of Local-First Systems",
        "subject": "Software Architecture",
        "audience": "Developers",
        "style": "Technical and Practical",
        "length": "Medium",
        "chapters": 5
    }
    
    # Create dummy source files for MVP test
    sources_dir = Path("examples/demo_book_project")
    sources_dir.mkdir(parents=True, exist_ok=True)
    (sources_dir / "source1.md").write_text("# Local-First Basics\nLocal-first software keeps data on the device.")
    (sources_dir / "source2.md").write_text("# Sync Strategies\nCRDTs are great for conflict-free replicated data types.")
    
    source_files = list(sources_dir.glob("*.md"))

    print("Starting Phase 0...")
    project = run_phase0(project_name, source_files, book_params)
    
    print("Starting Phase 1...")
    run_phase1(project, router)
    
    print("Starting Phase 2...")
    run_phase2(project, router, book_params)
    
    print("Starting Phase 3...")
    run_phase3(project, router, book_params)
    
    print("Starting Phase 4...")
    run_phase4(project, router)
    
    print("Starting Phase 5 (MVP: 1 Chapter)...")
    run_phase5(project, router, "01", "Introduction to Local-First")
    
    print("Starting Phase 9...")
    run_phase9(project)
    
    print(f"Book production complete! Final book at: {project.get_dir('final')}")

if __name__ == "__main__":
    main()
