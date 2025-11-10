# Test App Documentation Index

Complete planning and specification for the Next.js Person Aggregate Root test application with input sanitization.

## 📋 Documents

### 1. **README.md** (334 lines)
Quick reference guide with:
- Project overview and purpose
- Tech stack
- Directory structure
- Component breakdown
- API endpoints reference
- Sanitization summary
- Testing scenarios
- Success criteria

**Start here for quick overview** ↑

---

### 2. **PLAN.md** (978 lines)
Comprehensive specification with:
- Functional & non-functional requirements
- Complete architecture
- 6 component specifications (Person Selector, Form, Display, Debug Panel, Loading)
- Service layer (API client, Sanitization service)
- Type definitions
- Custom hooks
- User interaction flows
- Page layouts with ASCII mockups
- Error handling strategy
- Testing scenarios
- Implementation phases

**Read this for complete implementation guide** ↑

---

### 3. **SANITIZATION.md** (454 lines) — NEW
Detailed input sanitization & escaping guide with:
- Why sanitization matters
- What to sanitize (9 categories)
- What NOT to sanitize (special chars, emoji, unicode)
- Step-by-step implementation
- Code examples
- Service layer structure
- User feedback messages
- Testing scenarios
- Security considerations
- Implementation checklist

**Reference this when implementing input cleaning** ↑

---

## 🎯 Quick Start

1. **First time?** → Read `README.md` (5 min)
2. **Planning implementation?** → Read `PLAN.md` (20 min)
3. **Coding the form?** → Read `SANITIZATION.md` (10 min)
4. **Have questions?** → Check the specific document's section

---

## 📁 Directory Structure

```
test-app/
├── INDEX.md                    ← You are here
├── README.md                   ← Quick reference
├── PLAN.md                     ← Complete specification
├── SANITIZATION.md             ← Input cleaning guide
├── package.json               ← Dependencies (to create)
├── tsconfig.json              ← TypeScript config (to create)
├── next.config.js             ← Next.js config (to create)
├── .env.local.example         ← Environment template (to create)
├── public/
└── src/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    ├── components/
    │   ├── PersonForm.tsx        ← Uses sanitization
    │   ├── PersonSelector.tsx
    │   ├── PersonaDisplay.tsx
    │   ├── ApiDebugPanel.tsx
    │   └── Loading.tsx
    ├── services/
    │   ├── api.ts
    │   ├── sanitizer.ts          ← NEW (input cleaning)
    │   └── types.ts
    └── hooks/
        └── usePersons.ts
```

---

## 🔧 Key Additions (Input Sanitization)

### New Service: `sanitizer.ts`

Three main functions:

```typescript
// 1. Clean user input
sanitizeRawText(input: string): string

// 2. Validate cleaned input
validateSanitizedInput(input: string): { valid, error?, byteLength? }

// 3. Escape for JSON (if needed)
escapeForJson(input: string): string
```

### What Gets Cleaned

| Problem | Solution |
|---------|----------|
| Extra spaces | Collapse to single space |
| Mixed line endings | Normalize to \n |
| Control characters | Remove (except \n, \t, \r) |
| Zero-width chars | Remove invisible characters |
| Null bytes | Strip \0 |
| Invalid UTF-8 | Validate & reject if bad |

### What Gets Preserved

✓ Special characters (!, @, #, etc.)
✓ Emoji (👋 🌍 ✨)
✓ Unicode (international text)
✓ Quotes & brackets
✓ Intentional whitespace structure

---

## 📊 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| PLAN.md | 978 | Complete spec |
| README.md | 334 | Quick ref |
| SANITIZATION.md | 454 | Input cleaning |
| **Total** | **1,766** | **Full planning** |

---

## ✅ What's Covered

- [x] User flows documented
- [x] Component architecture designed
- [x] API integration planned
- [x] Error handling strategy
- [x] Input sanitization specification (NEW)
- [x] Testing scenarios
- [x] Implementation phases
- [x] Success criteria

## ⏭️ Next Steps

When ready to implement:

1. Initialize Next.js project
2. Follow PLAN.md implementation phases
3. Use SANITIZATION.md for form component
4. Test both user flows
5. Verify debug panel logs API calls

---

## 📚 Related Documentation

- `../IMPLEMENTATION-PLAN.md` - Person Aggregate Root API design
- `../PLAN.md` (in this dir) - Complete test app spec
- `../docs/DEPLOYMENT_GUIDE.md` - API deployment

---

## 📝 Notes

- This is a test/demo application
- Focus on functionality over perfection
- Sanitization is critical for reliability
- Input validation should happen at both UI and API level
- Debug panel is essential for troubleshooting API integration

---

**Status**: 📋 Complete Planning Phase
**No code implemented yet** — Ready for development

---

Created: 2025-11-09
Version: 1.0 (with Input Sanitization)
