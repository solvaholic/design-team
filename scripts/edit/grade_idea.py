#!/usr/bin/env python3
"""Grade or update idea in currentstate.json.

Validates full schema and uses atomic write pattern.
"""

import argparse
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "currentstate.schema.json"


def validate_against_schema(data: Dict[str, Any]) -> tuple[bool, str | None]:
    """Validate data against JSON schema.
    
    Args:
        data: Data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Basic required field validation
        required_fields = ["project_name", "created_at", "updated_at", "phase"]
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
                
        # Validate phase enum
        valid_phases = ["empathize", "define", "ideate", "prototype", "iterate"]
        if data["phase"] not in valid_phases:
            return False, f"Invalid phase: {data['phase']}. Must be one of {valid_phases}"
            
        # Validate ideas structure
        if "ideas" in data:
            for idx, idea in enumerate(data["ideas"]):
                if not isinstance(idea, dict):
                    return False, f"Idea {idx} is not an object"
                    
                required = ["id", "title", "status"]
                for field in required:
                    if field not in idea:
                        return False, f"Idea {idx} missing required field: {field}"
                        
                for grade_field in ["impact", "feasibility"]:
                    if grade_field in idea and idea[grade_field] not in ["high", "medium", "low"]:
                        return False, f"Idea {idx} has invalid {grade_field}: {idea[grade_field]}"
                        
                valid_statuses = ["ideated", "prototyping", "iterating", "validated", "invalidated", "implemented"]
                if idea["status"] not in valid_statuses:
                    return False, f"Idea {idx} has invalid status: {idea['status']}"
                    
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def grade_idea(
    project_path: Path,
    idea_id: str,
    impact: str | None = None,
    feasibility: str | None = None,
    status: str | None = None,
    idea_doc_link: str | None = None,
    prototype_links: list[str] | None = None,
    append_prototype_links: bool = False
) -> Dict[str, Any]:
    """Grade or update an idea in currentstate.json.
    
    Args:
        project_path: Path to project directory
        idea_id: Unique ID for idea
        impact: Impact level (high, medium, low)
        feasibility: Feasibility level (high, medium, low)
        status: Status (ideated, prototyping, iterating, validated, invalidated, implemented)
        idea_doc_link: Link to detailed idea document
        prototype_links: List of prototype links (replaces or appends based on flag)
        append_prototype_links: If True, append to existing links instead of replacing
        
    Returns:
        Standardized result dictionary
    """
    try:
        state_file = project_path / "currentstate.json"
        
        if not state_file.exists():
            return {
                "status": "error",
                "data": None,
                "error": f"currentstate.json not found in {project_path}"
            }
            
        # Load current state
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
            
        # Find idea
        if "ideas" not in state:
            return {
                "status": "error",
                "data": None,
                "error": "No ideas array found in currentstate.json"
            }
            
        idea = None
        for i in state["ideas"]:
            if i["id"] == idea_id:
                idea = i
                break
                
        if idea is None:
            return {
                "status": "error",
                "data": None,
                "error": f"Idea with id '{idea_id}' not found"
            }
            
        # Update fields
        if impact is not None:
            if impact not in ["high", "medium", "low"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid impact: {impact}. Must be high, medium, or low"
                }
            idea["impact"] = impact
            
        if feasibility is not None:
            if feasibility not in ["high", "medium", "low"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid feasibility: {feasibility}. Must be high, medium, or low"
                }
            idea["feasibility"] = feasibility
            
        if status is not None:
            valid_statuses = ["ideated", "prototyping", "iterating", "validated", "invalidated", "implemented"]
            if status not in valid_statuses:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid status: {status}. Must be one of {valid_statuses}"
                }
            idea["status"] = status
            
        if idea_doc_link is not None:
            idea["idea_doc_link"] = idea_doc_link
            
        if prototype_links is not None:
            if append_prototype_links and "prototype_links" in idea:
                idea["prototype_links"] = idea.get("prototype_links", []) + prototype_links
            else:
                idea["prototype_links"] = prototype_links
                
        # Update timestamp
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # Validate full schema
        is_valid, error = validate_against_schema(state)
        if not is_valid:
            return {
                "status": "error",
                "data": None,
                "error": f"Schema validation failed: {error}"
            }
            
        # Atomic write: write to temp file, then rename
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=state_file.parent,
            delete=False,
            suffix=".tmp"
        ) as tmp_file:
            json.dump(state, tmp_file, indent=2, ensure_ascii=False)
            tmp_file.write("\n")
            tmp_path = Path(tmp_file.name)
            
        # Atomic rename
        tmp_path.replace(state_file)
        
        return {
            "status": "success",
            "data": {
                "idea_id": idea_id,
                "idea": idea,
                "updated_at": state["updated_at"]
            },
            "error": None
        }
        
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Invalid JSON in currentstate.json: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Error grading idea: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Grade or update idea in currentstate.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Grade impact and feasibility
  grade_idea.py --project projects/my-project --id idea1 \\
    --impact high --feasibility medium
  
  # Update status
  grade_idea.py --project projects/my-project --id idea1 \\
    --status prototyping
  
  # Add prototype link
  grade_idea.py --project projects/my-project --id idea1 \\
    --prototype-links "ideas/prototype-v1.md" --append-prototype-links
"""
    )
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="Path to project directory"
    )
    parser.add_argument(
        "--id",
        required=True,
        help="Idea ID"
    )
    parser.add_argument(
        "--impact",
        choices=["high", "medium", "low"],
        help="Impact level"
    )
    parser.add_argument(
        "--feasibility",
        choices=["high", "medium", "low"],
        help="Feasibility level"
    )
    parser.add_argument(
        "--status",
        choices=["ideated", "prototyping", "iterating", "validated", "invalidated", "implemented"],
        help="Idea status"
    )
    parser.add_argument(
        "--idea-doc-link",
        help="Link to detailed idea document"
    )
    parser.add_argument(
        "--prototype-links",
        nargs="+",
        help="List of prototype links"
    )
    parser.add_argument(
        "--append-prototype-links",
        action="store_true",
        help="Append to existing prototype links instead of replacing"
    )
    
    args = parser.parse_args()
    
    result = grade_idea(
        project_path=args.project,
        idea_id=args.id,
        impact=args.impact,
        feasibility=args.feasibility,
        status=args.status,
        idea_doc_link=args.idea_doc_link,
        prototype_links=args.prototype_links,
        append_prototype_links=args.append_prototype_links
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
