# EPIC-09: Person Aggregate Root - Backlog Summary

## Status: ✅ COMPLETE - Ready for Implementation

The complete backlog for EPIC-09 has been generated with all stories, tasks, and detailed agent prompts ready for execution.

## Quick Stats

| Metric | Count |
|--------|-------|
| **Epic ID** | EPIC-09 |
| **Stories** | 15 |
| **Task Files Created** | 18+ |
| **Story Points** | 117 |
| **Estimated Duration** | 9-10 weeks (1 dev) / 4-5 weeks (2-3 devs) |
| **Priority** | 🔴 Critical |

## What's Included

✅ **EPIC.md** - Epic overview with business value, technical approach, risks, and success metrics

✅ **15 User Stories** with:
- User story statements (As a... I want... so that...)
- Acceptance criteria
- Story point estimates
- Technical notes
- Task lists
- Dependencies

✅ **18+ Detailed Tasks** with:
- Step-by-step instructions
- Copy-paste-ready agent prompts
- Verification steps
- Expected outcomes
- Estimated times

✅ **Supporting Documentation**:
- EPIC-09-INDEX.md (complete task breakdown)
- IMPLEMENTATION-PLAN.md (architectural reference)

## Directory Structure

```
backlog/epic-09-person-aggregate-root/
├── EPIC.md                                    Epic overview (15 phases)
├── story-01-database-schema/
│   ├── STORY.md
│   ├── task-01-create-migration-sql.md       (45 min)
│   └── task-02-test-migration-locally.md     (45 min)
├── story-02-python-data-models/STORY.md      (3-4 hrs)
├── story-03-person-repository/STORY.md       (2-3 hrs)
├── story-04-person-data-repository/STORY.md  (2-3 hrs)
├── story-05-persona-repository-update/STORY.md (2-3 hrs)
├── story-06-persona-recomputation/STORY.md   (3-4 hrs)
├── story-07-person-service-crud/STORY.md     (2-3 hrs)
├── story-08-data-accumulation/STORY.md       (2-3 hrs)
├── story-09-person-management-endpoints/STORY.md (2-3 hrs)
├── story-10-data-history-endpoints/STORY.md  (2-3 hrs)
├── story-11-persona-retrieval-endpoints/STORY.md (2-3 hrs)
├── story-12-backward-compatibility/STORY.md  (2-3 hrs)
├── story-13-data-migration-script/STORY.md   (2-3 hrs)
├── story-14-integration-tests/STORY.md       (3-4 hrs)
└── story-15-deployment-guide/STORY.md        (2-3 hrs)
```

## How to Use This Backlog

### 1. Start with Understanding
```
1. Read: IMPLEMENTATION-PLAN.md (overview of the design)
2. Read: backlog/epic-09-person-aggregate-root/EPIC.md (context)
3. Read: backlog/EPIC-09-INDEX.md (complete task list)
```

### 2. Execute Stories in Order
**Phase 1 (Weeks 1-1.5)**: Foundation
- Story US-09-01: Create Database Schema
- Story US-09-02: Create Python Data Models

**Phase 2 (Weeks 1.5-3)**: Data Access [Can parallelize 3 stories]
- Story US-09-03: Person Repository
- Story US-09-04: PersonData Repository
- Story US-09-05: Persona Repository Update

**Phase 3 (Weeks 3-5)**: Service Logic [Can parallelize]
- Story US-09-06: Persona Recomputation
- Story US-09-07: Person Service CRUD
- Story US-09-08: Data Accumulation

**Phase 4 (Weeks 5-7.5)**: API Endpoints [Can parallelize 4 stories]
- Story US-09-09: Person Management Endpoints
- Story US-09-10: Data History Endpoints
- Story US-09-11: Persona Retrieval Endpoints
- Story US-09-12: Backward-Compatible Adapters

**Phase 5 (Weeks 7.5-9.5)**: Testing & Deployment
- Story US-09-13: Data Migration Script
- Story US-09-14: Integration Tests
- Story US-09-15: Deployment Guide

### 3. Execute Individual Tasks
```
1. Open story STORY.md file
2. Review acceptance criteria
3. Review task list
4. Open first task-XX.md file
5. Copy the "Agent Prompt" section
6. Paste into Claude Code or your AI coding assistant
7. Verify against "Verification Steps"
8. Mark story task complete
9. Move to next task in story
10. Mark story complete when all acceptance criteria met
```

### 4. Track Progress
- Mark tasks complete as you finish them
- Update story status (Pending → In Progress → Complete)
- Document any blockers or issues
- Note actual time spent vs. estimates

## Key Features of This Backlog

### ✅ AI-Agent Ready
Every task includes a detailed "Agent Prompt" section with:
- Specific file paths to create/modify
- Step-by-step instructions
- Code patterns and examples
- Copy-paste-ready commands
- Clear verification criteria

### ✅ Fully Traceable
- Each task links to its story
- Each story links to its epic
- Each epic links to implementation plan
- Full chain of responsibility

### ✅ Properly Sequenced
- Critical path identified
- Dependencies clearly marked
- Parallelization opportunities noted
- Phased rollout approach

### ✅ Comprehensive Coverage
- Database schema
- Data models
- Repository pattern
- Service layer
- API endpoints
- Backward compatibility
- Data migration
- Testing
- Deployment

## Estimated Effort Breakdown

| Phase | Stories | Hours | Weeks |
|-------|---------|-------|-------|
| **Phase 1** | 2 | 10-12 | 1.5 |
| **Phase 2** | 3 | 12-15 | 1.5 |
| **Phase 3** | 3 | 12-15 | 2 |
| **Phase 4** | 4 | 14-18 | 2.5 |
| **Phase 5** | 3 | 13-17 | 2 |
| **TOTAL** | **15** | **61-77** | **9-10** |

*(Assumes 1 developer working 6-8 hours/day with meetings and other work)*

## Team Recommendations

### Solo Developer (9-10 weeks)
- Work through phases sequentially
- Use detailed task prompts to maximize efficiency
- Plan for code review cycle time

### 2 Developers (4-5 weeks)
- **Dev 1**: Phase 1 + Phase 2A (Repos) + Phase 4A (Endpoints)
- **Dev 2**: Phase 2B (Models) + Phase 3 + Phase 4B + Phase 5

### 3+ Developers (3-3.5 weeks)
- **Dev 1**: Foundation (Phases 1-2)
- **Dev 2**: Service Logic (Phase 3)
- **Dev 3**: API + Testing (Phases 4-5)

## Success Criteria

Upon completion, you should have:

- ✅ Three new database tables properly designed and migrated
- ✅ Complete Python models with validation
- ✅ Full repository layer for data access
- ✅ Service layer with persona recomputation logic
- ✅ Seven new API endpoints with full functionality
- ✅ Backward-compatible endpoints for existing clients
- ✅ Data migration script tested and documented
- ✅ Comprehensive integration tests (80%+ coverage)
- ✅ Deployment guide with rollback procedures
- ✅ Zero data loss during migration

## Critical Path

```
START
  ↓
US-09-01 (Database)
  ↓
US-09-02 (Models)
  ↓
┌─→ US-09-03 (PersonRepo)
├─→ US-09-04 (PersonDataRepo)
└─→ US-09-05 (PersonaRepo)
  ↓
US-09-06 (Recomputation)
  ↓
┌─→ US-09-07 (Service CRUD)
└─→ US-09-08 (Data Accum)
  ↓
┌─→ US-09-09 (Person Endpoints)
├─→ US-09-10 (Data Endpoints)
├─→ US-09-11 (Persona Endpoints)
└─→ US-09-12 (Backward Compat)
  ↓
US-09-13 (Migration Script)
  ↓
US-09-14 (Integration Tests)
  ↓
US-09-15 (Deployment)
  ↓
DONE ✅
```

## File Navigation

### Read First
- `IMPLEMENTATION-PLAN.md` - Architecture and design decisions
- `backlog/epic-09-person-aggregate-root/EPIC.md` - Epic overview

### For Detailed Tasks
- `backlog/EPIC-09-INDEX.md` - Complete task breakdown with descriptions

### For Execution
- Each `story-XX-*/STORY.md` - Story overview and acceptance criteria
- Each `story-XX-*/task-YY-*.md` - Individual task with agent prompt

### For Reference
- `backlog/epic-09-person-aggregate-root/EPIC.md` - Epic context
- Original backlog files: `backlog/epic-01-*` through `backlog/epic-08-*`

## Common Questions

**Q: Can I skip any stories?**
A: No, they have dependencies. Follow the phases in order.

**Q: Can I parallelize work?**
A: Yes! See Phase 2, Phase 3, and Phase 4 - multiple stories can be done simultaneously.

**Q: How do I handle blockers?**
A: Document them, check dependencies, reach out for help. Don't skip stories.

**Q: What if estimates are off?**
A: Adjust as you go. Longer estimates → simplify future stories.

**Q: How do I test locally?**
A: Each story has verification steps. Use task prompts for detailed testing.

## Next Steps

1. **NOW**: Review IMPLEMENTATION-PLAN.md
2. **TODAY**: Read backlog/epic-09-person-aggregate-root/EPIC.md
3. **TOMORROW**: Start with US-09-01 (Create Database Schema)
4. **FOLLOW**: Use EPIC-09-INDEX.md to track progress

## Support & Questions

- **Architecture questions**: See IMPLEMENTATION-PLAN.md sections 1-4
- **Database design**: See EPIC-09/story-01-*/
- **API design**: See EPIC-09/story-09-12/
- **Existing patterns**: Review PersonaRepository and PersonaService in codebase

---

## Summary

EPIC-09 is a complete, executable backlog for redesigning the persona-api database architecture to support incremental data accumulation and persona improvement. With detailed task prompts, clear dependencies, and phased execution, it's ready for any team size.

**Total Scope**: 15 Stories | 117 Story Points | 9-10 Weeks (1 dev) | 4-5 Weeks (2-3 devs)

**Status**: ✅ **Ready to Start**

**Last Updated**: 2025-11-09

---

Generated by: generate-backlog skill for Claude Code
