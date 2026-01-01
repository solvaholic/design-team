# Custom Tools System

The design team repository uses custom Python scripts for all file operations and state management, enabling use in any environment with shell access and Python—not just VS Code.

## Architecture

### Tool Runner Dispatcher
[scripts/tool_runner.py](../scripts/tool_runner.py) provides a unified CLI interface to all read and edit operations:

```bash
python3 scripts/tool_runner.py --tool TOOL_NAME --params '{"param": "value"}'
```

### Tool Categories

**Read-Only Tools** ([scripts/tools/](../scripts/tools/))
- `read_file` - Read file contents with optional line range
- `search_workspace` - Semantic search across workspace files
- `list_directory` - List directory contents with metadata
- `grep_search` - Regex pattern search with context lines

**Edit Tools** ([scripts/edit/](../scripts/edit/))
- `update_stakeholder` - Add or update stakeholder in currentstate.json
- `grade_assumption` - Grade assumption certainty and risk levels
- `add_insight` - Add insights from research
- `grade_idea` - Grade idea impact and feasibility
- `record_playback` - Record playback sessions with decisions
- `update_phase` - Transition project between design thinking phases

## Standardized JSON Response Format

All tools return consistent JSON responses:

```json
{
  "status": "success|error",
  "data": {
    // Tool-specific result data
  },
  "error": null|"error message"
}
```

### Success Response Example

```json
{
  "status": "success",
  "data": {
    "path": "README.md",
    "content": "# Design Team\n\n...",
    "total_lines": 50
  },
  "error": null
}
```

### Error Response Example

```json
{
  "status": "error",
  "data": null,
  "error": "File not found: /nonexistent/file.txt"
}
```

## Atomic Update Pattern

All edit tools use atomic write operations to prevent data corruption:

1. **Load** existing currentstate.json
2. **Modify** data in memory
3. **Validate** against full schema
4. **Write** to temporary file in same directory
5. **Rename** temporary file to replace original (atomic operation)

If any step fails, the original file remains unchanged.

```python
# Simplified pattern from edit scripts
with tempfile.NamedTemporaryFile(
    mode="w",
    dir=state_file.parent,
    delete=False,
    suffix=".tmp"
) as tmp_file:
    json.dump(state, tmp_file, indent=2)
    tmp_path = Path(tmp_file.name)

# Atomic rename - never leaves file in corrupt state
tmp_path.replace(state_file)
```

## Usage Examples

### Read Operations

#### Read File
```bash
# Read entire file with JSON output
python3 scripts/tool_runner.py --tool read_file --params '{
  "file": "projects/my-project/currentstate.json"
}'

# Read specific line range
python3 scripts/tool_runner.py --tool read_file --params '{
  "file": "README.md",
  "start_line": 1,
  "end_line": 10
}'
```

#### Search Workspace
```bash
# Semantic search across all files
python3 scripts/tool_runner.py --tool search_workspace --params '{
  "query": "design thinking phases",
  "workspace": ".",
  "max_results": 5
}'

# Search with file type filter
python3 scripts/tool_runner.py --tool search_workspace --params '{
  "query": "stakeholder needs",
  "workspace": "projects/my-project",
  "include": ["*.md"],
  "max_results": 10
}'
```

#### List Directory
```bash
# List directory contents
python3 scripts/tool_runner.py --tool list_directory --params '{
  "directory": "projects/my-project/insights"
}'

# Recursive listing with pattern
python3 scripts/tool_runner.py --tool list_directory --params '{
  "directory": "projects",
  "recursive": true,
  "pattern": "*.md"
}'
```

#### Grep Search
```bash
# Search for pattern across files
python3 scripts/tool_runner.py --tool grep_search --params '{
  "pattern": "TODO|FIXME",
  "workspace": ".",
  "file_pattern": "**/*.py"
}'

# Search with context lines
python3 scripts/tool_runner.py --tool grep_search --params '{
  "pattern": "def validate",
  "workspace": "scripts",
  "file_pattern": "*.py",
  "context": 3
}'
```

### Edit Operations

#### Update Stakeholder
```bash
# Add new stakeholder
python3 scripts/tool_runner.py --tool update_stakeholder --params '{
  "project": "projects/my-project",
  "id": "s1",
  "name": "Software Engineers",
  "type": "group",
  "role": "Primary IC users",
  "needs": ["Fast iteration", "Clear documentation"],
  "pain_points": ["Unclear requirements", "Slow feedback loops"]
}'

# Append to existing stakeholder needs
python3 scripts/tool_runner.py --tool update_stakeholder --params '{
  "project": "projects/my-project",
  "id": "s1",
  "needs": ["Better tooling"],
  "append_needs": true
}'
```

#### Grade Assumption
```bash
# Grade assumption certainty and risk
python3 scripts/tool_runner.py --tool grade_assumption --params '{
  "project": "projects/my-project",
  "id": "a1",
  "certainty": "low",
  "risk": "high",
  "status": "validating"
}'

# Add validation plan
python3 scripts/tool_runner.py --tool grade_assumption --params '{
  "project": "projects/my-project",
  "id": "a1",
  "validation_plan": "Interview 10 users about their current workflow"
}'
```

#### Add Insight
```bash
# Add research insight
python3 scripts/tool_runner.py --tool add_insight --params '{
  "project": "projects/my-project",
  "id": "i1",
  "title": "Users prioritize speed over features",
  "description": "All 12 interviewed users mentioned wanting faster response times",
  "confidence": "high",
  "sources": ["insights/interview-1.md", "insights/interview-2.md"],
  "implications": "Focus prototype on performance optimizations"
}'
```

#### Grade Idea
```bash
# Grade solution idea
python3 scripts/tool_runner.py --tool grade_idea --params '{
  "project": "projects/my-project",
  "id": "idea1",
  "impact": "high",
  "feasibility": "medium",
  "status": "prototyping"
}'

# Link prototype iterations
python3 scripts/tool_runner.py --tool grade_idea --params '{
  "project": "projects/my-project",
  "id": "idea1",
  "prototype_links": ["ideas/prototype-v1.md"],
  "append_prototype_links": true
}'
```

#### Record Playback
```bash
# Record leadership playback
python3 scripts/tool_runner.py --tool record_playback --params '{
  "project": "projects/my-project",
  "id": "pb1",
  "date": "2026-01-15",
  "audience": ["Pat", "Casey", "Morgan"],
  "phase": "empathize",
  "artifacts_link": "playbacks/empathize-presentation.md",
  "decisions": ["Proceed to Define phase", "Focus on IC persona"]
}'
```

#### Update Phase
```bash
# Transition to next phase
python3 scripts/tool_runner.py --tool update_phase --params '{
  "project": "projects/my-project",
  "phase": "define"
}'
```

## Using Params Files

For complex operations, save parameters to a JSON file:

```bash
# Create params file
cat > params.json << 'EOF'
{
  "project": "projects/my-project",
  "id": "s2",
  "name": "Customer Support Team",
  "type": "group",
  "role": "Secondary stakeholders",
  "needs": [
    "Quick resolution paths",
    "Clear escalation procedures"
  ],
  "pain_points": [
    "Incomplete documentation",
    "Slow response from engineering"
  ]
}
EOF

# Use params file
python3 scripts/tool_runner.py --tool update_stakeholder --params-file params.json
```

## Listing Available Tools

```bash
python3 scripts/tool_runner.py --list
```

Output:
```json
{
  "status": "success",
  "data": {
    "tools": [
      {
        "name": "read_file",
        "type": "read",
        "description": "Read file contents with optional line range",
        "script": "tools/read_file.py"
      },
      // ... all other tools
    ],
    "total": 10
  },
  "error": null
}
```

## Tool Development

### Adding New Tools

1. **Create script** in `scripts/tools/` (read) or `scripts/edit/` (edit)
2. **Implement standardized response format** with `{"status", "data", "error"}`
3. **Add to tool registry** in `scripts/tool_runner.py`
4. **Document positional arguments** if needed
5. **Test** via tool_runner.py
6. **Update this documentation**

### Edit Tool Requirements

All edit tools must:
- Load and modify currentstate.json
- Validate against schema before writing
- Use atomic write pattern (tempfile + rename)
- Update `updated_at` timestamp
- Return standardized JSON response

### Example Template

```python
#!/usr/bin/env python3
"""Tool description."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

def my_tool_function(param: str) -> Dict[str, Any]:
    """Function description.
    
    Args:
        param: Parameter description
        
    Returns:
        Standardized result dictionary
    """
    try:
        # Tool logic here
        result_data = {"key": "value"}
        
        return {
            "status": "success",
            "data": result_data,
            "error": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "error": f"Error: {e}"
        }

def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("param", help="Parameter help")
    args = parser.parse_args()
    
    result = my_tool_function(args.param)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "success" else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Integration with Agents

Agents access tools via shell commands:

```markdown
# In agent .md files
tools:
  - execute  # Use for running scripts/tool_runner.py
```

Example usage in agent context:
```bash
# Read project state
python3 scripts/tool_runner.py --tool read_file --params '{"file": "projects/my-project/currentstate.json"}'

# Update stakeholder
python3 scripts/tool_runner.py --tool update_stakeholder --params '{"project": "projects/my-project", "id": "s1", "name": "Engineers", "type": "group"}'
```

## Error Handling

Tools return non-zero exit codes on failure and always output JSON:

```bash
# Successful operation
python3 scripts/tool_runner.py --tool read_file --params '{"file": "README.md"}'
echo $?  # 0

# Failed operation
python3 scripts/tool_runner.py --tool read_file --params '{"file": "/nonexistent"}'
echo $?  # 1
```

Parse the JSON response to check status:
```bash
result=$(python3 scripts/tool_runner.py --tool read_file --params '{"file": "README.md"}')
status=$(echo "$result" | jq -r '.status')

if [ "$status" = "success" ]; then
    echo "Success!"
else
    echo "Error: $(echo "$result" | jq -r '.error')"
fi
```

## Schema Validation

Edit tools validate currentstate.json against [schemas/currentstate.schema.json](../schemas/currentstate.schema.json) before writing:

- Checks required fields (project_name, created_at, updated_at, phase)
- Validates enum values (phases, certainty, risk, status, etc.)
- Validates nested object structures (assumptions, stakeholders, insights, ideas, playbacks)
- Ensures data type correctness

Failed validation returns an error without modifying the file.

## Performance Considerations

- **Search operations** may be slow on large workspaces; use specific directories and file patterns
- **Full schema validation** on every edit ensures integrity but adds ~10-50ms overhead
- **Atomic writes** require disk space for temporary file (typically same size as currentstate.json)
- **Tool_runner.py dispatch** adds ~50-100ms subprocess overhead vs direct script calls

For performance-critical batch operations, consider calling scripts directly instead of via tool_runner.py.

## See Also

- [Workflow Documentation](WORKFLOW.md) - Design thinking process flows
- [Data Structures](DATA_STRUCTURES.md) - currentstate.json schema details
- [Integration Guide](INTEGRATION.md) - Agent and skill integration patterns
