# Person Aggregate Root API - Test Application

A Next.js 16 application for testing and verifying the Person Aggregate Root API endpoints.

## Features

- Create new persons and generate personas
- Submit unstructured data with automatic sanitization
- Real-time persona generation and versioning
- API call debugging panel with request/response logging
- Input validation and byte counting
- Responsive UI with Tailwind CSS

## Prerequisites

- Node.js 18+ installed
- Person Aggregate Root API running (default: http://localhost:8080)
- npm or pnpm package manager

## Quick Start

### 1. Install Dependencies

```bash
cd test-app
npm install
```

### 2. Configure Environment

Create `.env.local` file (or copy from `.env.local.example`):

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

### 3. Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## User Flows

### Flow 1: Create New Person with Persona

1. Click **"+ Create New"** button
2. New person appears in dropdown (automatically selected)
3. Enter unstructured data in the text area
4. Select data source from dropdown
5. Click **"Submit Data"**
6. Persona generates and displays on the right
7. Version starts at 1

### Flow 2: Update Existing Person

1. Select existing person from dropdown
2. Current persona loads (if exists)
3. Enter new unstructured data
4. Click **"Submit Data"**
5. Persona regenerates with updated information
6. Version increments (1 → 2, 2 → 3, etc.)
7. Data count increases

## Features

### Input Sanitization

All user input is automatically sanitized:

- Removes null bytes and control characters
- Normalizes line endings
- Collapses excessive whitespace
- Validates UTF-8 encoding
- Enforces 100,000 byte limit

### Real-time Validation

- Byte counter (not character count)
- Validation errors displayed inline
- Submit button disabled if invalid

### Debug Panel

- Logs all API calls with timestamps
- Shows request/response bodies
- Color-coded status (green=success, red=error, yellow=warning)
- Copy individual calls or all calls
- Expandable details for each call

## Project Structure

```
test-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Main page (orchestrates all components)
│   │   └── globals.css         # Global styles + Tailwind
│   ├── components/
│   │   ├── PersonSelector.tsx  # Person dropdown + create new
│   │   ├── PersonForm.tsx      # Data submission form
│   │   ├── PersonaDisplay.tsx  # Persona viewer
│   │   ├── ApiDebugPanel.tsx   # API call logger
│   │   └── Loading.tsx         # Loading indicator
│   ├── services/
│   │   ├── api.ts              # API client with logging
│   │   ├── sanitizer.ts        # Input sanitization
│   │   └── types.ts            # TypeScript types
│   └── hooks/
│       └── usePersons.ts       # Custom hook for person management
├── .env.local                  # Environment config (git-ignored)
├── .env.local.example          # Example config
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.ts          # Tailwind config
└── next.config.ts              # Next.js config
```

## API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v1/person` | Create new person |
| GET | `/v1/person` | List all persons |
| POST | `/v1/person/:id/data-and-regenerate` | Add data + regenerate persona |
| GET | `/v1/person/:id/persona` | Get latest persona |
| GET | `/v1/person/:id/data` | Get person data history |

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# TypeScript type checking
npx tsc --noEmit
```

## Technology Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4 (via @tailwindcss/postcss)
- **HTTP Client**: Native fetch API
- **State Management**: React hooks (useState, useEffect, useCallback)
- **Runtime**: Node.js 18+

## Troubleshooting

### API Connection Failed

**Error**: "Unable to connect to API"

**Solution**:
1. Verify API is running: `curl http://localhost:8080/health`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_BASE_URL`
3. Ensure no firewall blocking port 8080

### Text Exceeds Limit

**Error**: "Text exceeds limit: X bytes (max 100,000)"

**Solution**:
1. Input is measured in bytes (not characters)
2. Emoji and special characters use multiple bytes
3. Reduce text length to under 100,000 bytes

### Persona Not Generating

**Issue**: Data submitted but no persona displayed

**Solution**:
1. Check Debug Panel for API errors
2. Verify API is processing persona generation
3. Try refreshing the persona manually
4. Check browser console for errors

### TypeScript Errors

**Issue**: TypeScript compilation fails

**Solution**:
```bash
# Check for errors
npx tsc --noEmit

# Clear build cache
rm -rf .next
npm run dev
```

## Testing Scenarios

### Test 1: Create Person Flow

1. Click "Create New"
2. Enter data: "John Doe is a software engineer with 10 years of experience"
3. Submit
4. Verify persona generates with version 1
5. Check debug panel shows 3 API calls (create, add data, list)

### Test 2: Update Person Flow

1. Select existing person
2. Enter new data: "John recently learned Python and machine learning"
3. Submit
4. Verify persona updates with version 2
5. Check data count increments

### Test 3: Sanitization

1. Enter text with extra spaces: "Hello    world"
2. Verify cleaned to: "Hello world"
3. Enter text with control characters
4. Verify they are removed

### Test 4: Validation

1. Try to submit empty text → Error displayed
2. Try to submit 101KB text → Error displayed
3. Verify byte counter updates in real-time

### Test 5: Error Handling

1. Stop API server
2. Try to submit data
3. Verify error message displays
4. Restart API and retry
5. Verify success

## Known Limitations

- No authentication (test app only)
- No data persistence on refresh (relies on API state)
- No pagination for large person lists
- No search/filter functionality
- Single-user application (no concurrent users)

## Contributing

This is a test application for the Person Aggregate Root API. For production use, additional features should be added:

- User authentication
- Error boundaries
- Loading states
- Accessibility improvements
- Unit and integration tests
- Performance optimizations

## License

ISC

## Support

For issues related to:
- **API**: See main project documentation
- **Test App**: Check browser console and Debug Panel
- **TypeScript**: Run `npx tsc --noEmit` for details

---

**Built with Next.js 16 + TypeScript | Last Updated: 2025-11-09**
