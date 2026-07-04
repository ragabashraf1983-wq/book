from book_fabric.core.agents import AgentRoster, Agent
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState

def run_phase3(project, router: LLMRouter, book_params: dict):
    state = ProjectState(project)
    roster = AgentRoster(project)
    roster.create_default_agents()
    
    subject = book_params.get("subject", "General")
    prompt = f"The book subject is {subject}. Suggest 3-5 additional specialist agents needed for this domain. For each, provide: Name, Role, Expertise, Permissions, Forbidden actions, and Review criteria. Format as a list."
    
    specialists_text = router.generate("planning", prompt, system_prompt="You are a Project Manager agent.")
    
    # For MVP, we'll just add the text to the roster or try to parse it. 
    # To keep it simple, we'll append the specialists to the roster file manually or just log them.
    # Let's try to just save them in a simplified way.
    roster.save_roster()
    with open(project.get_dir("project") / "AGENT_ROSTER.md", "a") as f:
        f.write("\n## Dynamic Specialist Agents\n")
        f.write(specialists_text)
    
    # Update state
    current_dev = state.get_devstate()
    updated_dev = current_dev.replace("Current Phase: PHASE 2", "Current Phase: PHASE 3")
    updated_dev = updated_dev.replace("Next Task: Agent Roster", "Next Task: Evidence Map")
    state.update_devstate(updated_dev)
    state.save_resume_state({"phase": 3, "status": "COMPLETED"})
