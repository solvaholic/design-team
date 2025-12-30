# Design Team - Data Structures

This document explains the core data structures used by the Design Team system to track projects through the design thinking process.

## Overview

The Design Team system uses a combination of structured JSON data and markdown templates to maintain state throughout a design project's lifecycle. This enables both humans and AI agents to understand, track, and guide the design process.

## Directory Structure

```
design-team/
├── schemas/                         # JSON schemas for validation
│   └── currentstate.schema.json     # Schema for project state
├── templates/                       # Templates for new content
│   ├── project/                     # Complete project template
│   │   ├── currentstate.json        # Project state template
│   │   ├── insights/                # Research artifacts
│   │   ├── ideas/                   # Solution concepts
│   │   └── playbacks/               # Presentation materials
│   ├── insights/                    # Research templates
│   │   ├── observation_template.md
│   │   ├── interview_template.md
│   │   └── research_synthesis_template.md
│   ├── ideas/                       # Idea templates
│   │   ├── idea_template.md
│   │   └── prototype_template.md
│   └── playbacks/                   # Playback template
│       └── playback_template.md
└── projects/                        # Active projects (created by users)
    └── [project_name]/
        ├── currentstate.json
        ├── insights/
        ├── ideas/
        └── playbacks/
```

## Core Data Structure: currentstate.json

The `currentstate.json` file is the **central index** of a project's state. It tracks:

### 1. Project Metadata
- **project_name**: Human-readable project identifier
- **created_at**: Timestamp of project creation
- **updated_at**: Last modification timestamp
- **phase**: Current design thinking phase (empathize, define, ideate, prototype, iterate)
- **description**: Brief problem space description

### 2. Assumptions
Array of key assumptions with:
- Unique ID
- Description of the assumption
- **Certainty**: high | medium | low (confidence level)
- **Risk**: high | medium | low (impact if wrong)
- Validation plan
- Status: open | validating | validated | invalidated

**Purpose**: Track what we believe to be true and systematically validate/invalidate assumptions.

### 3. Stakeholders
Array of stakeholder groups/individuals with:
- Unique ID
- Name and type (group | individual)
- Role in relation to the project
- Known needs and pain points
- Links to observation/interview notes

**Purpose**: Maintain understanding of who is affected and what they need.

### 4. Research Plan
Object containing questions to answer:
- Unique ID per question
- The question itself
- Purpose (why it matters)
- Method (how to answer)
- Status: pending | in-progress | answered
- Link to findings

**Purpose**: Structure the research process and track what we're learning.

### 5. Insights
Array of synthesized findings:
- Unique ID
- Title and description
- Confidence level
- Source links (to research notes/visualizations)
- Implications for design

**Purpose**: Distill research into actionable understanding.

### 6. Ideas
Array of solution concepts:
- Unique ID
- Title and description
- **Impact**: high | medium | low (expected value)
- **Feasibility**: high | medium | low (implementation difficulty)
- Status: ideated | prototyping | iterating | validated | invalidated | implemented
- Links to idea docs and prototypes

**Purpose**: Track solution exploration and evaluation.

### 7. Playbacks
Array of presentation sessions:
- Unique ID
- Date and audience
- Phase being presented
- Link to artifacts
- Decisions made

**Purpose**: Record key decision points and leadership engagement.

## Markdown Templates

### Research Templates (insights/)

#### observation_template.md
Structure for capturing field observations:
- Context and objective
- Observed behaviors, environment, pain points
- Direct quotes and artifacts
- Initial insights and follow-up questions

#### interview_template.md
Structure for user interviews:
- Participant background
- Questions and responses
- Key quotes and observations
- Insights and follow-up actions

#### research_synthesis_template.md
Structure for synthesizing research:
- Data sources
- Patterns and themes
- Key insights with evidence
- Contradictions and next steps

### Idea Templates (ideas/)

#### idea_template.md
Structure for solution concepts:
- Description and rationale
- User needs addressed
- Key benefits and differentiators
- Related insights
- Open questions and decision

#### prototype_template.md
Structure for prototype iterations:
- What, goals, and scope
- Key features demonstrated
- Iteration plan and success criteria
- Feedback from iteration sessions
- Synthesis and next steps

### Playback Templates (playbacks/)

#### playback_template.md
Structure for stakeholder presentations:
- Audience and objectives
- Presentation structure
- Artifacts shared
- Feedback and questions
- Decisions made and action items

## Usage Patterns

### Creating a New Project
1. Copy `templates/project/` to `projects/[project_name]/`
2. Update `currentstate.json` with project details
3. Set phase to "empathize"
4. Add initial assumptions and stakeholders

### Conducting Research (Empathize Phase)
1. Use observation/interview templates to capture data
2. Save files to `projects/[project_name]/insights/`
3. Update stakeholders in `currentstate.json` with notes_links
4. Add research questions to research_plan

### Synthesizing Insights (Define Phase)
1. Use research_synthesis_template to analyze findings
2. Update insights array in `currentstate.json`
3. Reference source files from insights/
4. Update phase to "define"

### Generating Ideas (Ideate Phase)
1. Use idea_template for each solution concept
2. Save to `projects/[project_name]/ideas/`
3. Add to ideas array in `currentstate.json`
4. Grade impact and feasibility
5. Update phase to "ideate"

### Prototyping (Prototype Phase)
1. Use prototype_template for each iteration
2. Link from parent idea document
3. Update idea status in `currentstate.json`
4. Update phase to "prototype"

### Presenting (All Phases)
1. Use playback_template for each presentation
2. Save to `projects/[project_name]/playbacks/`
3. Record decisions in both playback doc and `currentstate.json`
4. Update phase based on decisions

## Design Principles

1. **Single Source of Truth**: `currentstate.json` is the index; markdown files are the details
2. **Links Over Duplication**: Reference files rather than copying content
3. **Progressive Disclosure**: High-level state in JSON, rich context in markdown
4. **Agent-Readable**: Structured data enables AI agents to understand and guide the process
5. **Human-Friendly**: Templates provide clear structure for manual use
6. **Git-Native**: All state lives in version control for history and collaboration

## Schema Validation

The `schemas/currentstate.schema.json` file defines the structure and constraints for project state. Tools can use this to:
- Validate `currentstate.json` files
- Generate forms or UIs
- Provide autocomplete in editors
- Catch errors early

---

**Version**: 1.0  
**Last Updated**: 2025-12-29
