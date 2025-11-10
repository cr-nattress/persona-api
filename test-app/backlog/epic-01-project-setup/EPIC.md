# EPIC-01: Project Setup

## Epic Overview

**Epic ID**: EPIC-01
**Epic Name**: Project Setup
**Epic Owner**: Development Team
**Status**: Pending
**Story Points**: 16
**Priority**: High (Blocker for all other work)

## Business Value Statement

Establish the foundational Next.js project with TypeScript, Tailwind CSS, and proper directory structure to enable rapid development of the Person Aggregate Root API test application.

**Business Impact**: Without this foundation, no development can occur. This epic unblocks all subsequent work.

## Current State vs Target State

### Current State
- No Next.js project exists
- No development environment configured
- No project structure defined

### Target State
- Next.js 14+ project with App Router initialized
- TypeScript configured with strict mode
- Tailwind CSS installed and configured
- Environment variables set up for API URL
- Complete directory structure matching PLAN.md specification
- Development server running successfully
- All dependencies installed

## Technical Approach

### Technology Stack
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **Package Manager**: npm or pnpm
- **Node Version**: 18+

### Key Technical Decisions
1. Use App Router (not Pages Router) for modern Next.js features
2. Enable TypeScript strict mode for type safety
3. Configure Tailwind with custom theme if needed
4. Use environment variables for API configuration
5. Follow recommended Next.js directory structure

## User Stories

This epic contains the following user stories:

### Story 01: Initialize Next.js (8 points)
**As a** developer
**I want** to initialize a Next.js 14+ project with TypeScript
**So that** I have a working development environment

**Tasks**:
1. Create Next.js project
2. Setup TypeScript configuration
3. Configure Tailwind CSS
4. Setup environment variables

### Story 02: Project Structure (8 points)
**As a** developer
**I want** to create the recommended directory structure
**So that** the codebase is organized and maintainable

**Tasks**:
1. Create directory structure (src/, components/, services/, hooks/)

## Acceptance Criteria

The epic is considered complete when:

1. Next.js development server runs without errors (`npm run dev`)
2. TypeScript compilation succeeds with strict mode enabled
3. Tailwind CSS classes work in components
4. Environment variables load correctly
5. All required directories exist:
   - `src/app/`
   - `src/components/`
   - `src/services/`
   - `src/hooks/`
6. `package.json` contains all required dependencies
7. `.env.local` is git-ignored and `.env.local.example` exists
8. README includes setup instructions

## Definition of Done

- [ ] All user stories completed and accepted
- [ ] All acceptance criteria met
- [ ] Development server runs successfully
- [ ] TypeScript compiles without errors
- [ ] No security vulnerabilities in dependencies
- [ ] Directory structure matches specification
- [ ] Environment configuration documented
- [ ] Code committed to version control
- [ ] README updated with setup steps

## Dependencies

### Blocks
- **EPIC-02**: Service Layer (cannot start until project setup complete)
- **EPIC-03**: UI Components (requires project structure)
- **EPIC-04**: Integration (requires all infrastructure)
- **EPIC-05**: Testing & Polish (requires working application)

### Depends On
- None (this is the first epic)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Node version incompatibility | High | Low | Specify Node 18+ requirement, test before starting |
| npm install failures | High | Medium | Use lock file, document node/npm versions |
| Tailwind config errors | Medium | Low | Use official Next.js + Tailwind guide |
| Environment variable issues | Medium | Medium | Provide clear .env.local.example template |
| TypeScript config too strict | Low | Low | Use recommended tsconfig.json from Next.js |

## Technical Notes

### Required Dependencies
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

### Directory Structure
```
test-app/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.local (git-ignored)
├── .env.local.example
├── public/
│   └── favicon.ico
└── src/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    ├── components/
    ├── services/
    └── hooks/
```

### Environment Variables
```bash
# .env.local.example
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

## Estimated Timeline

- **Story 01**: 40 minutes (4 tasks)
- **Story 02**: 10 minutes (1 task)
- **Total**: ~50 minutes

## Success Metrics

- Development server starts in <5 seconds
- Hot reload works correctly
- No console errors on startup
- TypeScript IntelliSense works in IDE
- Tailwind classes apply correctly

## Related Documentation

- `test-app/PLAN.md` - Lines 73-117 (Technology Stack & Directory Structure)
- `test-app/README.md` - Lines 36-70 (Project Structure)
- Next.js Documentation: https://nextjs.org/docs
- Tailwind CSS Documentation: https://tailwindcss.com/docs

## Epic Progress

- [ ] Story 01: Initialize Next.js (0/4 tasks)
- [ ] Story 02: Project Structure (0/1 tasks)

**Overall Progress**: 0% (0/5 tasks completed)

---

**Epic Created**: 2025-11-09
**Epic Status**: Ready for Execution
**Next Action**: Begin Story 01, Task 01 (Create Next.js project)
