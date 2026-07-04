import streamlit as st
import os
from pathlib import Path
from book_fabric.core.project import Project
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState
from book_fabric.core.config_manager import is_configured, get_setting, save_setting
from book_fabric.phases.phase0_project import run_phase0
from book_fabric.phases.phase1_source_audit import run_phase1
from book_fabric.phases.phase2_architecture import run_phase2
from book_fabric.phases.phase3_agents import run_phase3
from book_fabric.phases.phase4_evidence import run_phase4
from book_fabric.phases.phase5_chapters import run_phase5
from book_fabric.phases.phase9_final import run_phase9

st.set_page_config(page_title="BOOK FABRIC", layout="wide", page_icon="📖")

# --- APP STATE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# --- SETUP WIZARD ---
if not is_configured():
    st.title("👋 Welcome to BOOK FABRIC")
    st.subheader("Let's get you set up in 30 seconds!")
    
    with st.container(border=True):
        st.markdown("To start generating books, we need to connect to your **9router** account.")
        api_key = st.text_input("Enter your 9router API Key", type="password", placeholder="sk-...")
        endpoint = st.text_input("API Endpoint", value="https://api.9router.ai", help="Leave as default unless using a local tunnel/VPN")
        
        if st.button("Save Settings & Start"):
            if api_key:
                save_setting("NINEROUTER_API_KEY", api_key)
                save_setting("9ROUTER_ENDPOINT", endpoint)
                st.success("Settings saved! The app will now reload.")
                st.rerun()
            else:
                st.error("Please enter your API key to continue.")
    
    st.info("Where do I find my key? Go to your 9router dashboard -> API Keys.")
    st.stop() # Stop execution until configured

# --- MAIN APPLICATION ---
# Initialize router
router = LLMRouter(Path("book_fabric/config/models.yaml"))

st.title("📖 BOOK FABRIC")
st.subheader("Automated Multi-Agent Book Production System")

# Sidebar: Navigation
menu = st.sidebar.selectbox("Menu", ["🏠 Dashboard", "⚙️ Settings", "📂 Project Management"])

if menu == "⚙️ Settings":
    st.header("Configuration Settings")
    
    with st.container(border=True):
        st.subheader("API Connection")
        current_key = get_setting("NINEROUTER_API_KEY")
        new_key = st.text_input("9router API Key", value=current_key, type="password")
        
        current_endpoint = get_setting("9ROUTER_ENDPOINT", "https://api.9router.ai")
        new_endpoint = st.text_input("API Endpoint", value=current_endpoint)
        
        if st.button("Update Settings"):
            save_setting("NINEROUTER_API_KEY", new_key)
            save_setting("9ROUTER_ENDPOINT", new_endpoint)
            st.success("Settings updated!")
            st.rerun()

    st.divider()
    st.subheader("Model Routing")
    st.info("Model roles (Planning, Writing, Review) are defined in `book_fabric/config/models.yaml`.")

elif menu == "📂 Project Management":
    st.header("Manage Projects")
    
    projects_dir = Path("projects")
    projects_dir.mkdir(exist_ok=True)
    available_projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]
    selected_project_name = st.selectbox("Select Project", ["+ Create New Project"] + available_projects)

    if selected_project_name == "+ Create New Project":
        st.subheader("New Book Project")
        with st.form("new_project"):
            p_name = st.text_input("Project Folder Name (e.g., My_First_Book)")
            title = st.text_input("Book Title")
            subject = st.text_input("Subject/Domain")
            audience = st.text_input("Intended Audience")
            style = st.text_input("Target Style")
            length = st.text_input("Target Length")
            chapters = st.number_input("Chapter Count", min_value=1, value=5)
            uploaded_files = st.file_uploader("Upload Source Markdown Files", type=["md"], accept_multiple_files=True)
            submit = st.form_submit_button("🚀 Initialize Project")
            
            if submit:
                if not p_name or not title:
                    st.error("Project Folder Name and Title are required.")
                else:
                    temp_dir = Path("temp_uploads")
                    temp_dir.mkdir(exist_ok=True)
                    source_paths = []
                    for uploaded_file in uploaded_files:
                        path = temp_dir / uploaded_file.name
                        with open(path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        source_paths.append(path)
                    
                    params = {
                        "title": title, "subject": subject, "audience": audience,
                        "style": style, "length": length, "chapters": chapters
                    }
                    run_phase0(p_name, source_paths, params)
                    st.success(f"Project {p_name} created successfully!")
                    st.rerun()
    else:
        st.info(f"Working on project: **{selected_project_name}**")
        st.markdown("Go to the **Dashboard** to start the production process.")

else: # Dashboard
    st.header("Production Dashboard")
    
    projects_dir = Path("projects")
    available_projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]
    
    if not available_projects:
        st.warning("No projects found. Please go to 'Project Management' to create one.")
    else:
        selected_project_name = st.selectbox("Active Project", available_projects)
        project = Project(selected_project_name)
        state = ProjectState(project)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Project State")
            st.markdown(state.get_devstate())
        
        with col2:
            st.subheader("Action Center")
            
            # Phase-based buttons
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔍 Run Source Audit"):
                    run_phase1(project, router)
                    st.rerun()
                if st.button("📐 Design Architecture"):
                    params = {"title": "Existing Book", "subject": "General", "audience": "General", "style": "General", "length": "General", "chapters": 5}
                    run_phase2(project, router, params)
                    st.rerun()
                if st.button("🤖 Setup Agents"):
                    params = {"subject": "General"}
                    run_phase3(project, router, params)
                    st.rerun()
            with c2:
                if st.button("🗺️ Create Evidence Map"):
                    run_phase4(project, router)
                    st.rerun()
                if st.button("✍️ Draft Chapter 01"):
                    run_phase5(project, router, "01", "Introduction")
                    st.rerun()
                if st.button("📚 Assemble Final Book"):
                    run_phase9(project)
                    st.rerun()
            
            st.divider()
            st.subheader("File Explorer")
            all_files = []
            for d in project.dirs.values():
                all_files.extend([f.relative_to(project.root) for f in d.rglob("*") if f.is_file()])
            
            selected_file = st.selectbox("Open File", all_files)
            if selected_file:
                with open(project.root / selected_file, "r", encoding="utf-8") as f:
                    st.text_area("Content", f.read(), height=400)
