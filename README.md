# BOOK FABRIC

BOOK FABRIC is an automated multi-agent book and Canonical Knowledge Base production system. It transforms a set of Markdown source documents into a structured, reviewed, and synthesized book.

## Features
- **Local-First**: All projects are stored in the `projects/` directory. No cloud database required.
- **Resumable**: Tracks progress via `DEVSTATE.md` and `RESUME_STATE.json`.
- **Multi-Agent Workflow**: Uses specialized agents (Project Manager, Architect, Writing Agent, etc.) to produce high-quality content.
- **Multi-Model Routing**: Supports various LLM providers (OpenAI, GitHub Models, Ollama) via a configurable YAML file.
- **Evidence-Based**: Every claim is mapped to source documents.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ragabashraf1983-wq/book
   cd book
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pyyaml requests pydantic
   ```

3. Configure LLM models:
   Edit `book_fabric/config/models.yaml` and set your environment variables for API keys:
   ```bash
   export OPENAI_API_KEY='your-key'
   export GITHUB_TOKEN='your-token'
   ```

## Running the App

### 1. Configuration (9router)
The app is configured to use **9router** by default. To set it up:

1. Create a file named `.env` in the root directory.
2. Add your 9router API key:
   ```env
   NINEROUTER_API_KEY=your_sk_key_here
   ```
3. (Optional) If you are using a local tunnel, Tailscale, or a specific endpoint, add:
   ```env
   9ROUTER_ENDPOINT=http://your-endpoint:port
   ```

### 2. Launching the App
...

## Project Workflow
1. **Create Project**: Define title, subject, and upload `.md` sources.
2. **Source Audit**: Analyze sources and create a manifest.
3. **Architecture**: Design the book structure and TOC.
4. **Agent Roster**: Create specialist agents for the domain.
5. **Evidence Map**: Map concepts to sources.
6. **Chapter Production**: Draft, review (via 5 agents), and revise chapters.
7. **Final Assembly**: Combine all approved content into `final_<book_name>.md`.

## Project Structure
- `projects/<project_name>/00_Project/`: Metadata and state.
- `projects/<project_name>/10_Sources/`: Original source documents.
- `projects/<project_name>/20_Analysis/`: Source synthesis and gap analysis.
- `projects/<project_name>/30_Planning/`: Architecture and evidence maps.
- `projects/<project_name>/40_Chapters/`: Drafted chapters.
- `projects/<project_name>/50_Reviews/`: Agent reviews.
- `projects/<project_name>/70_Final/`: The final assembled book.
