#!/usr/bin/env python3
"""Grade or update assumption in currentstate.json.

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
            
        # Validate assumptions structure
        if "assumptions" in data:
            for idx, assumption in enumerate(data["assumptions"]):
                if not isinstance(assumption, dict):
                    return False, f"Assumption {idx} is not an object"
                    
                required = ["id", "description", "certainty", "risk"]
                for field in required:
                    if field not in assumption:
                        return False, f"Assumption {idx} missing required field: {field}"
                        
                for grade_field in ["certainty", "risk"]:
                    if assumption[grade_field] not in ["high", "medium", "low"]:
                        return False, f"Assumption {idx} has invalid {grade_field}: {assumption[grade_field]}"
                        
                if "status" in assumption and assumption["status"] not in ["open", "validating", "validated", "invalidated"]:
                    return False, f"Assumption {idx} has invalid status: {assumption['status']}"
                    
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def grade_assumption(
    project_path: Path,
    assumption_id: str,
    certainty: str | None = None,
    risk: str | None = None,
    validation_plan: str | None = None,
    status: str | None = None
) -> Dict[str, Any]:
    """Grade or update an assumption in currentstate.json.
    
    Args:
        project_path: Path to project directory
        assumption_id: Unique ID for assumption
        certainty: Certainty level (high, medium, low)
        risk: Risk level (high, medium, low)
        validation_plan: How to validate the assumption
        status: Status (open, validating, validated, invalidated)
        
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
            
        # Find assumption
        if "assumptions" not in state:
            return {
                "status": "error",
                "data": None,
                "error": "No assumptions array found in currentstate.json"
            }
            
        assumption = None
        for a in state["assumptions"]:
            if a["id"] == assumption_id:
                assumption = a
                break
                
        if assumption is None:
            return {
                "status": "error",
                "data": None,
                "error": f"Assumption with id '{assumption_id}' not found"
            }
            
        # Update fields
        if certainty is not None:
            if certainty not in ["high", "medium", "low"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid certainty: {certainty}. Must be high, medium, or low"
                }
            assumption["certainty"] = certainty
            
        if risk is not None:
            if risk not in ["high", "medium", "low"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid risk: {risk}. Must be high, medium, or low"
                }
            assumption["risk"] = risk
            
        if validation_plan is not None:
            assumption["validation_plan"] = validation_plan
            
        if status is not None:
            if status not in ["open", "validating", "validated", "invalidated"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid status: {status}. Must be open, validating, validated, or invalidated"
                }
            assumption["status"] = status
            
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
                "assumption_id": assumption_id,
                "assumption": assumption,
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
            "error": f"Error grading assumption: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Grade or update assumption in currentstate.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Grade certainty and risk
  grade_assumption.py --project projects/my-project --id a1 \\
    --certainty low --risk high
  
  # Add validation plan
  grade_assumption.py --project projects/my-project --id a1 \\
    --validation-plan "Interview 10 users"
  
  # Update status
  grade_assumption.py --project projects/my-project --id a1 \\
    --status validating
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
        help="Assumption ID"
    )
    parser.add_argument(
        "--certainty",
        choices=["high", "medium", "low"],
        help="Certainty level"
    )
    parser.add_argument(
        "--risk",
        choices=["high", "medium", "low"],
        help="Risk level"
    )
    parser.add_argument(
        "--validation-plan",
        help="Validation plan description"
    )
    parser.add_argument(
        "--status",
        choices=["open", "validating", "validated", "invalidated"],
        help="Assumption status"
    )
    
    args = parser.parse_args()
    
    result = grade_assumption(
        project_path=args.project,
        assumption_id=args.id,
        certainty=args.certainty,
        risk=args.risk,
        validation_plan=args.validation_plan,
        status=args.status
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
