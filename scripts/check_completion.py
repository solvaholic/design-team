#!/usr/bin/env python3
"""Check if phase completion criteria are met."""

import json
import sys
from pathlib import Path
from typing import Dict, Any
import argparse


def load_state(project_path: Path) -> Dict[str, Any]:
    """Load currentstate.json from project directory."""
    state_file = project_path / "currentstate.json"
    if not state_file.exists():
        raise FileNotFoundError(f"No currentstate.json found in {project_path}")
    
    with open(state_file) as f:
        return json.load(f)


def check_empathize_complete(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Check if Empathize phase is complete."""
    reasons = []
    
    stakeholders = state.get("stakeholders", [])
    if len(stakeholders) < 2:
        reasons.append("Need at least 2 stakeholder groups defined")
    
    for sh in stakeholders:
        if not sh.get("notes_links"):
            reasons.append(f"Stakeholder '{sh.get('name')}' needs research notes")
        if not (sh.get("needs") or sh.get("pain_points")):
            reasons.append(f"Stakeholder '{sh.get('name')}' needs documented needs or pain points")
    
    insights = state.get("insights", [])
    if len(insights) < 3:
        reasons.append(f"Need at least 3 synthesized insights (have {len(insights)})")
    
    return len(reasons) == 0, reasons


def check_define_complete(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Check if Define phase is complete."""
    reasons = []
    
    insights = state.get("insights", [])
    if len(insights) < 3:
        reasons.append(f"Need at least 3 validated insights (have {len(insights)})")
    
    assumptions = state.get("assumptions", [])
    if not assumptions:
        reasons.append("No assumptions identified")
    else:
        ungraded = [a for a in assumptions 
                   if a.get("certainty") is None or a.get("risk") is None]
        if ungraded:
            reasons.append(f"{len(ungraded)} assumptions need certainty/risk grades")
        
        high_risk = [a for a in assumptions 
                    if a.get("risk") == "high" and a.get("certainty") == "low"]
        if high_risk:
            reasons.append(f"{len(high_risk)} high-risk assumptions need validation plan")
    
    return len(reasons) == 0, reasons


def check_ideate_complete(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Check if Ideate phase is complete."""
    reasons = []
    
    ideas = state.get("ideas", [])
    if len(ideas) < 3:
        reasons.append(f"Need at least 3 solution ideas (have {len(ideas)})")
    
    if ideas:
        ungraded = [idea for idea in ideas
                   if idea.get("impact_grade") is None or idea.get("feasibility_grade") is None]
        if ungraded:
            reasons.append(f"{len(ungraded)} ideas need impact/feasibility grades")
        
        high_impact = [idea for idea in ideas 
                      if idea.get("impact_grade") in ["high", "medium"]]
        if len(high_impact) < 2:
            reasons.append("Need at least 2 ideas with medium/high impact")
    
    return len(reasons) == 0, reasons


def check_prototype_complete(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Check if Prototype phase is complete."""
    reasons = []
    
    ideas = state.get("ideas", [])
    prototyped = [idea for idea in ideas if idea.get("status") == "prototyping"]
    
    if not prototyped:
        reasons.append("At least one idea must have a prototype")
    
    # Check for prototype documents in ideas/ folder
    # This would require filesystem access which we can add if needed
    
    return len(reasons) == 0, reasons


def check_iterate_complete(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Check if Iterate phase is complete."""
    reasons = []
    
    ideas = state.get("ideas", [])
    validated = [idea for idea in ideas 
                if idea.get("status") in ["validated", "implemented"]]
    
    if not validated:
        reasons.append("At least one idea must be validated through iteration")
    
    # Should have feedback from stakeholders documented
    # This would require checking prototype files for feedback sections
    
    return len(reasons) == 0, reasons


def main():
    parser = argparse.ArgumentParser(description="Check phase completion criteria")
    parser.add_argument("--project", type=str, required=True,
                       help="Project name or path to project directory")
    parser.add_argument("--phase", type=str,
                       help="Specific phase to check (default: current phase)")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    # Convert project name to path if needed
    project_path = Path(args.project)
    if not project_path.is_absolute() and not str(project_path).startswith("projects/"):
        project_path = Path("projects") / project_path
    
    try:
        state = load_state(project_path)
        phase = args.phase or state.get("phase")
        
        checkers = {
            "empathize": check_empathize_complete,
            "define": check_define_complete,
            "ideate": check_ideate_complete,
            "prototype": check_prototype_complete,
            "iterate": check_iterate_complete
        }
        
        if phase not in checkers:
            raise ValueError(f"Invalid phase: {phase}")
        
        complete, reasons = checkers[phase](state)
        
        result = {
            "phase": phase,
            "complete": complete,
            "reasons": reasons,
            "project": state.get("project_name")
        }
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Project: {result['project']}")
            print(f"Phase: {phase}")
            print(f"Complete: {'✓' if complete else '✗'}")
            
            if reasons:
                print("\nRemaining Requirements:")
                for reason in reasons:
                    print(f"  • {reason}")
            else:
                print("\n✓ Phase completion criteria met")
                print("  Ready for playback presentation to LT")
        
        sys.exit(0 if complete else 1)
        
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
