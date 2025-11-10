# Task 01: Create Directory Structure

## Task Information

**Task ID**: EPIC-01 / Story 02 / Task 01
**Task Title**: Create Directory Structure
**Estimated Time**: 10 minutes
**Status**: Pending

## Objective

Create the complete directory structure for components, services, and hooks as specified in PLAN.md.

## Prerequisites

- Story 01 completed (Next.js initialized)
- Working directory: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\`

## Agent Prompt

```
Create the directory structure for the Next.js test application following the PLAN.md specification.

CONTEXT:
- Next.js 14+ project with App Router already initialized
- Need to create directories for components, services, and hooks
- Structure should match the specification in test-app/PLAN.md

REQUIREMENTS:
1. Create src/components/ directory
2. Create src/services/ directory
3. Create src/hooks/ directory
4. Create .gitkeep files in empty directories (optional)
5. Verify directory structure matches specification

STEPS:
1. Navigate to: C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\

2. Create directories:
   mkdir src\components
   mkdir src\services
   mkdir src\hooks

3. Verify structure:
   - src/app/ (should already exist)
   - src/components/ (newly created)
   - src/services/ (newly created)
   - src/hooks/ (newly created)

4. (Optional) Create .gitkeep in empty directories to track them:
   type nul > src\components\.gitkeep
   type nul > src\services\.gitkeep
   type nul > src\hooks\.gitkeep

VERIFICATION:
- All three directories exist
- Directories are empty and ready for code
- TypeScript path aliases work (@/components, @/services, @/hooks)
- Directories committed to git (if using .gitkeep)

EXPECTED OUTPUT:
- Complete directory structure matching PLAN.md
- Ready for component and service implementation
```

## Step-by-Step Instructions

### Step 1: Navigate to Project Root

```bash
cd C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\
```

### Step 2: Create Directories

**Windows Command Prompt:**
```bash
mkdir src\components
mkdir src\services
mkdir src\hooks
```

**PowerShell or Git Bash:**
```bash
mkdir -p src/components
mkdir -p src/services
mkdir -p src/hooks
```

### Step 3: (Optional) Create .gitkeep Files

To ensure git tracks empty directories:

**Windows Command Prompt:**
```bash
type nul > src\components\.gitkeep
type nul > src\services\.gitkeep
type nul > src\hooks\.gitkeep
```

**PowerShell or Git Bash:**
```bash
touch src/components/.gitkeep
touch src/services/.gitkeep
touch src/hooks/.gitkeep
```

### Step 4: Verify Structure

List directories to confirm:
```bash
dir src /ad  # Windows
ls -la src   # Git Bash
```

Expected output:
```
src/
├── app/
├── components/
├── services/
└── hooks/
```

## Verification Checklist

- [ ] `src/components/` directory exists
- [ ] `src/services/` directory exists
- [ ] `src/hooks/` directory exists
- [ ] All directories are empty (except optional .gitkeep)
- [ ] Directories visible in file explorer
- [ ] TypeScript path alias `@/*` works for all directories
- [ ] Git tracks directories (if using .gitkeep)

## Expected Directory Structure

After completion:

```
test-app/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── .env.local
├── .env.local.example
├── .gitignore
├── node_modules/
├── public/
└── src/
    ├── app/
    │   ├── favicon.ico
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── components/     # ← NEW
    │   └── .gitkeep    # ← (optional)
    ├── services/       # ← NEW
    │   └── .gitkeep    # ← (optional)
    └── hooks/          # ← NEW
        └── .gitkeep    # ← (optional)
```

## Testing Import Paths

Test that TypeScript recognizes the new directories:

Create a test file `src/components/Test.tsx`:
```typescript
export default function Test() {
  return <div>Test Component</div>;
}
```

Import it in `src/app/page.tsx`:
```typescript
import Test from '@/components/Test';
```

Verify:
- No TypeScript errors
- Import resolves correctly
- IDE autocomplete works

Delete test file after verification.

## Troubleshooting

### Issue: Directories not visible
**Solution**: Refresh file explorer or IDE

### Issue: Git doesn't track empty directories
**Solution**: Add .gitkeep files as shown above

### Issue: Import paths don't work
**Solution**:
- Verify tsconfig.json has `"paths": { "@/*": ["./src/*"] }`
- Restart TypeScript server in IDE

### Issue: Permission denied
**Solution**: Run command prompt as Administrator

## Documentation Update

Add to project README:

```markdown
## Project Structure

```
test-app/
└── src/
    ├── app/          # Next.js App Router (pages and layouts)
    ├── components/   # React UI components
    ├── services/     # API client and business logic
    └── hooks/        # Custom React hooks
```

### Directory Purpose

- **app/**: Next.js 14 App Router pages and layouts
- **components/**: Reusable React components (PersonForm, PersonSelector, etc.)
- **services/**: Service layer (API client, sanitization, types)
- **hooks/**: Custom React hooks (usePersons, etc.)
```

## Related Files

- **Previous Story**: Story 01 (Initialize Next.js)
- **Next Epic**: EPIC-02 (Service Layer)
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- Empty directories may not be tracked by git without .gitkeep
- This structure follows Next.js best practices
- All directories use path alias `@/*` for clean imports
- Structure matches the specification in PLAN.md lines 89-117

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: 10 minutes
