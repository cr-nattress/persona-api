# Task 02: Setup TypeScript

## Task Information

**Task ID**: EPIC-01 / Story 01 / Task 02
**Task Title**: Setup TypeScript
**Estimated Time**: 10 minutes
**Status**: Pending

## Objective

Configure TypeScript with strict mode and recommended compiler options for Next.js development.

## Prerequisites

- Task 01 completed (Next.js project created)
- TypeScript installed by create-next-app
- Working directory: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\`

## Agent Prompt

```
Configure TypeScript for the Next.js test application with strict mode and optimal compiler options.

CONTEXT:
- Next.js 14+ project with TypeScript already initialized
- Need to configure tsconfig.json with strict mode
- Ensure type safety and IDE IntelliSense work correctly

REQUIREMENTS:
1. Enable TypeScript strict mode
2. Configure compiler options for Next.js
3. Verify TypeScript compilation works
4. Ensure no type errors in existing files

STEPS:
1. Open tsconfig.json
2. Update compiler options with strict settings:
   - strict: true
   - noUnusedLocals: true
   - noUnusedParameters: true
   - noFallthroughCasesInSwitch: true
   - forceConsistentCasingInFileNames: true
   - esModuleInterop: true
   - skipLibCheck: true

3. Verify configuration:
   - Run: npx tsc --noEmit
   - Ensure no compilation errors

4. Test in IDE:
   - Open src/app/page.tsx
   - Verify IntelliSense works
   - Verify type checking highlights errors

VERIFICATION:
- tsconfig.json contains strict mode settings
- TypeScript compiles without errors
- IDE shows type hints and errors
- No console warnings during dev server startup

EXPECTED OUTPUT:
- Updated tsconfig.json with strict configuration
- TypeScript compilation successful
- Full type safety enabled
```

## Step-by-Step Instructions

### Step 1: Open tsconfig.json

Navigate to and open:
```
C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\tsconfig.json
```

### Step 2: Update Compiler Options

Replace the existing `tsconfig.json` with:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "forceConsistentCasingInFileNames": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Step 3: Verify TypeScript Compilation

Run the TypeScript compiler in check mode:
```bash
npx tsc --noEmit
```

Expected output:
```
(no output means success - TypeScript compiled without errors)
```

### Step 4: Test Development Server

Start the dev server:
```bash
npm run dev
```

Verify no TypeScript errors appear in the console.

### Step 5: Test IDE IntelliSense

1. Open `src/app/page.tsx` in your IDE
2. Hover over a variable to see type hints
3. Try adding an invalid type to test error highlighting
4. Remove the test error

## Verification Checklist

- [ ] `tsconfig.json` updated with strict mode
- [ ] `"strict": true` enabled
- [ ] `"noUnusedLocals": true` enabled
- [ ] `"noUnusedParameters": true` enabled
- [ ] `"noFallthroughCasesInSwitch": true` enabled
- [ ] `npx tsc --noEmit` runs without errors
- [ ] Development server starts without TypeScript errors
- [ ] IDE shows type hints on hover
- [ ] IDE highlights type errors with red underlines
- [ ] No warnings in console

## Expected Configuration

Key strict mode settings:

```typescript
// Enable all strict type checking
"strict": true

// Disallow unused local variables
"noUnusedLocals": true

// Disallow unused function parameters
"noUnusedParameters": true

// Ensure switch statements are exhaustive
"noFallthroughCasesInSwitch": true

// Enforce consistent file name casing
"forceConsistentCasingInFileNames": true
```

## Troubleshooting

### Issue: TypeScript errors in existing files
**Solution**: Review and fix each error. Most will be simple type annotations.

### Issue: IDE not showing type hints
**Solution**:
- Restart IDE
- Ensure TypeScript extension installed (VS Code: built-in)
- Check workspace uses correct TypeScript version

### Issue: Module resolution errors
**Solution**: Verify `moduleResolution: "bundler"` is set correctly

### Issue: Path alias not working
**Solution**: Verify `paths` configuration includes `"@/*": ["./src/*"]`

## Testing Type Safety

Add this code to test TypeScript strict mode:

```typescript
// In src/app/page.tsx, temporarily add:

// This should show an error (strict mode catches it)
const test: string = 123; // Type 'number' is not assignable to type 'string'

// Remove this test code after verification
```

## Related Files

- **Previous Task**: task-01-create-nextjs-project.md
- **Next Task**: task-03-configure-tailwind.md
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- Strict mode helps catch bugs early
- noUnusedLocals prevents accumulating dead code
- These settings are recommended for all TypeScript projects
- Next.js uses TypeScript plugin for enhanced checking

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: 10 minutes
