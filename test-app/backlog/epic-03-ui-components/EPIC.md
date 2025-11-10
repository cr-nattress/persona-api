# EPIC-03: UI Components

## Epic Overview

**Epic ID**: EPIC-03
**Epic Name**: UI Components
**Epic Owner**: Development Team
**Status**: Pending
**Story Points**: 29
**Priority**: Medium (Core functionality)

## Business Value Statement

Build all React UI components that users interact with to create persons, submit data, view personas, and debug API calls. These components deliver the primary user experience and verify API functionality.

**Business Impact**: These components enable users to test the Person Aggregate Root API through an intuitive interface, making it easy to verify both user flows work correctly.

## Current State vs Target State

### Current State
- No UI components exist
- No way for users to interact with API
- Cannot visualize API responses
- No debugging capability

### Target State
- PersonForm accepts and sanitizes user input
- PersonSelector shows all available persons
- PersonaDisplay renders generated personas beautifully
- ApiDebugPanel logs all API calls for troubleshooting
- Loading component provides feedback during operations
- All components styled with Tailwind CSS
- Fully responsive and accessible

## Technical Approach

### Component Architecture

1. **PersonForm** - Data submission form
   - Large textarea for raw text input
   - Character/byte counter (0-100,000)
   - Source dropdown selector
   - Real-time sanitization
   - Validation error messages
   - Submit and clear buttons

2. **PersonSelector** - Person dropdown
   - Lists all available persons
   - "Create New Person" option
   - Shows person ID and metadata
   - Disabled state during loading

3. **PersonaDisplay** - Persona viewer
   - Formatted JSON display
   - Metadata (version, timestamps, data count)
   - Copy to clipboard functionality
   - Collapsible sections

4. **ApiDebugPanel** - API call logger
   - Lists all API calls chronologically
   - Shows request/response bodies
   - Color-coded status codes
   - Collapsible panel
   - Copy all and clear functions

5. **Loading** - Loading indicator
   - Spinner animation
   - Optional message
   - Used across all async operations

## User Stories

This epic contains the following user stories:

### Story 01: Form Component (8 points)
**As a** user
**I want** to submit unstructured data about a person
**So that** a persona can be generated

**Tasks**:
1. Create PersonForm component structure
2. Add sanitization integration
3. Add validation feedback
4. Style PersonForm with Tailwind

### Story 02: Selector Component (5 points)
**As a** user
**I want** to select a person from a dropdown
**So that** I can view or update their persona

**Tasks**:
1. Create PersonSelector component
2. Implement dropdown logic
3. Style PersonSelector with Tailwind

### Story 03: Display Component (5 points)
**As a** user
**I want** to view the generated persona
**So that** I can verify the API output

**Tasks**:
1. Create PersonaDisplay component
2. Format JSON display
3. Style PersonaDisplay with Tailwind

### Story 04: Debug Panel (8 points)
**As a** developer
**I want** to view all API calls in a debug panel
**So that** I can troubleshoot issues

**Tasks**:
1. Create ApiDebugPanel component
2. Implement API logging display
3. Add copy functionality
4. Style debug panel with Tailwind

### Story 05: Loading Component (3 points)
**As a** user
**I want** to see loading indicators
**So that** I know when operations are in progress

**Tasks**:
1. Create Loading spinner component

## Acceptance Criteria

The epic is considered complete when:

1. **PersonForm**:
   - Accepts text input up to 100,000 bytes
   - Sanitizes input in real-time
   - Shows byte counter
   - Displays validation errors clearly
   - Submits sanitized data to parent
   - Clears form after submission

2. **PersonSelector**:
   - Lists all persons with ID and metadata
   - Shows "Create New Person" option
   - Triggers callback on selection
   - Disables during loading states
   - Shows empty state when no persons

3. **PersonaDisplay**:
   - Renders JSON with formatting
   - Shows metadata (version, timestamps)
   - Copy button works correctly
   - Shows loading state
   - Shows empty state when no persona

4. **ApiDebugPanel**:
   - Lists all API calls chronologically
   - Shows request method, endpoint, status
   - Displays request and response bodies
   - Color codes by status (2xx green, 4xx yellow, 5xx red)
   - Copy all button works
   - Clear button empties log
   - Collapsible to save space

5. **Loading**:
   - Shows spinner animation
   - Displays optional message
   - Works across all components

6. **General**:
   - All components fully typed with TypeScript
   - No prop-types warnings
   - Responsive on desktop and tablet
   - Tailwind classes applied correctly
   - No accessibility violations

## Definition of Done

- [ ] All user stories completed and accepted
- [ ] All acceptance criteria met
- [ ] TypeScript compiles without errors
- [ ] No React warnings in console
- [ ] All props fully typed
- [ ] Components responsive on desktop/tablet
- [ ] Keyboard navigation works
- [ ] ARIA labels added where needed
- [ ] Code reviewed and approved
- [ ] Components tested in isolation
- [ ] Code committed to version control

## Dependencies

### Blocks
- **EPIC-04**: Integration (main page needs components)

### Depends On
- **EPIC-01**: Project Setup (requires Next.js structure)
- **EPIC-02**: Service Layer (components use services and hooks)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Component re-render loops | High | Medium | Use React.memo, useCallback properly |
| Textarea performance with large text | Medium | Low | Debounce character counter updates |
| JSON formatting breaks on edge cases | Medium | Low | Use try-catch, show raw JSON on error |
| Copy to clipboard doesn't work | Low | Low | Feature detect, provide fallback |
| Accessibility issues | Medium | Medium | Use semantic HTML, add ARIA labels |

## Technical Notes

### Component Props

```typescript
// PersonForm
interface PersonFormProps {
  personId: string | null;
  isLoading: boolean;
  onSubmit: (data: { rawText: string; source: string }) => void;
}

// PersonSelector
interface PersonSelectorProps {
  persons: Person[];
  selectedPersonId: string | null;
  onSelect: (personId: string | null) => void;
  onCreateNew: () => void;
  isLoading: boolean;
}

// PersonaDisplay
interface PersonaDisplayProps {
  persona: Persona | null;
  personDataCount: number;
  isLoading: boolean;
  onRefresh?: () => void;
}

// ApiDebugPanel
interface ApiDebugPanelProps {
  calls: ApiCall[];
  isOpen: boolean;
  onToggle: () => void;
  onClear: () => void;
}

// Loading
interface LoadingProps {
  isLoading: boolean;
  message?: string;
}
```

### Styling Guidelines

- Use Tailwind utility classes
- Consistent spacing (p-4, m-2, etc.)
- Color scheme:
  - Primary: blue-600
  - Success: green-600
  - Error: red-600
  - Warning: yellow-600
- Borders: border-gray-300
- Backgrounds: bg-white, bg-gray-50

## Estimated Timeline

- **Story 01**: 55 minutes (4 tasks)
- **Story 02**: 35 minutes (3 tasks)
- **Story 03**: 35 minutes (3 tasks)
- **Story 04**: 55 minutes (4 tasks)
- **Story 05**: 10 minutes (1 task)
- **Total**: ~195 minutes (3.25 hours)

## Parallelization Opportunities

All 5 stories can be developed in parallel after EPIC-02 completes:

- **Developer 1**: Story 01 (PersonForm) + Story 02 (PersonSelector)
- **Developer 2**: Story 03 (PersonaDisplay) + Story 04 (ApiDebugPanel)
- **Developer 3**: Story 05 (Loading) - quick, can help with others

This parallelization can reduce elapsed time from 195 minutes to ~90 minutes with 2-3 developers.

## Success Metrics

- All components render without errors
- Form sanitization catches 100% of test cases
- Dropdown shows all persons correctly
- Debug panel logs every API call
- No console warnings or errors
- Performance: <100ms render time per component

## Related Documentation

- `test-app/PLAN.md` - Lines 122-489 (Component Architecture)
- `test-app/README.md` - Lines 71-186 (Component summary)
- `test-app/SANITIZATION.md` - Input sanitization for PersonForm

## Epic Progress

- [ ] Story 01: Form Component (0/4 tasks)
- [ ] Story 02: Selector Component (0/3 tasks)
- [ ] Story 03: Display Component (0/3 tasks)
- [ ] Story 04: Debug Panel (0/4 tasks)
- [ ] Story 05: Loading Component (0/1 tasks)

**Overall Progress**: 0% (0/14 tasks completed)

---

**Epic Created**: 2025-11-09
**Epic Status**: Ready for Execution
**Next Action**: Begin Story 01, Task 01 (Create PersonForm component)
