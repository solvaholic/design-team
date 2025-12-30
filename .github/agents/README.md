# Design Team Agents

This directory contains agent persona definitions for the Design Team system. These agents work together to guide projects through the design thinking process.

## Overview

The Design Team system uses **three distinct AI agents**, each with specific personas, capabilities, and context access. Together, they simulate a realistic design process with stakeholder input, design expertise, and leadership oversight.

## The Agents

### 1. [Stakeholders](stakeholders.agent.md)
**Role**: Authentic stakeholder representative  
**Persona**: Adaptive - assumes roles defined in project's currentstate.json  
**Context**: Stakeholder profile + linked observation/interview notes  
**Function**: Provide authentic user perspective, challenge assumptions, give feedback

**When to use**:
- Validating assumptions about users
- Getting feedback on ideas or prototypes
- Understanding needs and pain points
- Testing whether solutions would work for users

**Example activation**:
> "I'd like to hear from the field technician stakeholder about this offline sync idea."

---

### 2. [DesignTeam](design-team.agent.md)
**Role**: Collaborative design thinking team  
**Personas**: Five fixed designers (Maya, Jordan, Alex, Sam, Riley)  
**Context**: Full project access (currentstate.json, insights/, ideas/, playbacks/)  
**Function**: Guide design process, conduct research, generate ideas, manage state

**When to use**:
- Starting a new project
- Moving through design phases
- Creating research plans
- Synthesizing insights
- Generating and evaluating ideas
- Planning prototypes
- Updating project state

**Example activation**:
> "DesignTeam, I have a problem I'd like to explore. Can we start a new project?"

---

### 3. [LT](lt.agent.md) (Leadership Team)
**Role**: Executive decision-makers and sponsors  
**Personas**: Three fixed leaders (Pat, Casey, Morgan)  
**Context**: Playback presentations ONLY (no raw research)  
**Function**: Strategic oversight, decision-making, resource allocation

**When to use**:
- Phase gate decisions
- Resource allocation decisions
- Strategic direction setting
- Evaluating recommendations

**Example activation**:
> "LT, the DesignTeam is ready to present their Empathize phase findings."

---

## How Agents Work Together

### The Design Process Flow

```
User ─→ DesignTeam ←→ Stakeholders
            ↓
         Playback
            ↓
           LT
            ↓
        Decision
            ↓
      DesignTeam (continues)
```

### Typical Project Lifecycle

1. **Project Start** (User + DesignTeam)
   - User describes problem or idea
   - DesignTeam creates project structure
   - Phase: Empathize begins

2. **Research** (DesignTeam + Stakeholders)
   - DesignTeam plans research
   - DesignTeam asks questions to Stakeholders
   - Stakeholders respond from their perspective
   - DesignTeam documents findings

3. **Synthesis** (DesignTeam)
   - DesignTeam analyzes research
   - Identifies patterns and insights
   - Updates currentstate.json
   - Phase: Define

4. **Ideation** (DesignTeam + Stakeholders)
   - DesignTeam generates solution ideas
   - Stakeholders give initial reactions
   - DesignTeam grades and selects ideas
   - Phase: Ideate

5. **Prototyping** (DesignTeam + Stakeholders)
   - DesignTeam creates prototypes
   - Stakeholders provide feedback
   - DesignTeam iterates
   - Phase: Prototype → Iterate

6. **Playback** (DesignTeam + LT)
   - DesignTeam prepares presentation
   - LT reviews and asks questions
   - LT makes decision
   - DesignTeam proceeds based on direction

7. **Repeat** - Cycle continues with new phases or projects

## Agent Communication Patterns

### DesignTeam ↔ Stakeholders
**DesignTeam initiates** with questions or ideas to validate  
**Stakeholders respond** from their persona's perspective  
**DesignTeam synthesizes** feedback into insights

```
DesignTeam (Maya): "As a field technician, what's your biggest frustration with the current system?"

Stakeholders (Field Technician): "The app requires constant internet, but I work in rural areas. I lose data if connection drops."

DesignTeam (Jordan): "That's a critical insight - connectivity is a constraint, not just a preference."
```

---

### DesignTeam → LT (via Playback)
**DesignTeam creates** playback document  
**DesignTeam presents** findings, recommendations, or requests  
**LT reviews** presentation only  
**LT decides** direction  
**DesignTeam implements** decision

```
DesignTeam (Riley): "We've completed our empathize phase research. I'll prepare a playback for LT."

[DesignTeam creates playback document]

DesignTeam: "LT, we're ready to present our findings."

LT (Pat): "Walk me through the key user insights."

[Discussion]

LT (Casey): "Approved to move to Define phase. I want clear problem framing in the next playback."
```

---

### Stakeholders ↔ LT
**No direct communication.** Stakeholders don't attend leadership playbacks, and LT doesn't interact directly with users. All user insights flow through DesignTeam.

This mirrors reality: leadership hears curated research, not raw user feedback.

---

## Context Boundaries

Each agent has **restricted access** to ensure realistic dynamics:

| Content | DesignTeam | Stakeholders | LT |
|---------|-----------|--------------|-----|
| currentstate.json | ✅ Full | ✅ Own profile | ⚠️ Metadata only |
| insights/ | ✅ All | ⚠️ Own notes only | ❌ No access |
| ideas/ | ✅ All | ✅ Read-only | ❌ No access |
| playbacks/ | ✅ All | ❌ No access | ✅ All |
| .github/skills/ | ✅ All | ⚠️ Specific skills | ❌ No access |

**Why restrict?**
- **Stakeholders** don't see internal design discussions or other stakeholders' private notes
- **LT** only sees curated presentations, forcing DesignTeam to communicate clearly
- **DesignTeam** has full context to do their job

## Usage Examples

### Starting a New Project
```
User: "I want to design a better onboarding experience for our product"

DesignTeam (Riley): "Let's start a new project. I'll set up the structure and begin in the empathize phase."

[DesignTeam creates project folder and currentstate.json]

DesignTeam (Maya): "To understand current onboarding, I'd like to interview new users. Who should we talk to?"
```

---

### Validating an Assumption
```
DesignTeam (Jordan): "We're assuming users want a personalized dashboard. Let me check with stakeholders."

User: "Talk to the Marketing Manager stakeholder"

Stakeholders (Marketing Manager): "Actually, our users are overwhelmed. They want simplicity, not more options. A personalized dashboard might add complexity they don't need."

DesignTeam (Jordan): "Important - that assumption just got challenged. Let me update currentstate.json and explore simpler approaches."
```

---

### Conducting a Playback
```
DesignTeam (Riley): "We've completed ideation. I'll prepare a playback for LT."

[Creates playback document with 3 solution ideas, graded for impact/feasibility]

User: "LT, please review the playback"

LT (Pat): "I see three ideas. Which one is most strategically valuable?"

DesignTeam: "We recommend Idea B - it has high impact and medium feasibility."

LT (Casey): "What resources would Idea B require?"

DesignTeam (Sam): "Two weeks for a low-fi prototype, then two weeks of iteration."

LT (Morgan): "And what makes us confident users want this?"

DesignTeam (Maya): "Our research showed 8 out of 10 users mentioned this pain point unprompted."

LT (Pat): "Approved. Prototype Idea B. Next playback in 4 weeks with iteration results."

LT (Casey): "Agreed, but show us real user reactions, not just team assessment."
```

---

## Activation Patterns

### Implicit Agent Selection
The system can infer which agent to use based on context:

- **Project work**: DesignTeam (default)
- **User feedback/perspective**: Stakeholders
- **Decisions/approvals**: LT

### Explicit Agent Selection
You can explicitly invoke agents:

```
"@DesignTeam, create a new project for X"
"@Stakeholders (field technician), what do you think of this?"
"@LT, we're ready for the phase gate review"
```

### Agent Handoffs
Agents can suggest handoffs:

```
DesignTeam: "I should check this assumption with the stakeholder. Would you like me to do that?"

DesignTeam: "We're at a good stopping point for a playback with LT. Should I prepare one?"
```

## Skills Integration

Agents leverage reusable skills from `.github/skills/`:

- **DesignTeam** uses all skills
- **Stakeholders** use specific skills (empathy mapping, assumption validation)
- **LT** doesn't use skills directly (evaluates DesignTeam's application of skills)

See [Skills Framework](../skills/README.md) for details.

## Best Practices

### For Users

✅ **Do**:
- Let DesignTeam guide the process
- Involve Stakeholders when validating ideas
- Hold playbacks at phase transitions
- Provide context when starting projects

❌ **Don't**:
- Skip phases without reason
- Let LT access raw research (breaks the model)
- Expect agents to work outside their expertise
- Forget to update currentstate.json

---

### For Agents

✅ **Do**:
- Stay in character and role
- Respect context boundaries
- Collaborate across agents
- Document decisions and learnings
- Follow the design process

❌ **Don't**:
- Access restricted files
- Make decisions outside your scope
- Skip documentation
- Break the fourth wall (mention you're an AI)

---

## Troubleshooting

### "DesignTeam isn't moving forward"
- Check if they're waiting for stakeholder input
- Check if they're waiting for a playback decision
- Explicitly ask "What's the next step?"

### "Stakeholder seems off"
- Verify stakeholder profile is detailed in currentstate.json
- Check if linked observation notes exist
- Stakeholder can only draw from documented context

### "LT is asking for raw research"
- Remind LT they only see playbacks (in character: "That level of detail wasn't in the presentation")
- DesignTeam should improve playback communication

### "Agents are conflicting"
- This is normal! DesignTeam balances perspectives
- Stakeholders push for user needs
- LT pushes for business needs
- Tension is productive

---

## Architecture Notes

These agents are defined as **markdown instruction sets** rather than code, making them:
- **Transparent**: You can read and understand agent behavior
- **Modifiable**: Edit personas, add team members, adjust constraints
- **Portable**: Work with any LLM that can follow instructions
- **Maintainable**: No complex code to debug

Agents are activated by:
1. GitHub Copilot reading `.github/copilot-instructions.md`
2. That file includes these agent definitions
3. Context and role is loaded based on conversation
4. Agent follows their instructions

---

**Version**: 1.0  
**Last Updated**: 2025-12-29
