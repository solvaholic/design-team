# Working with Projects in Git

## Default Behavior

The `projects/` folder is **ignored by default** in git. This is intentional because:
- Projects contain work-in-progress and exploratory content
- Each user/team may have different projects they're working on
- Not all project work needs to be in version control

## Selectively Committing Projects

When you want to commit a specific project to version control:

### Option 1: Add exclusion to projects/.gitignore (Recommended)

Edit `projects/.gitignore` and add an exclusion for your project:

```bash
# In projects/.gitignore, uncomment or add:
!my-project-name/
```

Then stage and commit normally (no `-f` flag needed):

```bash
git add projects/my-project-name/
git commit -m "Add my-project-name"
```

This approach is cleaner because once excluded in the gitignore, the project behaves like any normal tracked folder.

### Option 2: Force add with -f flag

If you don't want to modify `.gitignore`, you can force-add files:

```bash
git add -f projects/my-project-name/
git commit -m "Add my-project-name"
```

Or add specific files only:

```bash
git add -f projects/my-project-name/currentstate.json
git add -f projects/my-project-name/insights/key-insight.md
git commit -m "Add key artifacts from my-project-name"
```

### Option 3: Ask an Agent for Help

You can ask @DesignTeam or another agent:
- "Help me prepare my project for sharing"
- "Which files from my project should I commit?"
- "Add my project to git and commit the important artifacts"

The agent can:
- Add the exclusion to `projects/.gitignore`
- Identify which artifacts are ready to share
- Stage the appropriate files
- Create meaningful commit messages
- Help decide what should remain local vs shared

## Best Practices

**Commit when:**
- Project reaches a milestone or phase gate
- Insights need to be shared with the team
- Work needs to be preserved or handed off
- Leadership decisions are documented

**Keep local when:**
- Still in early exploration
- Contains sensitive information
- Personal working notes and drafts
- Experimental ideas not yet validated

## Example Workflow

```bash
# Work on your project locally (all changes ignored by default)
# ... make changes ...

# Option A: Add exclusion to projects/.gitignore
echo "!my-project/" >> projects/.gitignore
git add projects/.gitignore
git add projects/my-project/
git commit -m "Add my-project"

# Option B: Ask agent to handle it
@DesignTeam "Add my-project to git and commit phase 1 artifacts"

# Option C: Force add without modifying .gitignore
git status  # Shows only tracked files, projects/* hidden
git add -f projects/my-project/currentstate.json
git add -f projects/my-project/playbacks/phase1-decision.md
git commit -m "Phase 1 complete: Problem definition approved"
```

## Technical Details

- `projects/.gitignore` contains `*` to ignore all project folders by default
- Add `!project-name/` to exclude specific projects from being ignored
- Excluded projects are tracked normally (standard `git add` works)
- The `-f` flag can bypass gitignore without modifying the file
- Once added (either way), files are tracked normally
- To stop tracking: `git rm --cached -r projects/my-project-name/` then remove the exclusion
