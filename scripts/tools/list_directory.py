#!/usr/bin/env python3
"""List directory contents with optional filtering and sorting.

Returns directory contents in standardized JSON format.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import re


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 KB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def list_directory(
    dir_path: Path,
    recursive: bool = False,
    include_hidden: bool = False,
    pattern: str | None = None
) -> Dict[str, Any]:
    """List directory contents.
    
    Args:
        dir_path: Path to directory to list
        recursive: Whether to list recursively
        include_hidden: Whether to include hidden files/directories
        pattern: Optional glob pattern to filter results
        
    Returns:
        Standardized result dictionary with status, data, and error fields
    """
    try:
        if not dir_path.exists():
            return {
                "status": "error",
                "data": None,
                "error": f"Directory not found: {dir_path}"
            }
            
        if not dir_path.is_dir():
            return {
                "status": "error",
                "data": None,
                "error": f"Path is not a directory: {dir_path}"
            }
            
        entries = []
        
        # Determine iteration method
        if recursive:
            if pattern:
                iterator = dir_path.rglob(pattern)
            else:
                iterator = dir_path.rglob("*")
        else:
            if pattern:
                iterator = dir_path.glob(pattern)
            else:
                iterator = dir_path.iterdir()
                
        for entry in sorted(iterator):
            # Skip hidden files unless requested
            if not include_hidden and entry.name.startswith("."):
                continue
                
            try:
                stat = entry.stat()
                entry_info = {
                    "name": entry.name,
                    "path": str(entry.relative_to(dir_path)),
                    "type": "directory" if entry.is_dir() else "file",
                    "size": stat.st_size,
                    "size_formatted": format_size(stat.st_size),
                    "modified": stat.st_mtime
                }
                
                # For files, add extension
                if entry.is_file():
                    entry_info["extension"] = entry.suffix
                    
                entries.append(entry_info)
                
            except (OSError, PermissionError):
                # Skip entries we can't access
                continue
                
        # Separate directories and files for better organization
        directories = [e for e in entries if e["type"] == "directory"]
        files = [e for e in entries if e["type"] == "file"]
        
        return {
            "status": "success",
            "data": {
                "path": str(dir_path),
                "entries": directories + files,
                "summary": {
                    "total": len(entries),
                    "directories": len(directories),
                    "files": len(files)
                }
            },
            "error": None
        }
        
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Error listing directory: {e}"
        }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="List directory contents with optional filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Directory to list (default: current directory)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="List directories recursively"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Include hidden files and directories"
    )
    parser.add_argument(
        "-p", "--pattern",
        help="Glob pattern to filter results (e.g., '*.md')"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (default: human-readable)"
    )
    
    args = parser.parse_args()
    
    result = list_directory(
        args.directory,
        recursive=args.recursive,
        include_hidden=args.all,
        pattern=args.pattern
    )
    
    if args.json or result["status"] == "error":
        # Always output JSON for errors, or when explicitly requested
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "success" else 1
    else:
        # Human-readable output
        data = result["data"]
        print(f"Directory: {data['path']}")
        print(f"Total: {data['summary']['total']} entries ({data['summary']['directories']} dirs, {data['summary']['files']} files)\n")
        
        for entry in data["entries"]:
            type_indicator = "/" if entry["type"] == "directory" else ""
            size_str = "" if entry["type"] == "directory" else f" ({entry['size_formatted']})"
            print(f"  {entry['name']}{type_indicator}{size_str}")
            
        return 0


if __name__ == "__main__":
    sys.exit(main())
