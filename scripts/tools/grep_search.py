#!/usr/bin/env python3
"""Search file contents using regex patterns (like grep).

Returns matching lines with context in standardized JSON format.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import re


def grep_search(
    pattern: str,
    file_paths: List[Path] | None = None,
    workspace_path: Path | None = None,
    file_pattern: str | None = None,
    context_lines: int = 0,
    case_sensitive: bool = False,
    max_results: int = 100
) -> Dict[str, Any]:
    """Search files for regex pattern matches.
    
    Args:
        pattern: Regex pattern to search for
        file_paths: Specific file paths to search
        workspace_path: Workspace root to search recursively
        file_pattern: Glob pattern for files to search in workspace
        context_lines: Number of context lines before/after match
        case_sensitive: Whether search is case-sensitive
        max_results: Maximum number of matches to return
        
    Returns:
        Standardized result dictionary with status, data, and error fields
    """
    try:
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            return {
                "status": "error",
                "data": None,
                "error": f"Invalid regex pattern: {e}"
            }
            
        # Determine files to search
        search_files = []
        
        if file_paths:
            search_files = file_paths
        elif workspace_path:
            if not workspace_path.exists() or not workspace_path.is_dir():
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Invalid workspace path: {workspace_path}"
                }
                
            # Default file pattern if not specified
            if file_pattern is None:
                file_pattern = "**/*"
                
            search_files = [
                f for f in workspace_path.glob(file_pattern)
                if f.is_file() and not any(
                    part.startswith(".") or part in ["__pycache__", "node_modules", "venv"]
                    for part in f.parts
                )
            ]
        else:
            return {
                "status": "error",
                "data": None,
                "error": "Must specify either file_paths or workspace_path"
            }
            
        if not search_files:
            return {
                "status": "success",
                "data": {
                    "pattern": pattern,
                    "matches": [],
                    "total_matches": 0,
                    "files_searched": 0
                },
                "error": None
            }
            
        # Search files
        all_matches = []
        files_with_matches = 0
        
        for file_path in search_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.splitlines()
                
                file_matches = []
                
                for line_num, line in enumerate(lines, start=1):
                    if regex.search(line):
                        match_data = {
                            "line_number": line_num,
                            "line": line,
                            "context_before": [],
                            "context_after": []
                        }
                        
                        # Add context lines
                        if context_lines > 0:
                            start = max(0, line_num - context_lines - 1)
                            end = min(len(lines), line_num + context_lines)
                            
                            match_data["context_before"] = [
                                {"line_number": i + 1, "line": lines[i]}
                                for i in range(start, line_num - 1)
                            ]
                            
                            match_data["context_after"] = [
                                {"line_number": i + 1, "line": lines[i]}
                                for i in range(line_num, end)
                            ]
                            
                        file_matches.append(match_data)
                        
                        if len(all_matches) + len(file_matches) >= max_results:
                            break
                            
                if file_matches:
                    files_with_matches += 1
                    relative_path = file_path.relative_to(workspace_path) if workspace_path else file_path
                    all_matches.append({
                        "file": str(relative_path),
                        "matches": file_matches
                    })
                    
                if len(all_matches) >= max_results:
                    break
                    
            except (UnicodeDecodeError, PermissionError):
                # Skip files we can't read
                continue
                
        return {
            "status": "success",
            "data": {
                "pattern": pattern,
                "case_sensitive": case_sensitive,
                "matches": all_matches,
                "total_matches": sum(len(m["matches"]) for m in all_matches),
                "files_with_matches": files_with_matches,
                "files_searched": len(search_files)
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Search error: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Search files for regex pattern matches (grep-like)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search specific file
  grep_search.py "TODO" main.py
  
  # Search all Python files in workspace
  grep_search.py "class.*:" --workspace . --file-pattern "**/*.py"
  
  # Case-sensitive search with context
  grep_search.py "ERROR" --case-sensitive --context 2 --workspace .
"""
    )
    parser.add_argument(
        "pattern",
        help="Regex pattern to search for"
    )
    parser.add_argument(
        "files",
        type=Path,
        nargs="*",
        help="Specific files to search"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root to search recursively"
    )
    parser.add_argument(
        "--file-pattern",
        help="Glob pattern for files to search (used with --workspace)"
    )
    parser.add_argument(
        "-C", "--context",
        type=int,
        default=0,
        help="Number of context lines to show before and after match"
    )
    parser.add_argument(
        "-i", "--case-sensitive",
        action="store_true",
        help="Make search case-sensitive (default: case-insensitive)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of matches to return (default: 100)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (default: human-readable)"
    )
    
    args = parser.parse_args()
    
    result = grep_search(
        pattern=args.pattern,
        file_paths=args.files if args.files else None,
        workspace_path=args.workspace,
        file_pattern=args.file_pattern,
        context_lines=args.context,
        case_sensitive=args.case_sensitive,
        max_results=args.max_results
    )
    
    if args.json or result["status"] == "error":
        # Always output JSON for errors, or when explicitly requested
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "success" else 1
    else:
        # Human-readable output (grep-like)
        data = result["data"]
        
        if data["total_matches"] == 0:
            print(f"No matches found for pattern: {data['pattern']}")
            return 1
            
        print(f"Found {data['total_matches']} matches in {data['files_with_matches']} files:\n")
        
        for file_match in data["matches"]:
            print(f"\n{file_match['file']}:")
            for match in file_match["matches"]:
                print(f"  Line {match['line_number']}: {match['line']}")
                
        return 0


if __name__ == "__main__":
    sys.exit(main())
