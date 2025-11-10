# Quick Start Guide - Person Aggregate Root API Test App

## Prerequisites

1. **API Server Running**
   ```bash
   # In the main project directory
   cd persona-api
   ./run_local.sh  # or your API startup command
   ```
   Verify API is running: http://localhost:8080/health

2. **Node.js 18+**
   ```bash
   node --version  # Should be v18 or higher
   ```

## Setup (One-Time)

```bash
# Navigate to test app
cd test-app

# Install dependencies
npm install

# Verify environment config
cat .env.local
# Should show: NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

## Run the App

```bash
# Start development server
npm run dev
```

Open http://localhost:3000 in your browser

## Test User Flow 1: Create New Person

1. Click **"+ Create New"** button
2. Enter sample data:
   ```
   John Doe is a software engineer with 10 years of experience.
   He specializes in JavaScript, React, and TypeScript.
   ```
3. Click **"Submit Data"**
4. Verify persona appears with version 1
5. Check Debug Panel shows API calls

## Test User Flow 2: Update Person

1. Keep same person selected
2. Enter more data:
   ```
   John recently completed a cloud architecture certification.
   He enjoys hiking and photography.
   ```
3. Click **"Submit Data"**
4. Verify version increments to 2
5. Verify data count shows 2

## Success Indicators

- No errors in browser console
- Debug panel shows all API calls with green status codes
- Persona JSON displays correctly
- Byte counter updates in real-time
- Form clears after submission

## Troubleshooting

**Can't connect to API**
```bash
# Verify API is running
curl http://localhost:8080/health

# Check environment variable
cat .env.local
```

**Port 3000 already in use**
```bash
# Use different port
npm run dev -- -p 3001
```

**TypeScript errors**
```bash
# Check compilation
npx tsc --noEmit
```

## Next Steps

- Read full documentation: `APP_README.md`
- Complete testing checklist: `TESTING_CHECKLIST.md`
- Review implementation: `IMPLEMENTATION_SUMMARY.md`

---

**Ready to test in under 2 minutes!**
