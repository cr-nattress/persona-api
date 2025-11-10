# Backlog Template Guide

## Overview

This guide provides templates for generating the remaining 48 backlog files (11 stories + 37 tasks). Use these templates to maintain consistency across all backlog documents.

## File Naming Conventions

### Stories
```
story-{number:02d}-{descriptive-name}/STORY.md
```
Examples:
- `story-01-input-sanitization/STORY.md`
- `story-02-api-client/STORY.md`

### Tasks
```
task-{number:02d}-{descriptive-action}.md
```
Examples:
- `task-01-create-sanitizer-service.md`
- `task-02-implement-sanitization-functions.md`

## STORY.md Template

```markdown
# Story {number}: {Story Title}

## Story Information

**Story ID**: EPIC-{epic#} / Story {story#}
**Story Title**: {Story Title}
**Story Points**: {1, 2, 3, 5, or 8}
**Priority**: {High, Medium, Low}
**Status**: Pending

## User Story

**As a** {role}
**I want** {capability}
**So that** {business value}

## Story Description

{2-3 sentence description of what this story delivers and why it matters}

## Acceptance Criteria

1. **{Criterion Category}**
   - {Specific testable criterion}
   - {Specific testable criterion}

2. **{Criterion Category}**
   - {Specific testable criterion}

{Continue for 4-8 total criteria}

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All {N} tasks completed
- [ ] {Specific completion requirement}
- [ ] {Specific completion requirement}
- [ ] Code committed to version control

## Tasks

This story contains the following tasks:

| # | Task | File | Duration |
|---|------|------|----------|
| 01 | {Task description} | task-01-{name}.md | {X} min |
| 02 | {Task description} | task-02-{name}.md | {X} min |

## Technical Notes

{Key technical details, code samples, configuration examples}

## Dependencies

**Blocks**:
- {Stories/epics that cannot start until this completes}

**Depends On**:
- {Stories/epics that must complete before this starts}

## Risks

- {Risk description} → {Mitigation strategy}

## Validation Steps

1. {Validation step}
2. {Validation step}

## Related Documentation

- `test-app/PLAN.md` - Lines {X-Y}
- {Other relevant files}

---

**Story Created**: 2025-11-09
**Story Status**: Ready for Execution
**Next Action**: Begin Task 01
```

## Task.md Template

```markdown
# Task {number}: {Task Title}

## Task Information

**Task ID**: EPIC-{epic#} / Story {story#} / Task {task#}
**Task Title**: {Task Title}
**Estimated Time**: {X} minutes
**Status**: Pending

## Objective

{Single sentence describing what this task accomplishes}

## Prerequisites

- {Previous task completed}
- {Required setup or configuration}
- Working directory: {path}

## Agent Prompt

```
{Copy-paste ready prompt for Claude Code}

{ACTION}: {What to do}

CONTEXT:
- {Background information}
- {Why this is needed}
- {Current state}

REQUIREMENTS:
1. {Specific requirement}
2. {Specific requirement}
3. {Specific requirement}

STEPS:
1. {Step with command or action}
2. {Step with command or action}
3. {Step with command or action}

VERIFICATION:
- {How to verify success}
- {What to check}
- {Expected output}

EXPECTED OUTPUT:
- {File created}
- {Configuration updated}
- {Feature working}
```
\```

## Step-by-Step Instructions

### Step 1: {Action}

{Detailed explanation}

```bash
# Command or code example
```

### Step 2: {Action}

{Detailed explanation}

```typescript
// Code example with comments
```

{Continue for all steps}

## Verification Checklist

- [ ] {Specific verification item}
- [ ] {Specific verification item}
- [ ] {Specific verification item}

## Expected Output

{Description of what should exist after completion}

```
{File structure, code sample, or configuration}
```

## Troubleshooting

### Issue: {Common problem}
**Solution**: {How to fix}

### Issue: {Common problem}
**Solution**: {How to fix}

## Related Files

- **Previous Task**: task-{X}-{name}.md
- **Next Task**: task-{X+1}-{name}.md
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- {Additional context}
- {Important considerations}
- {References to documentation}

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: {X} minutes
```

## Remaining Files to Generate

### EPIC-02: Service Layer (11 files)

#### Story 01: Input Sanitization
**Files**: STORY.md + 3 tasks

```
STORY.md
- User Story: As a developer, I want to implement input sanitization functions, so that user input is cleaned before API submission
- Points: 5
- Tasks: 3

task-01-create-sanitizer-service.md
- Create src/services/sanitizer.ts
- Define function signatures
- Duration: 10 min

task-02-implement-sanitization-functions.md
- Implement sanitizeRawText()
- Implement validateSanitizedInput()
- Implement getByteLength()
- Reference SANITIZATION.md lines 134-203
- Duration: 20 min

task-03-write-sanitizer-tests.md
- Create test file for sanitization
- Test edge cases (special chars, emoji, control chars)
- Test validation (empty, too long, UTF-8)
- Duration: 15 min
```

#### Story 02: API Client
**Files**: STORY.md + 3 tasks

```
STORY.md
- User Story: As a developer, I want to implement API client functions, so that components can communicate with the Person API
- Points: 5
- Tasks: 3

task-01-create-api-types.md
- Create src/services/types.ts
- Define Person, PersonData, Persona, ApiCall interfaces
- Reference PLAN.md lines 567-616
- Duration: 10 min

task-02-implement-api-client.md
- Create src/services/api.ts
- Implement createPerson()
- Implement listPersons()
- Implement addPersonDataAndRegenerate()
- Implement getPersona()
- Use fetch API with error handling
- Duration: 25 min

task-03-setup-api-logging.md
- Add API call logging registry
- Log all requests and responses
- Store in global state for debug panel
- Duration: 10 min
```

#### Story 03: Custom Hooks
**Files**: STORY.md + 1 task

```
STORY.md
- User Story: As a developer, I want to create custom React hooks, so that state management is reusable and clean
- Points: 5
- Tasks: 1

task-01-implement-usePersons-hook.md
- Create src/hooks/usePersons.ts
- Manage persons list state
- Implement refreshPersons()
- Implement addNewPerson()
- Handle loading and error states
- Duration: 20 min
```

### EPIC-03: UI Components (19 files)

{Similar structure for all 5 stories with their tasks}

### EPIC-04: Integration (9 files)

{Similar structure for 2 stories with their tasks}

### EPIC-05: Testing & Polish (9 files)

{Similar structure for 2 stories with their tasks}

## Quick Reference: All Stories

| Epic | Story | Title | Points | Tasks |
|------|-------|-------|--------|-------|
| 01 | 01 | Initialize Next.js | 8 | 4 ✅ |
| 01 | 02 | Project Structure | 8 | 1 ✅ |
| 02 | 01 | Input Sanitization | 5 | 3 |
| 02 | 02 | API Client | 5 | 3 |
| 02 | 03 | Custom Hooks | 5 | 1 |
| 03 | 01 | Form Component | 8 | 4 |
| 03 | 02 | Selector Component | 5 | 3 |
| 03 | 03 | Display Component | 5 | 3 |
| 03 | 04 | Debug Panel | 8 | 4 |
| 03 | 05 | Loading Component | 3 | 1 |
| 04 | 01 | Main Page | 8 | 4 |
| 04 | 02 | API Integration | 10 | 4 |
| 05 | 01 | Manual Testing | 8 | 4 |
| 05 | 02 | Refinement | 4 | 4 |

## Generation Checklist

### Completed ✅
- [x] README.md
- [x] BACKLOG-INDEX.md
- [x] All 5 EPIC.md files
- [x] EPIC-01 Story 01 + 4 tasks
- [x] EPIC-01 Story 02 + 1 task
- [x] GENERATION-SUMMARY.md
- [x] TEMPLATE-GUIDE.md

### Remaining ⏳
- [ ] EPIC-02 Story 01 + 3 tasks
- [ ] EPIC-02 Story 02 + 3 tasks
- [ ] EPIC-02 Story 03 + 1 task
- [ ] EPIC-03 Story 01 + 4 tasks
- [ ] EPIC-03 Story 02 + 3 tasks
- [ ] EPIC-03 Story 03 + 3 tasks
- [ ] EPIC-03 Story 04 + 4 tasks
- [ ] EPIC-03 Story 05 + 1 task
- [ ] EPIC-04 Story 01 + 4 tasks
- [ ] EPIC-04 Story 02 + 4 tasks
- [ ] EPIC-05 Story 01 + 4 tasks
- [ ] EPIC-05 Story 02 + 4 tasks

**Total Remaining**: 48 files

## Batch Generation Strategy

To efficiently generate remaining files:

1. **Batch by Epic**: Generate all stories and tasks for one epic at a time
2. **Use Templates**: Copy STORY.md and task-01 templates, modify details
3. **Maintain Consistency**: Follow exact format from completed files
4. **Reference Source Docs**: Use PLAN.md, SANITIZATION.md, README.md
5. **Validate Cross-References**: Ensure all file links are correct

## Key Content Sources

### For Service Layer (EPIC-02)
- `test-app/PLAN.md` lines 491-637
- `test-app/SANITIZATION.md` lines 134-314
- `test-app/README.md` lines 189-244

### For UI Components (EPIC-03)
- `test-app/PLAN.md` lines 122-489
- `test-app/README.md` lines 71-186

### For Integration (EPIC-04)
- `test-app/PLAN.md` lines 639-761
- `test-app/README.md` lines 266-295

### For Testing (EPIC-05)
- `test-app/PLAN.md` lines 799-845, 847-879
- `test-app/README.md` lines 296-310

---

**Document Created**: 2025-11-09
**Purpose**: Guide for generating remaining 48 backlog files
**Status**: Template ready for use
