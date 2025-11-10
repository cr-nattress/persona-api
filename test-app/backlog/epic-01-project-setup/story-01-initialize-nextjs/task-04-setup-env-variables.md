# Task 04: Setup Environment Variables

## Task Information

**Task ID**: EPIC-01 / Story 01 / Task 04
**Task Title**: Setup Environment Variables
**Estimated Time**: 5 minutes
**Status**: Pending

## Objective

Create environment variable configuration files for API base URL and other configuration settings.

## Prerequisites

- Task 01-03 completed (Next.js with TypeScript and Tailwind)
- Working directory: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\`

## Agent Prompt

```
Setup environment variables for the Next.js test application to configure API base URL.

CONTEXT:
- Need to configure API endpoint URL
- Must support different environments (development, production)
- Environment variables should be git-ignored for security

REQUIREMENTS:
1. Create .env.local with API configuration
2. Create .env.local.example as template (committed to git)
3. Add .env.local to .gitignore
4. Document environment variables in README
5. Verify variables load correctly in application

STEPS:
1. Create .env.local.example:
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8080

2. Copy to .env.local:
   cp .env.local.example .env.local

3. Verify .gitignore includes .env.local
   (should already be there from create-next-app)

4. Test environment variable loads:
   - Add console.log to page.tsx
   - Verify variable accessible

VERIFICATION:
- .env.local.example exists and committed
- .env.local exists and git-ignored
- Environment variable loads in application
- README documents environment setup

EXPECTED OUTPUT:
- Environment variables configured
- API base URL accessible via process.env.NEXT_PUBLIC_API_BASE_URL
- Template file available for other developers
```

## Step-by-Step Instructions

### Step 1: Create .env.local.example

Create file: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\.env.local.example`

Content:
```bash
# Person Aggregate Root API Base URL
# Default: Local development server
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080

# Example for production:
# NEXT_PUBLIC_API_BASE_URL=https://api.example.com
```

### Step 2: Create .env.local

Create file: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\.env.local`

Content:
```bash
# Person Aggregate Root API Base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

### Step 3: Verify .gitignore

Open `.gitignore` and verify it contains:
```
# local env files
.env*.local
```

If not present, add it.

### Step 4: Test Environment Variable

Update `src/app/page.tsx` to test:

```typescript
export default function Home() {
  // Test environment variable (remove after verification)
  console.log('API Base URL:', process.env.NEXT_PUBLIC_API_BASE_URL);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">
          Person Aggregate Root API Test
        </h1>
        <p className="text-lg text-gray-700">
          API URL: {process.env.NEXT_PUBLIC_API_BASE_URL}
        </p>
      </div>
    </main>
  );
}
```

### Step 5: Verify in Browser

1. Run dev server: `npm run dev`
2. Open http://localhost:3000
3. Check browser console for: `API Base URL: http://localhost:8080`
4. Check page displays API URL
5. Remove test code after verification

## Verification Checklist

- [ ] `.env.local.example` created
- [ ] `.env.local.example` contains `NEXT_PUBLIC_API_BASE_URL`
- [ ] `.env.local` created
- [ ] `.env.local` contains correct API URL
- [ ] `.gitignore` includes `.env*.local`
- [ ] Environment variable loads in application
- [ ] Console shows correct API URL
- [ ] Page displays API URL correctly
- [ ] `.env.local` is git-ignored (not tracked)
- [ ] `.env.local.example` is committed to git

## Environment Variable Guidelines

### Naming Convention

Next.js requires client-side environment variables to be prefixed with `NEXT_PUBLIC_`:

```bash
# Client-side accessible (browser)
NEXT_PUBLIC_API_BASE_URL=...

# Server-side only (Node.js)
DATABASE_URL=... # Not prefixed, not accessible in browser
```

### Using Environment Variables

```typescript
// In React components or client-side code
const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

// Example: API client
async function fetchData() {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/v1/person`);
  return response.json();
}
```

### Multiple Environments

```bash
# .env.local (development)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080

# .env.production (production)
NEXT_PUBLIC_API_BASE_URL=https://persona-api-prod.example.com

# .env.test (testing)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

## Troubleshooting

### Issue: Environment variable is undefined
**Solution**:
- Ensure variable prefixed with `NEXT_PUBLIC_`
- Restart dev server after changing .env files
- Check .env.local exists and has correct syntax

### Issue: Variable works locally but not in production
**Solution**:
- Set environment variables in deployment platform (Vercel, Netlify, etc.)
- Don't rely on .env.local in production (it's git-ignored)

### Issue: .env.local tracked by git
**Solution**:
- Remove from git: `git rm --cached .env.local`
- Verify .gitignore includes `.env*.local`
- Commit .gitignore changes

## Security Notes

- Never commit `.env.local` to version control
- Never include secrets or API keys in `NEXT_PUBLIC_` variables (they're exposed to browser)
- Use server-side environment variables for sensitive data
- `.env.local.example` should contain example values only, not real credentials

## Documentation Update

Add to project README:

```markdown
## Environment Setup

1. Copy environment template:
   ```bash
   cp .env.local.example .env.local
   ```

2. Update `.env.local` with your API endpoint:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
   ```

3. Restart development server to load new environment variables.

### Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Person Aggregate Root API base URL (default: http://localhost:8080)
```

## Related Files

- **Previous Task**: task-03-configure-tailwind.md
- **Next Story**: Story 02 (Project Structure)
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- Environment variables in Next.js are replaced at build time
- Changes to .env files require dev server restart
- NEXT_PUBLIC_ variables are embedded in the browser bundle
- Keep .env.local.example up to date as template for other developers

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: 5 minutes
