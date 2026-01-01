#!/usr/bin/env python3
"""Unified tool dispatcher for read and edit operations.

Routes tool invocations to appropriate scripts and provides standardized responses.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


# Tool registry mapping tool names to scripts
TOOL_REGISTRY = {
    # Read-only tools
    "read_file": {
        "script": "tools/read_file.py",
        "description": "Read file contents with optional line range",
        "positional": ["file"]  # file is a positional argument
    },
    "search_workspace": {
        "script": "tools/search_workspace.py",
        "description": "Search workspace for files matching query",
        "positional": ["query"]  # query is a positional argument
    },
    "list_directory": {
        "script": "tools/list_directory.py",
        "description": "List directory contents",
        "positional": ["directory"]  # directory is optional positional
    },
    "grep_search": {
        "script": "tools/grep_search.py",
        "description": "Search files for regex pattern matches",
        "positional": ["pattern"]  # pattern is a positional argument
    },
    
    # Edit tools
    "update_stakeholder": {
        "script": "edit/update_stakeholder.py",
        "description": "Add or update stakeholder in currentstate.json"
    },
    "grade_assumption": {
        "script": "edit/grade_assumption.py",
        "description": "Grade or update assumption in currentstate.json"
    },
    "add_insight": {
        "script": "edit/add_insight.py",
        "description": "Add insight to currentstate.json"
    },
    "grade_idea": {
        "script": "edit/grade_idea.py",
        "description": "Grade or update idea in currentstate.json"
    },
    "record_playback": {
        "script": "edit/record_playback.py",
        "description": "Record playback session in currentstate.json"
    },
    "update_phase": {
        "script": "edit/update_phase.py",
        "description": "Update project phase in currentstate.json"
    }
}


def build_command_args(tool_name: str, params: Dict[str, Any], tool_info: Dict[str, Any]) -> List[str]:
    """Build command line arguments from parameters dictionary.
    
    Args:
        tool_name: Name of tool to invoke
        params: Dictionary of parameters
        tool_info: Tool registry information
        
    Returns:
        List of command arguments
    """
    args = []
    positional_params = tool_info.get("positional", [])
    params_copy = params.copy()
    
    # Handle positional arguments first
    for pos_param in positional_params:
        if pos_param in params_copy:
            value = params_copy.pop(pos_param)
            if isinstance(value, list):
                args.extend(str(v) for v in value)
            else:
                args.append(str(value))
    
    # Handle remaining named arguments
    for key, value in params_copy.items():
        # Convert parameter names from snake_case/camelCase to kebab-case
        arg_name = key.replace("_", "-")
        
        if isinstance(value, bool):
            # Boolean flags
            if value:
                args.append(f"--{arg_name}")
        elif isinstance(value, list):
            # List arguments
            args.append(f"--{arg_name}")
            args.extend(str(v) for v in value)
        else:
            # Regular arguments
            args.append(f"--{arg_name}")
            args.append(str(value))
            
    return args


def run_tool(
    tool_name: str,
    params: Dict[str, Any],
    scripts_dir: Path | None = None
) -> Dict[str, Any]:
    """Run a tool with given parameters.
    
    Args:
        tool_name: Name of tool to run
        params: Dictionary of parameters for the tool
        scripts_dir: Path to scripts directory (defaults to script location)
        
    Returns:
        Standardized result dictionary
    """
    try:
        # Validate tool exists
        if tool_name not in TOOL_REGISTRY:
            available = ", ".join(sorted(TOOL_REGISTRY.keys()))
            return {
                "status": "error",
                "data": None,
                "error": f"Unknown tool: {tool_name}. Available tools: {available}"
            }
            
        # Determine scripts directory
        if scripts_dir is None:
            scripts_dir = Path(__file__).parent
            
        tool_info = TOOL_REGISTRY[tool_name]
        script_path = scripts_dir / tool_info["script"]
        
        if not script_path.exists():
            return {
                "status": "error",
                "data": None,
                "error": f"Tool script not found: {script_path}"
            }
            
        # Build command
        cmd_args = build_command_args(tool_name, params, tool_info)
        
        # For read_file, list_directory, and grep_search, force JSON output
        if tool_name in ["read_file", "list_directory", "grep_search"]:
            if "--json" not in cmd_args and "json" not in params:
                cmd_args.append("--json")
        
        cmd = [sys.executable, str(script_path)] + cmd_args
        
        # Execute tool
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Parse JSON output
        try:
            output = json.loads(result.stdout)
            
            # Ensure standardized format
            if not isinstance(output, dict) or "status" not in output:
                return {
                    "status": "error",
                    "data": None,
                    "error": f"Tool returned invalid response format"
                }
                
            return output
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw output as error
            return {
                "status": "error",
                "data": None,
                "error": f"Tool output is not valid JSON: {e}\nOutput: {result.stdout[:500]}"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "data": None,
            "error": f"Tool execution timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Error running tool: {e}"
        }


def list_tools() -> Dict[str, Any]:
    """List all available tools.
    
    Returns:
        Standardized result dictionary with tool information
    """
    tools = []
    for name, info in sorted(TOOL_REGISTRY.items()):
        tool_type = "edit" if "edit/" in info["script"] else "read"
        tools.append({
            "name": name,
            "type": tool_type,
            "description": info["description"],
            "script": info["script"]
        })
        
    return {
        "status": "success",
        "data": {
            "tools": tools,
            "total": len(tools)
        },
        "error": None
    }


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Unified tool dispatcher for design team operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tool invocation methods:

1. Using --tool and --params:
   tool_runner.py --tool read_file --params '{"file": "README.md", "start_line": 1, "end_line": 10}'

2. Using --tool and --params-file:
   tool_runner.py --tool update_stakeholder --params-file params.json

3. List available tools:
   tool_runner.py --list

Examples:
  # Read a file
  tool_runner.py --tool read_file --params '{"file": "README.md"}'
  
  # Search workspace
  tool_runner.py --tool search_workspace --params '{"query": "design thinking"}'
  
  # Update stakeholder
  tool_runner.py --tool update_stakeholder --params '{
    "project": "projects/my-project",
    "id": "s1",
    "name": "Engineers",
    "type": "group"
  }'
  
  # Grade assumption
  tool_runner.py --tool grade_assumption --params '{
    "project": "projects/my-project",
    "id": "a1",
    "certainty": "low",
    "risk": "high"
  }'
"""
    )
    
    parser.add_argument(
        "--tool",
        help="Name of tool to run"
    )
    parser.add_argument(
        "--params",
        help="JSON string of parameters"
    )
    parser.add_argument(
        "--params-file",
        type=Path,
        help="Path to JSON file containing parameters"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available tools"
    )
    parser.add_argument(
        "--scripts-dir",
        type=Path,
        help="Path to scripts directory (default: script location)"
    )
    
    args = parser.parse_args()
    
    # List tools mode
    if args.list:
        result = list_tools()
        print(json.dumps(result, indent=2))
        return 0
        
    # Validate required arguments
    if not args.tool:
        parser.error("--tool is required (or use --list to see available tools)")
        
    if not args.params and not args.params_file:
        parser.error("Either --params or --params-file is required")
        
    # Parse parameters
    try:
        if args.params_file:
            with open(args.params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        else:
            params = json.loads(args.params)
            
        if not isinstance(params, dict):
            print(json.dumps({
                "status": "error",
                "data": None,
                "error": "Parameters must be a JSON object"
            }, indent=2))
            return 1
            
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "data": None,
            "error": f"Invalid JSON in parameters: {e}"
        }, indent=2))
        return 1
    except FileNotFoundError:
        print(json.dumps({
            "status": "error",
            "data": None,
            "error": f"Parameters file not found: {args.params_file}"
        }, indent=2))
        return 1
        
    # Run tool
    result = run_tool(args.tool, params, scripts_dir=args.scripts_dir)
    
    # Output result
    print(json.dumps(result, indent=2))
    
    # Return appropriate exit code
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
