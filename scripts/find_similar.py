#!/usr/bin/env python3
"""Find similar or overlapping projects."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse


def load_all_projects(workspace: Path) -> List[Tuple[Path, Dict[str, Any]]]:
    """Load all currentstate.json files from projects/ directory."""
    projects = []
    projects_dir = workspace / "projects"
    
    if not projects_dir.exists():
        return projects
    
    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            state_file = project_dir / "currentstate.json"
            if state_file.exists():
                with open(state_file) as f:
                    try:
                        state = json.load(f)
                        projects.append((project_dir, state))
                    except json.JSONDecodeError:
                        continue
    
    return projects


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from text."""
    # Simple keyword extraction - could be enhanced with NLP
    stop_words = {"a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
                  "in", "on", "at", "to", "for", "of", "with", "by", "from"}
    
    words = text.lower().split()
    keywords = {w.strip(",.!?;:") for w in words if w not in stop_words and len(w) > 3}
    return keywords


def calculate_similarity(project1: Dict[str, Any], project2: Dict[str, Any]) -> float:
    """Calculate similarity score between two projects (0-1)."""
    score = 0.0
    
    # Compare problem statements
    p1_keywords = extract_keywords(project1.get("problem_statement", ""))
    p2_keywords = extract_keywords(project2.get("problem_statement", ""))
    
    if p1_keywords and p2_keywords:
        overlap = len(p1_keywords & p2_keywords)
        total = len(p1_keywords | p2_keywords)
        score += (overlap / total) * 0.5  # 50% weight
    
    # Compare stakeholder groups
    p1_stakeholders = {sh.get("group", "").lower() 
                      for sh in project1.get("stakeholders", [])}
    p2_stakeholders = {sh.get("group", "").lower() 
                      for sh in project2.get("stakeholders", [])}
    
    if p1_stakeholders and p2_stakeholders:
        overlap = len(p1_stakeholders & p2_stakeholders)
        total = len(p1_stakeholders | p2_stakeholders)
        score += (overlap / total) * 0.3  # 30% weight
    
    # Compare insights (if available)
    p1_insights = {extract_keywords(i.get("finding", "")) 
                  for i in project1.get("insights", [])}
    p2_insights = {extract_keywords(i.get("finding", "")) 
                  for i in project2.get("insights", [])}
    
    if p1_insights and p2_insights:
        # Flatten sets of sets for comparison
        p1_all = set().union(*p1_insights) if p1_insights else set()
        p2_all = set().union(*p2_insights) if p2_insights else set()
        
        if p1_all and p2_all:
            overlap = len(p1_all & p2_all)
            total = len(p1_all | p2_all)
            score += (overlap / total) * 0.2  # 20% weight
    
    return score


def find_similar(target_project: Path, workspace: Path, threshold: float = 0.3) -> List[Dict]:
    """Find projects similar to the target."""
    all_projects = load_all_projects(workspace)
    
    # Load target project
    target_state_file = target_project / "currentstate.json"
    if not target_state_file.exists():
        raise FileNotFoundError(f"No currentstate.json in {target_project}")
    
    with open(target_state_file) as f:
        target_state = json.load(f)
    
    target_name = target_state.get("project_name")
    
    similar = []
    for project_path, state in all_projects:
        # Skip self
        if project_path == target_project:
            continue
        
        score = calculate_similarity(target_state, state)
        
        if score >= threshold:
            similar.append({
                "project": state.get("project_name"),
                "path": str(project_path.relative_to(workspace)),
                "phase": state.get("phase"),
                "similarity": round(score, 2),
                "problem": state.get("problem_statement", "")[:100] + "..."
            })
    
    # Sort by similarity descending
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similar


def main():
    parser = argparse.ArgumentParser(description="Find similar projects")
    parser.add_argument("--project", type=str, required=True,
                       help="Project name or path to project directory")
    parser.add_argument("--threshold", type=float, default=0.3,
                       help="Similarity threshold (0-1, default 0.3)")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    # Convert project name to path if needed
    project_path = Path(args.project)
    if not project_path.is_absolute() and not str(project_path).startswith("projects/"):
        project_path = Path("projects") / project_path
    
    # Find workspace root (look for .github directory)
    workspace = project_path
    while workspace.parent != workspace:
        if (workspace / ".github").exists():
            break
        workspace = workspace.parent
    
    try:
        similar = find_similar(project_path, workspace, args.threshold)
        
        result = {
            "project": project_path.name,
            "similar_projects": similar,
            "count": len(similar)
        }
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Project: {result['project']}")
            print(f"Similar projects found: {result['count']}")
            
            if similar:
                print("\nSimilar Projects:")
                for proj in similar:
                    print(f"\n  {proj['project']} (similarity: {proj['similarity']})")
                    print(f"  Phase: {proj['phase']}")
                    print(f"  Path: {proj['path']}")
                    print(f"  Problem: {proj['problem']}")
            else:
                print("\nNo similar projects found")
        
        sys.exit(0)
        
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
