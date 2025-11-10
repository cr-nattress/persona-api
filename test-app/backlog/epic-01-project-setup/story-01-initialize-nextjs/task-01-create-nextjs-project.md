# Task 01: Create Next.js Project

## Task Information

**Task ID**: EPIC-01 / Story 01 / Task 01
**Task Title**: Create Next.js Project
**Estimated Time**: 10 minutes
**Status**: Pending

## Objective

Initialize a new Next.js 14+ project with App Router using the official create-next-app CLI tool.

## Prerequisites

- Node.js 18+ installed
- npm or pnpm available
- Terminal access
- Working directory: `C:\Users\RED\OneDrive\Documents\github\persona-api\`

## Agent Prompt

```
Create a new Next.js 14+ project for the Person Aggregate Root API test application.

CONTEXT:
- Project name: test-app
- Framework: Next.js 14+ with App Router
- Language: TypeScript (will configure in next task)
- Location: C:\Users\RED\OneDrive\Documents\github\persona-api\test-app

REQUIREMENTS:
1. Use create-next-app with latest Next.js 14+
2. Enable App Router (NOT Pages Router)
3. Use TypeScript
4. Include ESLint
5. Use src/ directory structure
6. Do NOT use Tailwind yet (will configure separately)

STEPS:
1. Navigate to: C:\Users\RED\OneDrive\Documents\github\persona-api\
2. Run: npx create-next-app@latest test-app
3. When prompted, answer:
   - TypeScript? Yes
   - ESLint? Yes
   - Tailwind CSS? No (will add manually)
   - src/ directory? Yes
   - App Router? Yes
   - Customize default import alias? No

4. Navigate into project: cd test-app
5. Verify installation: npm run dev
6. Open browser: http://localhost:3000
7. Verify Next.js welcome page loads
8. Stop dev server: Ctrl+C

VERIFICATION:
- Project created at correct path
- package.json exists with Next.js 14+
- src/app/ directory exists (App Router)
- tsconfig.json exists
- Development server runs successfully
- No errors in console

EXPECTED OUTPUT:
- New test-app/ directory
- Next.js 14+ installed
- Development server runs on port 3000
- Welcome page displays correctly
```

## Step-by-Step Instructions

### Step 1: Navigate to Parent Directory
```bash
cd C:\Users\RED\OneDrive\Documents\github\persona-api\
```

### Step 2: Create Next.js App
```bash
npx create-next-app@latest test-app
```

### Step 3: Answer Prompts
```
✔ Would you like to use TypeScript? … Yes
✔ Would you like to use ESLint? … Yes
✔ Would you like to use Tailwind CSS? … No
✔ Would you like to use `src/` directory? … Yes
✔ Would you like to use App Router? (recommended) … Yes
✔ Would you like to customize the default import alias (@/*)? … No
```

### Step 4: Navigate into Project
```bash
cd test-app
```

### Step 5: Verify Installation
```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Ready in XXXms
```

### Step 6: Check in Browser
Open http://localhost:3000 and verify the Next.js welcome page appears.

### Step 7: Stop Server
Press `Ctrl+C` in terminal.

## Verification Checklist

- [ ] Project directory created at `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\`
- [ ] `package.json` exists with Next.js 14+ listed
- [ ] `tsconfig.json` exists
- [ ] `next.config.js` exists
- [ ] `src/app/` directory exists
- [ ] `src/app/layout.tsx` exists
- [ ] `src/app/page.tsx` exists
- [ ] `public/` directory exists
- [ ] `.eslintrc.json` exists
- [ ] `node_modules/` directory exists
- [ ] Development server starts successfully
- [ ] Welcome page loads at http://localhost:3000
- [ ] No errors in terminal or browser console

## Expected File Structure

After completion:
```
test-app/
├── package.json
├── package-lock.json
├── tsconfig.json
├── next.config.js
├── .eslintrc.json
├── .gitignore
├── README.md
├── node_modules/
├── public/
│   ├── next.svg
│   └── vercel.svg
└── src/
    └── app/
        ├── favicon.ico
        ├── globals.css
        ├── layout.tsx
        └── page.tsx
```

## Troubleshooting

### Issue: npx not found
**Solution**: Install Node.js 18+ from https://nodejs.org/

### Issue: Port 3000 already in use
**Solution**:
- Stop any process using port 3000
- Or run with different port: `npm run dev -- -p 3001`

### Issue: Permission errors on Windows
**Solution**: Run terminal as Administrator

### Issue: npm install fails
**Solution**:
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and package-lock.json
- Run `npm install` again

## Related Files

- **Next Task**: task-02-setup-typescript.md
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- This creates a basic Next.js project with default configuration
- TypeScript will be configured properly in the next task
- Tailwind CSS will be added in a separate task
- Default files can be kept for now; we'll modify them later

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: 10 minutes
