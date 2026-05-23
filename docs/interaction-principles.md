# Interaction Principles

## Direct Manipulation First

Dashboard objects should be edited through spatial interaction whenever possible. Dragging, resizing, selecting, pinning, grouping, and context attachment should feel tactile and immediate.

## Shared Transform Model

Multi-selection creates a temporary transform boundary around independent objects.

- The boundary coordinates movement and resize.
- Objects keep their own identity, config, menu, size limits, and visual style.
- Transform previews must be reversible until commit.
- Final commit should write exact grid coordinates and sizes.

## Motion And Polish

- Use existing grid motion timing and easing.
- Avoid teleporting, jitter, flicker, and focus/menu leaks.
- Preserve pixel alignment during drag and resize.
- Ghost previews must match final drop positions.
- Hover-only controls should not respond under active drags or resizes.

## Occupancy

- Widgets and panels share one occupancy system.
- Pinned items are hard reservations.
- Sparse gaps are valid and should not be collapsed unless the user requests a reset or pack action.

## Resize Limits

Every object type owns its minimum viable size. Resizing must preserve visible controls and usable content.

For grouped resize, the group can shrink only until the most constrained selected object reaches its minimum valid size.

## Implementation Rule

Complex interaction changes should follow:

1. Reproduce.
2. Isolate state and geometry.
3. Add a regression test.
4. Apply the smallest deterministic fix.
5. Re-run interaction and visual tests.
