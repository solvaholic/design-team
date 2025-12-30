#!/usr/bin/env python3
"""Validate project state against schema and identify gaps."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse


def load_state(project_path: Path) -> Dict[str, Any]:
    """Load currentstate.json from project directory."""
    state_file = project_path / "currentstate.json"
    if not state_file.exists():
        raise FileNotFoundError(f"No currentstate.json found in {project_path}")
    
    with open(state_file) as f:
        return json.load(f)


def validate_structure(state: Dict[str, Any]) -> List[str]:
    """Check for required fields and valid structure."""
    errors = []
    
    # Required top-level fields
    required = ["project_name", "problem_statement", "phase", "stakeholders", 
                "assumptions", "research_plan", "insights", "ideas", "playbacks"]
    
    for field in required:
        if field not in state:
            errors.append(f"Missing required field: {field}")
    
    # Validate phase
    valid_phases = ["empathize", "define", "ideate", "prototype", "iterate"]
    if state.get("phase") not in valid_phases:
        errors.append(f"Invalid phase: {state.get('phase')}. Must be one of {valid_phases}")
    
    return errors


def identify_gaps(state: Dict[str, Any]) -> List[str]:
    """Identify missing or incomplete elements based on phase."""
    gaps = []
    phase = state.get("phase", "empathize")
    
    # Empathize phase checks
    if not state.get("stakeholders"):
        gaps.append("No stakeholders defined")
    else:
        for i, sh in enumerate(state["stakeholders"]):
            if not sh.get("needs") and not sh.get("pain_points"):
                gaps.append(f"Stakeholder '{sh.get('name', i)}' has no needs or pain points")
            if not sh.get("notes_links"):
                gaps.append(f"Stakeholder '{sh.get('name', i)}' has no research notes linked")
    
    # Define phase checks
    if phase in ["define", "ideate", "prototype", "iterate"]:
        if not state.get("insights"):
            gaps.append("No insights synthesized from research")
        
        if not state.get("assumptions"):
            gaps.append("No assumptions identified")
        else:
            ungraded = [a for a in state["assumptions"] 
                       if a.get("certainty") is None or a.get("risk") is None]
            if ungraded:
                gaps.append(f"{len(ungraded)} assumptions not graded for certainty/risk")
    
    # Ideate phase checks
    if phase in ["ideate", "prototype", "iterate"]:
        if not state.get("ideas"):
            gaps.append("No solution ideas generated")
        else:
            ungraded = [idea for idea in state["ideas"]
                       if idea.get("impact_grade") is None or idea.get("feasibility_grade") is None]
            if ungraded:
                gaps.append(f"{len(ungraded)} ideas not graded for impact/feasibility")
    
    # Prototype/Iterate phase checks
    if phase in ["prototype", "iterate"]:
        prototyped_ideas = [idea for idea in state.get("ideas", [])
                           if idea.get("status") in ["prototyping", "iterating"]]
        if not prototyped_ideas:
            gaps.append("No ideas in prototyping or iterating status")
    
    # Playback checks
    phase_playbacks = {
        "empathize": "empathize-complete",
        "define": "define-complete", 
        "ideate": "ideate-complete",
        "prototype": "prototype-complete",
        "iterate": "iterate-complete"
    }
    
    if phase in phase_playbacks:
        expected_playback = phase_playbacks[phase]
        playbacks = state.get("playbacks", [])
        if not any(pb.get("gate") == expected_playback for pb in playbacks):
            gaps.append(f"No playback recorded for {expected_playback} gate")
    
    return gaps


def main():
    parser = argparse.ArgumentParser(description="Validate project state")
    parser.add_argument("--project", type=Path, required=True,
                       help="Path to project directory")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        state = load_state(args.project)
        errors = validate_structure(state)
        gaps = identify_gaps(state)
        
        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "gaps": gaps,
            "phase": state.get("phase"),
            "project": state.get("project_name")
        }
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Project: {result['project']}")
            print(f"Phase: {result['phase']}")
            print(f"Valid: {'✓' if result['valid'] else '✗'}")
            
            if errors:
                print("\nStructure Errors:")
                for error in errors:
                    print(f"  ✗ {error}")
            
            if gaps:
                print("\nGaps Identified:")
                for gap in gaps:
                    print(f"  • {gap}")
            
            if not errors and not gaps:
                print("\n✓ State is valid with no gaps")
        
        sys.exit(0 if len(errors) == 0 else 1)
        
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
