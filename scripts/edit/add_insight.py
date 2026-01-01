#!/usr/bin/env python3
"""Add insight to currentstate.json.

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
            
        # Validate insights structure
        if "insights" in data:
            for idx, insight in enumerate(data["insights"]):
                if not isinstance(insight, dict):
                    return False, f"Insight {idx} is not an object"
                    
                required = ["id", "title", "description"]
                for field in required:
                    if field not in insight:
                        return False, f"Insight {idx} missing required field: {field}"
                        
                if "confidence" in insight and insight["confidence"] not in ["high", "medium", "low"]:
                    return False, f"Insight {idx} has invalid confidence: {insight['confidence']}"
                    
        return True, None
        
    except Exception as e:
        return False, f"Validation error: {e}"


def add_insight(
    project_path: Path,
    insight_id: str,
    title: str,
    description: str,
    confidence: str | None = None,
    sources: list[str] | None = None,
    implications: str | None = None
) -> Dict[str, Any]:
    """Add an insight to currentstate.json.
    
    Args:
        project_path: Path to project directory
        insight_id: Unique ID for insight
        title: Short title for the insight
        description: The insight itself
        confidence: Confidence level (high, medium, low)
        sources: List of source links
        implications: What this means for the design
        
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
            
        # Initialize insights array if needed
        if "insights" not in state:
            state["insights"] = []
            
        # Check if insight ID already exists
        for insight in state["insights"]:
            if insight["id"] == insight_id:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Insight with id '{insight_id}' already exists"
                }
                
        # Create new insight
        new_insight = {
            "id": insight_id,
            "title": title,
            "description": description
        }
        
        if confidence is not None:
            if confidence not in ["high", "medium", "low"]:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid confidence: {confidence}. Must be high, medium, or low"
                }
            new_insight["confidence"] = confidence
            
        if sources is not None:
            new_insight["sources"] = sources
            
        if implications is not None:
            new_insight["implications"] = implications
            
        state["insights"].append(new_insight)
        
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
                "insight_id": insight_id,
                "insight": new_insight,
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
            "error": f"Error adding insight: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Add insight to currentstate.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add insight with confidence
  add_insight.py --project projects/my-project --id i1 \\
    --title "Key Finding" \\
    --description "Users need X because Y" \\
    --confidence high
  
  # Add insight with sources and implications
  add_insight.py --project projects/my-project --id i2 \\
    --title "Pattern Discovered" \\
    --description "All users mentioned Z" \\
    --sources "insights/interview-1.md" "insights/interview-2.md" \\
    --implications "This suggests we should focus on Z"
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
        help="Insight ID"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Short title for the insight"
    )
    parser.add_argument(
        "--description",
        required=True,
        help="The insight itself"
    )
    parser.add_argument(
        "--confidence",
        choices=["high", "medium", "low"],
        help="Confidence level"
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        help="List of source links"
    )
    parser.add_argument(
        "--implications",
        help="What this means for the design"
    )
    
    args = parser.parse_args()
    
    result = add_insight(
        project_path=args.project,
        insight_id=args.id,
        title=args.title,
        description=args.description,
        confidence=args.confidence,
        sources=args.sources,
        implications=args.implications
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
