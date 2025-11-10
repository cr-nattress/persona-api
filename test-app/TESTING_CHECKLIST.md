# Testing Checklist - Person Aggregate Root API Test App

## Pre-Test Setup

- [ ] API server running at http://localhost:8080
- [ ] Test app running at http://localhost:3000
- [ ] Browser console open for debugging
- [ ] Debug panel open in UI

## User Flow 1: Create New Person

### Steps

- [ ] Click "Create New Person" button
- [ ] Verify new person appears in dropdown
- [ ] Verify person is auto-selected
- [ ] Person has ID visible in dropdown
- [ ] Person has 0 data count, null version
- [ ] Debug panel shows POST /v1/person with 201 status

### Data Submission

- [ ] Enter test data in textarea:
  ```
  John Doe is a 35-year-old software engineer with 10 years of experience in web development.
  He specializes in JavaScript, TypeScript, and React.
  ```
- [ ] Verify byte counter updates in real-time
- [ ] Select source: "api"
- [ ] Click "Submit Data"
- [ ] Verify "Submitting..." appears on button
- [ ] Wait for completion

### Persona Generation

- [ ] Persona appears on right side
- [ ] Version shows: 1
- [ ] Data count shows: 1
- [ ] Persona JSON is formatted
- [ ] Created timestamp is recent
- [ ] Computed from 1 data point
- [ ] "Copy JSON" button works
- [ ] Debug panel shows POST /v1/person/:id/data-and-regenerate
- [ ] Debug panel shows successful response (200/201)
- [ ] Person dropdown updates with new data count

### Verification

- [ ] No errors in browser console
- [ ] No errors in debug panel
- [ ] Form clears after submission
- [ ] Can repeat the process

## User Flow 2: Update Existing Person

### Steps

- [ ] Select person from dropdown (use person from Flow 1)
- [ ] Verify existing persona loads
- [ ] Version shows: 1 (from previous)
- [ ] Data count shows: 1

### Add More Data

- [ ] Enter new data:
  ```
  John recently completed a certification in cloud architecture.
  He is now working on microservices and Kubernetes deployments.
  ```
- [ ] Verify byte counter updates
- [ ] Select source: "interview"
- [ ] Click "Submit Data"

### Persona Regeneration

- [ ] Persona updates with new information
- [ ] Version increments to: 2
- [ ] Data count increments to: 2
- [ ] Persona JSON includes both data points
- [ ] Timestamp updates
- [ ] Computed from 2 data points
- [ ] Debug panel shows new API call
- [ ] Person dropdown updates

### Repeat Update

- [ ] Add third piece of data:
  ```
  John enjoys hiking and photography in his free time.
  ```
- [ ] Submit
- [ ] Verify version: 3
- [ ] Verify data count: 3
- [ ] Verify persona reflects all information

## Input Sanitization Tests

### Whitespace Handling

- [ ] Enter: `"Hello    world    test"`
- [ ] Verify sanitized to: `"Hello world test"`
- [ ] Byte counter updates correctly

### Line Endings

- [ ] Enter text with Windows line endings (\r\n)
- [ ] Verify normalized to Unix (\n)
- [ ] Multiline text preserves structure

### Special Characters

- [ ] Enter: `"Email: test@example.com | Phone: +1-555-1234"`
- [ ] Verify all characters preserved
- [ ] No sanitization of valid punctuation

### Emoji Support

- [ ] Enter: `"John loves coffee ☕ and coding 💻"`
- [ ] Verify emoji preserved
- [ ] Byte count correct (emoji = 4 bytes each)

### Control Characters

- [ ] Copy text with hidden control characters
- [ ] Paste into textarea
- [ ] Verify control characters removed
- [ ] Text remains readable

## Validation Tests

### Empty Input

- [ ] Try to submit empty text
- [ ] Verify error: "Text cannot be empty"
- [ ] Submit button disabled
- [ ] No API call made

### Oversized Input

- [ ] Create 101,000 byte text (repeat "x" 101000 times)
- [ ] Paste into textarea
- [ ] Verify error shows: "Text exceeds limit"
- [ ] Byte counter shows red
- [ ] Submit button disabled

### No Person Selected

- [ ] Deselect person (choose "-- Choose a person --")
- [ ] Try to submit data
- [ ] Verify error: "Please select or create a person first"
- [ ] Submit button disabled

## Error Handling Tests

### API Unavailable

- [ ] Stop the API server
- [ ] Try to create new person
- [ ] Verify error message displays
- [ ] Debug panel shows error with status 0
- [ ] UI remains functional

### Restart API

- [ ] Restart API server
- [ ] Try operation again
- [ ] Verify success
- [ ] Error clears

### Network Timeout

- [ ] Simulate slow network (browser DevTools)
- [ ] Submit large data
- [ ] Verify loading state shows
- [ ] Verify eventual completion or timeout

## Debug Panel Tests

### Panel Toggle

- [ ] Click panel header to collapse
- [ ] Verify panel hides
- [ ] Click again to expand
- [ ] Verify panel shows

### API Call Logging

- [ ] Verify all API calls appear
- [ ] Calls show: method, endpoint, status, duration
- [ ] Timestamp is accurate
- [ ] Color coding correct:
  - Green: 2xx success
  - Yellow: 4xx client error
  - Red: 5xx server error or network failure

### Expand Details

- [ ] Click on an API call
- [ ] Verify request body shows (if POST)
- [ ] Verify response body shows
- [ ] JSON is formatted correctly
- [ ] Click again to collapse

### Copy Functionality

- [ ] Click "Copy" on individual call
- [ ] Verify clipboard has JSON
- [ ] Click "Copy All"
- [ ] Verify all calls copied
- [ ] Format is valid JSON

### Clear Log

- [ ] Click "Clear" button
- [ ] Verify all calls removed
- [ ] Count shows: 0 calls
- [ ] Panel empty state appears

## UI/UX Tests

### Responsive Design

- [ ] Resize browser to mobile width
- [ ] Verify layout adapts
- [ ] All components accessible
- [ ] No horizontal scroll

### Loading States

- [ ] Verify spinner during API calls
- [ ] Buttons show "Loading..." text
- [ ] Disabled state on buttons
- [ ] Form inputs disabled during submission

### Form Behavior

- [ ] Form clears after successful submit
- [ ] Byte counter resets
- [ ] Error clears on new input
- [ ] Source dropdown works
- [ ] Textarea resizable

### Persona Display

- [ ] JSON syntax highlighting (dark bg)
- [ ] Scrollable for long personas
- [ ] Metadata grid displays correctly
- [ ] Refresh button works
- [ ] Copy JSON button works

## Performance Tests

### Large Data Handling

- [ ] Submit 50,000 bytes of text
- [ ] Verify performance acceptable (<5s)
- [ ] No UI freezing
- [ ] Persona generates successfully

### Multiple Operations

- [ ] Create 5 persons rapidly
- [ ] Verify all appear in dropdown
- [ ] Switch between persons
- [ ] Verify correct data loads each time
- [ ] No memory leaks visible

### API Call Volume

- [ ] Perform 10+ operations
- [ ] Debug panel handles many calls
- [ ] Scrolling works smoothly
- [ ] No performance degradation

## Accessibility Tests

### Keyboard Navigation

- [ ] Tab through all form elements
- [ ] Tab order is logical
- [ ] Enter submits form
- [ ] Escape clears error (optional)

### Screen Reader

- [ ] Labels present on all inputs
- [ ] Error messages announced
- [ ] Button states clear
- [ ] Form structure semantic

### Color Contrast

- [ ] Text readable on all backgrounds
- [ ] Error messages visible
- [ ] Status colors distinguishable
- [ ] Dark mode considerations (optional)

## Browser Compatibility

### Chrome/Edge

- [ ] All features work
- [ ] No console errors
- [ ] Performance good

### Firefox

- [ ] All features work
- [ ] No console errors
- [ ] Performance acceptable

### Safari (if available)

- [ ] All features work
- [ ] No console errors
- [ ] Performance acceptable

## Final Verification

- [ ] All user flows completed successfully
- [ ] No unhandled errors in console
- [ ] Debug panel shows all operations
- [ ] API integration working correctly
- [ ] Input sanitization working
- [ ] Validation working
- [ ] Error handling working
- [ ] UI responsive and polished

## Known Issues / Notes

[Document any issues found during testing here]

---

**Test Date**: _____________
**Tester**: _____________
**Environment**: Development / Production
**Browser**: _____________
**OS**: _____________
**Result**: Pass / Fail / Partial

**Notes**:
