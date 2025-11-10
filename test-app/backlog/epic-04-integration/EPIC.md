# EPIC-04: Integration

## Epic Overview

**Epic ID**: EPIC-04
**Epic Name**: Integration
**Epic Owner**: Development Team
**Status**: Pending
**Story Points**: 18
**Priority**: Medium (Critical for end-to-end functionality)

## Business Value Statement

Integrate all components into a cohesive application and test both user flows end-to-end to verify the Person Aggregate Root API works correctly. This epic delivers the complete, working test application.

**Business Impact**: This epic transforms individual components into a functional application that demonstrates API capabilities and validates both critical user flows.

## Current State vs Target State

### Current State
- Components exist in isolation
- No integration between components
- User flows not wired up
- Cannot test API end-to-end

### Target State
- Main page orchestrates all components
- User Flow 1 works: Create person → Add data → Generate persona
- User Flow 2 works: Select person → Add data → Regenerate persona
- Global state managed correctly
- Error handling robust across all operations
- Debug panel logs all API interactions
- Application ready for manual testing

## Technical Approach

### Integration Strategy

1. **Main Page Implementation** (`src/app/page.tsx`)
   - Render all components in correct layout
   - Manage global application state
   - Wire up component callbacks
   - Handle cross-component communication
   - Implement error boundaries

2. **State Management**
   - Persons list (from usePersons hook)
   - Selected person ID
   - Current persona
   - API call log
   - Loading states
   - Error states

3. **User Flow Wiring**
   - Create person → Auto-select → Enable form
   - Submit data → Generate persona → Refresh list → Display persona
   - Select person → Load persona → Enable form
   - Update person → Regenerate → Update display

4. **End-to-End Testing**
   - Test create person flow
   - Test update person flow
   - Test error scenarios
   - Verify debug panel logging

## User Stories

This epic contains the following user stories:

### Story 01: Main Page (8 points)
**As a** developer
**I want** to create the main page that orchestrates all components
**So that** the application is functional

**Tasks**:
1. Create main page with all components
2. Wire up components with props and callbacks
3. Manage global state
4. Setup error handling

### Story 02: API Integration (10 points)
**As a** developer
**I want** to test both user flows end-to-end
**So that** I verify the API integration works

**Tasks**:
1. Test create person flow
2. Test update person flow
3. Test error scenarios
4. Verify debug panel

## Acceptance Criteria

The epic is considered complete when:

1. **Main Page Integration**:
   - All components render in correct layout
   - Global state updates propagate correctly
   - No component isolation issues
   - Error boundaries catch and display errors
   - Loading states synchronized

2. **User Flow 1: Create New Person**:
   - User can click "Create New Person"
   - New person appears in dropdown
   - New person auto-selected
   - Form becomes enabled
   - User can submit data
   - Persona generates and displays
   - Version shows as 1
   - Debug panel logs 3 calls (POST person, POST data, GET persons)

3. **User Flow 2: Update Existing Person**:
   - User can select person from dropdown
   - Existing persona loads and displays
   - Form enabled for selected person
   - User can submit new data
   - Persona regenerates with incremented version
   - Timestamp updates
   - Debug panel logs 2 calls (POST data, GET persons)

4. **Error Handling**:
   - API unreachable → Shows clear error message
   - Invalid input → Form validation prevents submission
   - Server error → Error displayed, app remains functional
   - Network timeout → User notified, can retry

5. **Debug Panel**:
   - Every API call logged with timestamp
   - Request and response bodies shown
   - Status codes color-coded
   - Can copy all logs
   - Can clear logs

6. **State Management**:
   - Persons list stays in sync
   - Selected person persists correctly
   - Persona updates when person changes
   - No stale data displayed

## Definition of Done

- [ ] All user stories completed and accepted
- [ ] All acceptance criteria met
- [ ] Both user flows tested end-to-end
- [ ] Error scenarios tested
- [ ] Debug panel verified
- [ ] No console errors or warnings
- [ ] TypeScript compiles without errors
- [ ] Code reviewed and approved
- [ ] Performance acceptable (<5s per operation)
- [ ] Ready for manual testing phase
- [ ] Code committed to version control

## Dependencies

### Blocks
- **EPIC-05**: Testing & Polish (requires working app)

### Depends On
- **EPIC-01**: Project Setup (requires project structure)
- **EPIC-02**: Service Layer (requires API client and hooks)
- **EPIC-03**: UI Components (requires all components)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| State synchronization bugs | High | Medium | Thorough testing, use React DevTools |
| API timing issues | Medium | Medium | Add loading states, handle race conditions |
| Component prop drilling | Low | Low | Keep state at top level, use context if needed |
| Memory leaks from listeners | Medium | Low | Clean up useEffect dependencies properly |
| Race conditions on rapid clicks | Medium | Medium | Disable buttons during loading, debounce |

## Technical Notes

### Global State Structure

```typescript
// Main page state
const [persons, setPersons] = useState<Person[]>([]);
const [selectedPersonId, setSelectedPersonId] = useState<string | null>(null);
const [currentPersona, setCurrentPersona] = useState<Persona | null>(null);
const [apiCalls, setApiCalls] = useState<ApiCall[]>([]);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [debugPanelOpen, setDebugPanelOpen] = useState(true);
```

### User Flow 1: Create Person Flow

```typescript
async function handleCreateNewPerson() {
  setIsLoading(true);
  setError(null);

  try {
    // 1. Create person
    const person = await createPerson();

    // 2. Add to list and select
    setPersons(prev => [...prev, person]);
    setSelectedPersonId(person.id);

    // 3. Clear current persona (new person has none)
    setCurrentPersona(null);

  } catch (err) {
    setError(`Failed to create person: ${err.message}`);
  } finally {
    setIsLoading(false);
  }
}

async function handleSubmitData(data: { rawText: string; source: string }) {
  if (!selectedPersonId) return;

  setIsLoading(true);
  setError(null);

  try {
    // 1. Submit data and regenerate
    const result = await addPersonDataAndRegenerate(
      selectedPersonId,
      data.rawText,
      data.source
    );

    // 2. Update current persona
    setCurrentPersona(result.persona);

    // 3. Refresh persons list
    const updatedPersons = await listPersons();
    setPersons(updatedPersons);

  } catch (err) {
    setError(`Failed to submit data: ${err.message}`);
  } finally {
    setIsLoading(false);
  }
}
```

### User Flow 2: Update Person Flow

```typescript
async function handlePersonSelect(personId: string | null) {
  setSelectedPersonId(personId);

  if (!personId) {
    setCurrentPersona(null);
    return;
  }

  setIsLoading(true);
  setError(null);

  try {
    // Load persona for selected person
    const persona = await getPersona(personId);
    setCurrentPersona(persona);
  } catch (err) {
    // Person may not have persona yet
    setCurrentPersona(null);
  } finally {
    setIsLoading(false);
  }
}
```

### Error Handling Pattern

```typescript
function ErrorBoundary({ error, onReset }: { error: string; onReset: () => void }) {
  return (
    <div className="bg-red-50 border border-red-300 rounded p-4">
      <h3 className="text-red-800 font-semibold">Error</h3>
      <p className="text-red-600">{error}</p>
      <button onClick={onReset} className="mt-2 text-red-700 underline">
        Dismiss
      </button>
    </div>
  );
}
```

## Estimated Timeline

- **Story 01**: 70 minutes (4 tasks)
- **Story 02**: 65 minutes (4 tasks)
- **Total**: ~135 minutes (2.25 hours)

## Success Metrics

- Both user flows complete successfully
- API calls average <3 seconds response time
- Zero state synchronization bugs
- Error recovery works 100% of the time
- Debug panel logs 100% of API calls
- Zero console errors during normal operation

## Testing Scenarios

### Scenario 1: Happy Path - Create & View
1. App loads with empty persons list
2. Click "Create New Person"
3. New person appears and is selected
4. Enter data in form
5. Submit data
6. Persona generates and displays (version 1)
7. Debug panel shows 3 API calls

### Scenario 2: Happy Path - Update Existing
1. Select existing person from dropdown
2. Existing persona loads and displays
3. Enter new data in form
4. Submit data
5. Persona regenerates (version increments)
6. Debug panel shows 2 new API calls

### Scenario 3: Error Recovery
1. Disconnect API server
2. Try to create person
3. Error message displays
4. Reconnect API server
5. Retry operation
6. Operation succeeds

### Scenario 4: Multiple Persons
1. Create 3 different persons
2. Add data to each
3. Switch between them in dropdown
4. Each shows correct persona
5. No cross-contamination

## Related Documentation

- `test-app/PLAN.md` - Lines 639-704 (User Interaction Flows)
- `test-app/PLAN.md` - Lines 705-761 (Page Layout)
- `test-app/README.md` - Lines 266-295 (Testing scenarios)

## Epic Progress

- [ ] Story 01: Main Page (0/4 tasks)
- [ ] Story 02: API Integration (0/4 tasks)

**Overall Progress**: 0% (0/8 tasks completed)

---

**Epic Created**: 2025-11-09
**Epic Status**: Ready for Execution
**Next Action**: Begin Story 01, Task 01 (Create main page)
