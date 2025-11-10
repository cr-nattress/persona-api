# Task 03: Configure Tailwind CSS

## Task Information

**Task ID**: EPIC-01 / Story 01 / Task 03
**Task Title**: Configure Tailwind CSS
**Estimated Time**: 15 minutes
**Status**: Pending

## Objective

Install and configure Tailwind CSS 3+ for styling the Next.js test application.

## Prerequisites

- Task 01 completed (Next.js project created)
- Task 02 completed (TypeScript configured)
- Working directory: `C:\Users\RED\OneDrive\Documents\github\persona-api\test-app\`

## Agent Prompt

```
Install and configure Tailwind CSS for the Next.js test application.

CONTEXT:
- Next.js 14+ project with TypeScript
- Need Tailwind CSS for component styling
- Using App Router structure

REQUIREMENTS:
1. Install Tailwind CSS 3+ and dependencies
2. Create tailwind.config.js with Next.js paths
3. Create postcss.config.js
4. Add Tailwind directives to globals.css
5. Verify Tailwind classes work in components

STEPS:
1. Install Tailwind CSS and dependencies:
   npm install -D tailwindcss postcss autoprefixer

2. Initialize Tailwind configuration:
   npx tailwindcss init -p

3. Update tailwind.config.js to scan Next.js files:
   content: [
     './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
     './src/components/**/*.{js,ts,jsx,tsx,mdx}',
     './src/app/**/*.{js,ts,jsx,tsx,mdx}',
   ]

4. Add Tailwind directives to src/app/globals.css:
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

5. Test Tailwind classes work:
   - Add a test class to src/app/page.tsx
   - Run dev server
   - Verify styles apply

VERIFICATION:
- Tailwind CSS installed in package.json
- tailwind.config.js exists with correct content paths
- postcss.config.js exists
- globals.css has Tailwind directives
- Tailwind utility classes work in components
- No CSS compilation errors

EXPECTED OUTPUT:
- Tailwind CSS configured and functional
- Styles apply correctly in browser
- Ready for component styling
```

## Step-by-Step Instructions

### Step 1: Install Tailwind CSS

Run:
```bash
npm install -D tailwindcss postcss autoprefixer
```

### Step 2: Initialize Tailwind Config

Run:
```bash
npx tailwindcss init -p
```

This creates:
- `tailwind.config.js`
- `postcss.config.js`

### Step 3: Configure Tailwind Content Paths

Open `tailwind.config.js` and replace with:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Step 4: Add Tailwind Directives to CSS

Open `src/app/globals.css` and replace entire contents with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles (optional) */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Step 5: Test Tailwind Classes

Open `src/app/page.tsx` and update to test Tailwind:

```typescript
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">
          Person Aggregate Root API Test
        </h1>
        <p className="text-lg text-gray-700">
          Tailwind CSS is configured successfully!
        </p>
      </div>
    </main>
  );
}
```

### Step 6: Verify in Browser

Run dev server:
```bash
npm run dev
```

Open http://localhost:3000 and verify:
- Text is blue (blue-600)
- Text is bold (font-bold)
- Layout is centered (flex, items-center, justify-center)
- Spacing applied correctly (p-24, mb-4)

## Verification Checklist

- [ ] Tailwind CSS installed in `package.json` devDependencies
- [ ] `tailwind.config.js` exists
- [ ] `postcss.config.js` exists
- [ ] `globals.css` contains Tailwind directives
- [ ] Dev server compiles CSS without errors
- [ ] Tailwind classes apply correctly in browser
- [ ] No CSS warnings in console
- [ ] Text appears blue and bold as expected
- [ ] Layout matches Tailwind utilities

## Expected Files

### tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### postcss.config.js
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

## Troubleshooting

### Issue: Tailwind classes not applying
**Solution**:
- Verify `content` paths in tailwind.config.js
- Check globals.css has @tailwind directives
- Clear .next cache and restart dev server

### Issue: CSS not updating after changes
**Solution**:
- Stop dev server (Ctrl+C)
- Delete `.next` folder
- Restart: `npm run dev`

### Issue: Build errors with Tailwind
**Solution**:
- Verify postcss.config.js exists
- Check tailwindcss is in devDependencies
- Run `npm install` again

### Issue: Styles flash/change on page load
**Solution**: This is normal in development mode. Production build will optimize CSS.

## Testing Tailwind

Test these utility classes to verify Tailwind works:

```html
<!-- Colors -->
<div className="bg-blue-500 text-white">Blue background</div>

<!-- Spacing -->
<div className="p-4 m-2">Padding and margin</div>

<!-- Typography -->
<h1 className="text-4xl font-bold">Large bold text</h1>

<!-- Layout -->
<div className="flex items-center justify-center">Centered flex</div>

<!-- Responsive -->
<div className="md:w-1/2 lg:w-1/3">Responsive width</div>
```

## Related Files

- **Previous Task**: task-02-setup-typescript.md
- **Next Task**: task-04-setup-env-variables.md
- **Story**: STORY.md
- **Epic**: ../EPIC.md

## Notes

- Tailwind CSS is installed as devDependency
- PostCSS and Autoprefixer handle CSS processing
- Content paths tell Tailwind which files to scan for classes
- Unused classes are purged in production builds
- Custom theme extensions can be added later if needed

---

**Task Created**: 2025-11-09
**Task Status**: Ready for Execution
**Estimated Duration**: 15 minutes
