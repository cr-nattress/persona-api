# Story 01: Initialize Next.js

## Story Information

**Story ID**: EPIC-01 / Story 01
**Story Title**: Initialize Next.js
**Story Points**: 8
**Priority**: High
**Status**: Pending

## User Story

**As a** developer
**I want** to initialize a Next.js 14+ project with TypeScript
**So that** I have a working development environment

## Story Description

Create a new Next.js 14+ project using the App Router architecture, configure TypeScript with strict mode, install and configure Tailwind CSS for styling, and set up environment variables for API configuration.

This story establishes the foundational development environment required for all subsequent work.

## Acceptance Criteria

1. **Next.js Project Created**
   - Next.js 14+ installed with App Router (not Pages Router)
   - Project structure follows Next.js 14 conventions
   - Development server starts successfully with `npm run dev`
   - Application renders default home page at http://localhost:3000

2. **TypeScript Configured**
   - TypeScript 5+ installed
   - `tsconfig.json` exists with strict mode enabled
   - All `.js` files converted to `.tsx` or `.ts`
   - TypeScript compilation succeeds without errors
   - IDE provides IntelliSense and type checking

3. **Tailwind CSS Configured**
   - Tailwind CSS 3+ installed
   - `tailwind.config.js` and `postcss.config.js` exist
   - Tailwind directives added to global CSS
   - Tailwind utility classes work in components
   - No CSS compilation errors

4. **Environment Variables Set Up**
   - `.env.local.example` committed to repo
   - `.env.local` created (git-ignored)
   - `NEXT_PUBLIC_API_BASE_URL` defined
   - Environment variables accessible in code
   - README documents environment setup

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All 4 tasks completed
- [ ] Development server runs without errors
- [ ] TypeScript compiles without warnings
- [ ] Tailwind classes apply correctly
- [ ] Environment variables load successfully
- [ ] `package.json` contains all dependencies
- [ ] `package-lock.json` committed
- [ ] `.gitignore` includes `.env.local`
- [ ] Code committed to version control

## Tasks

This story contains the following tasks:

| # | Task | File | Duration |
|---|------|------|----------|
| 01 | Create Next.js project | task-01-create-nextjs-project.md | 10 min |
| 02 | Setup TypeScript | task-02-setup-typescript.md | 10 min |
| 03 | Configure Tailwind | task-03-configure-tailwind.md | 15 min |
| 04 | Setup environment variables | task-04-setup-env-variables.md | 5 min |

## Technical Notes

### Required Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
```

### Development Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

## Dependencies

**Blocks**:
- Story 02: Project Structure (needs project to exist)
- All stories in EPIC-02, EPIC-03, EPIC-04, EPIC-05

**Depends On**:
- None (first story)

## Risks

- Node version incompatibility → Specify Node 18+ requirement
- npm install failures → Use lock file, document versions
- Tailwind config errors → Follow official Next.js + Tailwind guide

## Validation Steps

After completing all tasks:

1. Run `npm run dev`
2. Open http://localhost:3000
3. Verify page loads without errors
4. Check console for TypeScript errors
5. Add a Tailwind class to test styling
6. Verify environment variable loads correctly

## Related Documentation

- `test-app/PLAN.md` - Lines 73-117
- Next.js 14 Documentation: https://nextjs.org/docs
- Tailwind CSS with Next.js: https://tailwindcss.com/docs/guides/nextjs

---

**Story Created**: 2025-11-09
**Story Status**: Ready for Execution
**Next Action**: Begin Task 01 (Create Next.js project)
