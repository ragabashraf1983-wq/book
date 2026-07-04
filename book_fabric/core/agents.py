from typing import List, Dict, Any
from pathlib import Path
from .files import write_text_file

class Agent:
    def __init__(self, name: str, role: str, expertise: str, permissions: List[str], forbidden: List[str], criteria: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.permissions = permissions
        self.forbidden = forbidden
        self.criteria = criteria

    def to_markdown(self) -> str:
        return (
            f"### {self.name}\n"
            f"- **Role:** {self.role}\n"
            f"- **Expertise:** {self.expertise}\n"
            f"- **Permissions:** {', '.join(self.permissions)}\n"
            f"- **Forbidden:** {', '.join(self.forbidden)}\n"
            f"- **Review Criteria:** {self.criteria}\n"
        )

class AgentRoster:
    def __init__(self, project: 'Project'):
        self.project = project
        self.agents: Dict[str, Agent] = {}

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def save_roster(self):
        content = "# Agent Roster\n\n"
        for agent in self.agents.values():
            content += agent.to_markdown() + "\n"
        write_text_file(self.project.get_dir("project") / "AGENT_ROSTER.md", content)

    def create_default_agents(self):
        defaults = [
            Agent("Project Manager", "Coordination", "Project oversight and state management", ["read_state", "update_state"], ["write_chapters"], "Consistency and progress"),
            Agent("Source Analyst", "Analysis", "Extracting concepts from Markdown sources", ["read_sources", "write_analysis"], ["invent_sources"], "Accuracy of extraction"),
            Agent("Architect", "Design", "Creating book structure and TOC", ["write_planning"], ["change_sources"], "Logical flow and coverage"),
            Agent("Writing Agent", "Drafting", "Generating chapter content", ["write_chapters"], ["plagiarize"], "Clarity and depth"),
            Agent("Reviewer", "Quality Control", "Checking completeness and accuracy", ["read_chapters", "write_reviews"], ["approve_without_review"], "Adherence to guidelines"),
            Agent("Critic", "Stress Testing", "Finding weaknesses and contradictions", ["read_chapters", "write_reviews"], [], "Rigorous critique"),
            Agent("Style Editor", "Editing", "Enforcing style and tone", ["read_chapters", "write_reviews"], [], "Consistency of voice"),
            Agent("Consistency Agent", "Verification", "Cross-chapter terminology check", ["read_chapters", "write_reviews"], [], "Terminology alignment"),
            Agent("Publisher", "Final Audit", "Final book assembly and verification", ["read_all", "write_final"], [], "Zero errors")
        ]
        for a in defaults:
            self.add_agent(a)
        self.save_roster()
