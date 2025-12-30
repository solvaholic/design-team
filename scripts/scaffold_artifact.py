#!/usr/bin/env python3
"""Scaffold new artifacts from templates."""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime
import argparse


def scaffold_project(name: str, workspace: Path, problem: str = "") -> Path:
    """Create new project from template."""
    projects_dir = workspace / "projects"
    projects_dir.mkdir(exist_ok=True)
    
    project_dir = projects_dir / name
    if project_dir.exists():
        raise ValueError(f"Project '{name}' already exists")
    
    # Copy template structure
    template_dir = workspace / "templates" / "project"
    if not template_dir.exists():
        raise FileNotFoundError("Project template not found")
    
    shutil.copytree(template_dir, project_dir)
    
    # Update currentstate.json
    state_file = project_dir / "currentstate.json"
    with open(state_file) as f:
        state = json.load(f)
    
    state["project_name"] = name
    if problem:
        state["problem_statement"] = problem
    state["last_updated"] = datetime.now().isoformat()
    
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)
    
    return project_dir


def scaffold_insight(name: str, project_dir: Path, insight_type: str = "observation") -> Path:
    """Create new insight artifact from template."""
    insights_dir = project_dir / "insights"
    insights_dir.mkdir(exist_ok=True)
    
    workspace = project_dir.parent.parent  # Navigate to workspace root
    
    templates = {
        "observation": "observation_template.md",
        "interview": "interview_template.md",
        "synthesis": "research_synthesis_template.md"
    }
    
    if insight_type not in templates:
        raise ValueError(f"Invalid insight type: {insight_type}")
    
    template_file = workspace / "templates" / "insights" / templates[insight_type]
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    # Create artifact with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    artifact_file = insights_dir / f"{name}-{timestamp}.md"
    
    shutil.copy(template_file, artifact_file)
    
    # Replace placeholders
    content = artifact_file.read_text()
    content = content.replace("[Name/Description]", name)
    content = content.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
    artifact_file.write_text(content)
    
    return artifact_file


def scaffold_idea(name: str, project_dir: Path) -> Path:
    """Create new idea document from template."""
    ideas_dir = project_dir / "ideas"
    ideas_dir.mkdir(exist_ok=True)
    
    workspace = project_dir.parent.parent
    template_file = workspace / "templates" / "ideas" / "idea_template.md"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    # Sanitize name for filename
    filename = name.lower().replace(" ", "_")
    artifact_file = ideas_dir / f"{filename}.md"
    
    if artifact_file.exists():
        raise ValueError(f"Idea '{name}' already exists")
    
    shutil.copy(template_file, artifact_file)
    
    # Replace placeholders
    content = artifact_file.read_text()
    content = content.replace("[Idea Name]", name)
    content = content.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
    artifact_file.write_text(content)
    
    return artifact_file


def scaffold_prototype(idea_name: str, project_dir: Path, iteration: int = 1) -> Path:
    """Create new prototype document from template."""
    ideas_dir = project_dir / "ideas"
    ideas_dir.mkdir(exist_ok=True)
    
    workspace = project_dir.parent.parent
    template_file = workspace / "templates" / "ideas" / "prototype_template.md"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    # Sanitize name for filename
    filename = idea_name.lower().replace(" ", "_")
    artifact_file = ideas_dir / f"{filename}-{iteration:03d}.md"
    
    if artifact_file.exists():
        raise ValueError(f"Prototype iteration {iteration} already exists")
    
    shutil.copy(template_file, artifact_file)
    
    # Replace placeholders
    content = artifact_file.read_text()
    content = content.replace("[Idea Name]", idea_name)
    content = content.replace("[###]", f"{iteration:03d}")
    content = content.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
    artifact_file.write_text(content)
    
    return artifact_file


def scaffold_playback(gate: str, project_dir: Path) -> Path:
    """Create new playback document from template."""
    playbacks_dir = project_dir / "playbacks"
    playbacks_dir.mkdir(exist_ok=True)
    
    workspace = project_dir.parent.parent
    template_file = workspace / "templates" / "playbacks" / "playback_template.md"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")
    
    timestamp = datetime.now().strftime("%Y%m%d")
    artifact_file = playbacks_dir / f"{gate}-{timestamp}.md"
    
    if artifact_file.exists():
        raise ValueError(f"Playback for {gate} on {timestamp} already exists")
    
    shutil.copy(template_file, artifact_file)
    
    # Replace placeholders
    content = artifact_file.read_text()
    content = content.replace("[Phase Gate Name]", gate)
    content = content.replace("[Date]", datetime.now().strftime("%Y-%m-%d"))
    artifact_file.write_text(content)
    
    return artifact_file


def main():
    parser = argparse.ArgumentParser(description="Scaffold artifacts from templates")
    parser.add_argument("--type", required=True,
                       choices=["project", "insight", "idea", "prototype", "playback"],
                       help="Type of artifact to create")
    parser.add_argument("--name", required=True,
                       help="Name of the artifact")
    parser.add_argument("--project", type=Path,
                       help="Path to project directory (not needed for project type)")
    parser.add_argument("--insight-type", choices=["observation", "interview", "synthesis"],
                       default="observation",
                       help="Type of insight (for insight artifacts)")
    parser.add_argument("--iteration", type=int, default=1,
                       help="Iteration number (for prototype artifacts)")
    parser.add_argument("--problem", type=str, default="",
                       help="Problem statement (for project artifacts)")
    
    args = parser.parse_args()
    
    try:
        # Find workspace root
        if args.type == "project":
            workspace = Path.cwd()
            while workspace.parent != workspace:
                if (workspace / ".github").exists():
                    break
                workspace = workspace.parent
            
            artifact_path = scaffold_project(args.name, workspace, args.problem)
        else:
            if not args.project:
                raise ValueError(f"--project required for {args.type} artifacts")
            
            if args.type == "insight":
                artifact_path = scaffold_insight(args.name, args.project, args.insight_type)
            elif args.type == "idea":
                artifact_path = scaffold_idea(args.name, args.project)
            elif args.type == "prototype":
                artifact_path = scaffold_prototype(args.name, args.project, args.iteration)
            elif args.type == "playback":
                artifact_path = scaffold_playback(args.name, args.project)
        
        print(f"Created: {artifact_path}")
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
