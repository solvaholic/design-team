#!/usr/bin/env python3
"""Read file contents with optional line range support.

Returns file contents in standardized JSON format.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


def read_file(file_path: Path, start_line: int | None = None, end_line: int | None = None) -> Dict[str, Any]:
    """Read file contents, optionally limiting to specific line range.
    
    Args:
        file_path: Path to file to read
        start_line: Starting line number (1-indexed, inclusive)
        end_line: Ending line number (1-indexed, inclusive)
        
    Returns:
        Standardized result dictionary with status, data, and error fields
    """
    try:
        if not file_path.exists():
            return {
                "status": "error",
                "data": None,
                "error": f"File not found: {file_path}"
            }
            
        if not file_path.is_file():
            return {
                "status": "error",
                "data": None,
                "error": f"Path is not a file: {file_path}"
            }
            
        # Read file contents
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        
        # Apply line range if specified
        if start_line is not None or end_line is not None:
            start_idx = (start_line - 1) if start_line else 0
            end_idx = end_line if end_line else len(lines)
            
            if start_idx < 0 or start_idx >= len(lines):
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Start line {start_line} out of range (file has {len(lines)} lines)"
                }
                
            if end_idx < start_idx or end_idx > len(lines):
                return {
                    "status": "error",
                    "data": None,
                    "error": f"End line {end_line} out of range (file has {len(lines)} lines)"
                }
                
            lines = lines[start_idx:end_idx]
            content = "".join(lines)
            
        return {
            "status": "success",
            "data": {
                "path": str(file_path),
                "content": content,
                "total_lines": len(lines),
                "start_line": start_line or 1,
                "end_line": end_line or len(lines)
            },
            "error": None
        }
        
    except UnicodeDecodeError as e:
        return {
            "status": "error",
            "data": None,
            "error": f"File encoding error: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Unexpected error reading file: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Read file contents with optional line range",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to file to read"
    )
    parser.add_argument(
        "--start-line",
        type=int,
        help="Starting line number (1-indexed, inclusive)"
    )
    parser.add_argument(
        "--end-line",
        type=int,
        help="Ending line number (1-indexed, inclusive)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (default: plain text)"
    )
    
    args = parser.parse_args()
    
    result = read_file(args.file, args.start_line, args.end_line)
    
    if args.json or result["status"] == "error":
        # Always output JSON for errors, or when explicitly requested
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "success" else 1
    else:
        # Plain text output for successful reads
        print(result["data"]["content"], end="")
        return 0


if __name__ == "__main__":
    sys.exit(main())
