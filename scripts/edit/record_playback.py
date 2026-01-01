#!/usr/bin/env python3
"""Record playback session in currentstate.json.

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
            
        # Validate playbacks structure
        if "playbacks" in data:
            for idx, playback in enumerate(data["playbacks"]):
                if not isinstance(playback, dict):
                    return False, f"Playback {idx} is not an object"
                    
                required = ["id", "date", "audience"]
                for field in required:
                    if field not in playback:
                        return False, f"Playback {idx} missing required field: {field}"
                        
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def record_playback(
    project_path: Path,
    playback_id: str,
    date: str,
    audience: list[str],
    phase: str | None = None,
    artifacts_link: str | None = None,
    decisions: list[str] | None = None
) -> Dict[str, Any]:
    """Record a playback session in currentstate.json.
    
    Args:
        project_path: Path to project directory
        playback_id: Unique ID for playback
        date: Date of playback (YYYY-MM-DD format)
        audience: List of attendees
        phase: Phase being presented
        artifacts_link: Link to playback materials
        decisions: List of key decisions or directions
        
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
            
        # Initialize playbacks array if needed
        if "playbacks" not in state:
            state["playbacks"] = []
            
        # Check if playback ID already exists
        for playback in state["playbacks"]:
            if playback["id"] == playback_id:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Playback with id '{playback_id}' already exists"
                }
                
        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {
                "status": "error",
                "data": None,
                "error": f"Invalid date format: {date}. Must be YYYY-MM-DD"
            }
            
        # Create new playback
        new_playback = {
            "id": playback_id,
            "date": date,
            "audience": audience
        }
        
        if phase is not None:
            valid_phases = ["empathize", "define", "ideate", "prototype", "iterate"]
            if phase not in valid_phases:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid phase: {phase}. Must be one of {valid_phases}"
                }
            new_playback["phase"] = phase
            
        if artifacts_link is not None:
            new_playback["artifacts_link"] = artifacts_link
            
        if decisions is not None:
            new_playback["decisions"] = decisions
            
        state["playbacks"].append(new_playback)
        
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
                "playback_id": playback_id,
                "playback": new_playback,
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
            "error": f"Error recording playback: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Record playback session in currentstate.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record simple playback
  record_playback.py --project projects/my-project --id pb1 \\
    --date 2026-01-15 --audience "LT" "Product Team"
  
  # Record playback with decisions
  record_playback.py --project projects/my-project --id pb1 \\
    --date 2026-01-15 --audience "LT" \\
    --phase empathize \\
    --artifacts-link "playbacks/empathize-presentation.md" \\
    --decisions "Proceed to Define phase" "Focus on IC persona"
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
        help="Playback ID"
    )
    parser.add_argument(
        "--date",
        required=True,
        help="Date of playback (YYYY-MM-DD format)"
    )
    parser.add_argument(
        "--audience",
        nargs="+",
        required=True,
        help="List of attendees"
    )
    parser.add_argument(
        "--phase",
        choices=["empathize", "define", "ideate", "prototype", "iterate"],
        help="Phase being presented"
    )
    parser.add_argument(
        "--artifacts-link",
        help="Link to playback materials"
    )
    parser.add_argument(
        "--decisions",
        nargs="+",
        help="List of key decisions or directions"
    )
    
    args = parser.parse_args()
    
    result = record_playback(
        project_path=args.project,
        playback_id=args.id,
        date=args.date,
        audience=args.audience,
        phase=args.phase,
        artifacts_link=args.artifacts_link,
        decisions=args.decisions
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
