import streamlit as st
import os
from pathlib import Path
from book_fabric.core.project import Project
from book_fabric.core.llm import LLMRouter
from book_fabric.core.state import ProjectState
from book_fabric.phases.phase0_project import run_phase0
from book_fabric.phases.phase1_source_audit import run_phase1
from book_fabric.phases.phase2_architecture import run_phase2
from book_fabric.phases.phase3_agents import run_phase3
from book_fabric.phases.phase4_evidence import run_phase4
from book_fabric.phases.phase5_chapters import run_phase5
from book_fabric.phases.phase9_final import run_phase9

st.set_page_config(page_title="BOOK FABRIC", layout="wide")

st.title("📖 BOOK FABRIC")
st.subheader("Automated Multi-Agent Book Production System")

# Initialize router
router = LLMRouter(Path("book_fabric/config/models.yaml"))

# Sidebar: Project Selection
st.sidebar.header("Project Management")
projects_dir = Path("projects")
projects_dir.mkdir(exist_ok=True)
available_projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]
selected_project_name = st.sidebar.selectbox("Select Project", ["New Project"] + available_projects)

if selected_project_name == "New Project":
    st.header("Create New Project")
    with st.form("new_project"):
        p_name = st.text_input("Project Name")
        title = st.text_input("Book Title")
        subject = st.text_input("Subject/Domain")
        audience = st.text_input("Intended Audience")
        style = st.text_input("Target Style")
        length = st.text_input("Target Length")
        chapters = st.number_input("Chapter Count", min_value=1, value=5)
        uploaded_files = st.file_uploader("Upload Source Markdown Files", type=["md"], accept_multiple_files=True)
        submit = st.form_submit_button("Create and Initialize")
        
        if submit:
            if not p_name or not title:
                st.error("Project Name and Title are required.")
            else:
                # Save uploaded files to a temp dir
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
                st.success(f"Project {p_name} created!")
                st.rerun()

else:
    # Existing Project
    project = Project(selected_project_name)
    state = ProjectState(project)
    
    st.header(f"Project: {selected_project_name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Status")
        st.markdown(state.get_devstate())
    
    with col2:
        st.subheader("Controls")
        
        if st.button("Run Phase 1: Source Audit"):
            run_phase1(project, router)
            st.rerun()
            
        if st.button("Run Phase 2: Architecture"):
            # For simplicity, we'll reuse some params or ask user. 
            # In a real app, these would be saved in a config file.
            params = {"title": "Existing Book", "subject": "General", "audience": "General", "style": "General", "length": "General", "chapters": 5}
            run_phase2(project, router, params)
            st.rerun()
            
        if st.button("Run Phase 3: Agents"):
            params = {"subject": "General"}
            run_phase3(project, router, params)
            st.rerun()
            
        if st.button("Run Phase 4: Evidence Map"):
            run_phase4(project, router)
            st.rerun()
            
        if st.button("Draft Chapter 01"):
            run_phase5(project, router, "01", "Introduction")
            st.rerun()
            
        if st.button("Assemble Final Book"):
            run_phase9(project)
            st.rerun()
            
        st.divider()
        st.subheader("Project Files")
        all_files = []
        for d in project.dirs.values():
            all_files.extend([f.relative_to(project.root) for f in d.rglob("*") if f.is_file()])
        
        selected_file = st.selectbox("View File", all_files)
        if selected_file:
            with open(project.root / selected_file, "r", encoding="utf-8") as f:
                st.text_area("Content", f.read(), height=400)

