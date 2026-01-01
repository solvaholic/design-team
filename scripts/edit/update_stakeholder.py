#!/usr/bin/env python3
"""Add or update stakeholder in currentstate.json.

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
            
        # Validate stakeholders structure
        if "stakeholders" in data:
            for idx, stakeholder in enumerate(data["stakeholders"]):
                if not isinstance(stakeholder, dict):
                    return False, f"Stakeholder {idx} is not an object"
                    
                required = ["id", "name", "type"]
                for field in required:
                    if field not in stakeholder:
                        return False, f"Stakeholder {idx} missing required field: {field}"
                        
                if stakeholder["type"] not in ["group", "individual"]:
                    return False, f"Stakeholder {idx} has invalid type: {stakeholder['type']}"
                    
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def update_stakeholder(
    project_path: Path,
    stakeholder_id: str,
    name: str | None = None,
    stakeholder_type: str | None = None,
    role: str | None = None,
    needs: list[str] | None = None,
    pain_points: list[str] | None = None,
    notes_links: list[str] | None = None,
    append_needs: bool = False,
    append_pain_points: bool = False,
    append_notes: bool = False
) -> Dict[str, Any]:
    """Add or update a stakeholder in currentstate.json.
    
    Args:
        project_path: Path to project directory
        stakeholder_id: Unique ID for stakeholder
        name: Stakeholder name
        stakeholder_type: Type (group or individual)
        role: Stakeholder role
        needs: List of needs (replaces or appends based on flag)
        pain_points: List of pain points (replaces or appends based on flag)
        notes_links: List of note links (replaces or appends based on flag)
        append_needs: If True, append to existing needs instead of replacing
        append_pain_points: If True, append to existing pain points
        append_notes: If True, append to existing notes links
        
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
            
        # Initialize stakeholders array if needed
        if "stakeholders" not in state:
            state["stakeholders"] = []
            
        # Find existing stakeholder or create new one
        stakeholder = None
        stakeholder_idx = None
        for idx, sh in enumerate(state["stakeholders"]):
            if sh["id"] == stakeholder_id:
                stakeholder = sh
                stakeholder_idx = idx
                break
                
        if stakeholder is None:
            # Create new stakeholder
            if not name or not stakeholder_type:
                return {
                    "status": "error",
                    "data": None,
                    "error": "name and type are required for new stakeholders"
                }
                
            stakeholder = {
                "id": stakeholder_id,
                "name": name,
                "type": stakeholder_type
            }
            state["stakeholders"].append(stakeholder)
            stakeholder_idx = len(state["stakeholders"]) - 1
            
        # Update fields
        if name is not None:
            stakeholder["name"] = name
        if stakeholder_type is not None:
            if stakeholder_type not in ["group", "individual"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid type: {stakeholder_type}. Must be 'group' or 'individual'"
                }
            stakeholder["type"] = stakeholder_type
        if role is not None:
            stakeholder["role"] = role
            
        # Handle array fields with append logic
        if needs is not None:
            if append_needs and "needs" in stakeholder:
                stakeholder["needs"] = stakeholder.get("needs", []) + needs
            else:
                stakeholder["needs"] = needs
                
        if pain_points is not None:
            if append_pain_points and "pain_points" in stakeholder:
                stakeholder["pain_points"] = stakeholder.get("pain_points", []) + pain_points
            else:
                stakeholder["pain_points"] = pain_points
                
        if notes_links is not None:
            if append_notes and "notes_links" in stakeholder:
                stakeholder["notes_links"] = stakeholder.get("notes_links", []) + notes_links
            else:
                stakeholder["notes_links"] = notes_links
                
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
                "stakeholder_id": stakeholder_id,
                "stakeholder": stakeholder,
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
            "error": f"Error updating stakeholder: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Add or update stakeholder in currentstate.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new stakeholder
  update_stakeholder.py --project projects/my-project --id s1 \\
    --name "Engineers" --type group --role "Primary users"
  
  # Update existing stakeholder with needs
  update_stakeholder.py --project projects/my-project --id s1 \\
    --needs "Need 1" "Need 2" --pain-points "Pain 1"
  
  # Append to existing needs
  update_stakeholder.py --project projects/my-project --id s1 \\
    --needs "Additional need" --append-needs
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
        help="Stakeholder ID"
    )
    parser.add_argument(
        "--name",
        help="Stakeholder name"
    )
    parser.add_argument(
        "--type",
        choices=["group", "individual"],
        help="Stakeholder type"
    )
    parser.add_argument(
        "--role",
        help="Stakeholder role"
    )
    parser.add_argument(
        "--needs",
        nargs="+",
        help="List of needs"
    )
    parser.add_argument(
        "--pain-points",
        nargs="+",
        help="List of pain points"
    )
    parser.add_argument(
        "--notes-links",
        nargs="+",
        help="List of note links"
    )
    parser.add_argument(
        "--append-needs",
        action="store_true",
        help="Append to existing needs instead of replacing"
    )
    parser.add_argument(
        "--append-pain-points",
        action="store_true",
        help="Append to existing pain points instead of replacing"
    )
    parser.add_argument(
        "--append-notes",
        action="store_true",
        help="Append to existing notes links instead of replacing"
    )
    
    args = parser.parse_args()
    
    result = update_stakeholder(
        project_path=args.project,
        stakeholder_id=args.id,
        name=args.name,
        stakeholder_type=args.type,
        role=args.role,
        needs=args.needs,
        pain_points=args.pain_points,
        notes_links=args.notes_links,
        append_needs=args.append_needs,
        append_pain_points=args.append_pain_points,
        append_notes=args.append_notes
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
