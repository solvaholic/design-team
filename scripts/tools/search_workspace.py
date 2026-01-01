#!/usr/bin/env python3
"""Semantic workspace search using keyword matching and file content scoring.

Searches workspace files for relevant content based on query terms.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import re


def calculate_relevance_score(content: str, query_terms: List[str]) -> float:
    """Calculate relevance score for content based on query terms.
    
    Args:
        content: File content to score
        query_terms: List of search terms
        
    Returns:
        Relevance score (0.0 to 1.0)
    """
    content_lower = content.lower()
    scores = []
    
    for term in query_terms:
        term_lower = term.lower()
        # Count occurrences
        count = content_lower.count(term_lower)
        # Bonus for term in first 500 chars
        first_part = content_lower[:500]
        if term_lower in first_part:
            count += 2
        scores.append(min(count, 10))  # Cap at 10 to prevent domination by repeated terms
        
    if not scores:
        return 0.0
        
    # Normalize score
    avg_score = sum(scores) / len(scores)
    return min(avg_score / 10.0, 1.0)


def search_workspace(
    workspace_path: Path,
    query: str,
    file_patterns: List[str] | None = None,
    exclude_patterns: List[str] | None = None,
    max_results: int = 20
) -> Dict[str, Any]:
    """Search workspace for files matching query.
    
    Args:
        workspace_path: Root path to search
        query: Search query string
        file_patterns: List of glob patterns to include (e.g., ["*.md", "*.json"])
        exclude_patterns: List of patterns to exclude (e.g., ["**/node_modules/**"])
        max_results: Maximum number of results to return
        
    Returns:
        Standardized result dictionary with status, data, and error fields
    """
    try:
        if not workspace_path.exists():
            return {
                "status": "error",
                "data": None,
                "error": f"Workspace path not found: {workspace_path}"
            }
            
        if not workspace_path.is_dir():
            return {
                "status": "error",
                "data": None,
                "error": f"Workspace path is not a directory: {workspace_path}"
            }
            
        # Parse query into terms
        query_terms = query.split()
        
        # Default patterns
        if file_patterns is None:
            file_patterns = ["*.md", "*.json", "*.py", "*.txt"]
            
        if exclude_patterns is None:
            exclude_patterns = [
                "**/__pycache__/**",
                "**/.git/**",
                "**/node_modules/**",
                "**/.venv/**",
                "**/venv/**"
            ]
            
        # Compile exclude patterns
        exclude_regexes = [
            re.compile(pattern.replace("**", ".*").replace("*", "[^/]*"))
            for pattern in exclude_patterns
        ]
        
        # Find matching files
        results = []
        
        for pattern in file_patterns:
            for file_path in workspace_path.rglob(pattern):
                if not file_path.is_file():
                    continue
                    
                # Check exclusions
                relative_path = file_path.relative_to(workspace_path)
                if any(regex.search(str(relative_path)) for regex in exclude_regexes):
                    continue
                    
                try:
                    content = file_path.read_text(encoding="utf-8")
                    score = calculate_relevance_score(content, query_terms)
                    
                    if score > 0:
                        # Extract snippet with context
                        snippet = ""
                        for term in query_terms:
                            match = re.search(
                                f".{{0,50}}{re.escape(term)}.{{0,50}}",
                                content,
                                re.IGNORECASE
                            )
                            if match:
                                snippet = match.group(0)
                                break
                                
                        results.append({
                            "path": str(relative_path),
                            "score": score,
                            "snippet": snippet.strip() if snippet else content[:100]
                        })
                        
                except (UnicodeDecodeError, PermissionError):
                    # Skip files we can't read
                    continue
                    
        # Sort by relevance and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:max_results]
        
        return {
            "status": "success",
            "data": {
                "query": query,
                "results": results,
                "total_found": len(results)
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
        description="Search workspace for files matching query",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "query",
        help="Search query string"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root path (default: current directory)"
    )
    parser.add_argument(
        "--include",
        action="append",
        help="File pattern to include (can specify multiple times)"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Pattern to exclude (can specify multiple times)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=20,
        help="Maximum number of results to return (default: 20)"
    )
    
    args = parser.parse_args()
    
    result = search_workspace(
        args.workspace,
        args.query,
        file_patterns=args.include,
        exclude_patterns=args.exclude,
        max_results=args.max_results
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
