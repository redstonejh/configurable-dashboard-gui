# Engineer Mode

## Purpose

Engineer Mode is the advanced visual wiring layer for explicit runtime/dataflow. It lets users connect object outputs to object inputs while preserving the dashboard's polished Apple-glass identity.

Ambient divider/region context remains separate. Context inheritance describes the environment an object belongs to; Engineer wires describe the explicit signal/data path that feeds an object.

Engineer Mode is not a full node editor. It is a minimal, powerful wiring mode inside the dashboard.

## Entry Point

Add an Engineer Mode toggle in the top toolbar.

When enabled:

- Connectable widgets, panels, dividers, and logic nodes expose input/output ports.
- Existing explicit runtime/dataflow links become visible.
- Users can create, select, and delete links.
- Normal dashboard editing still respects pinned, locked, and grid rules.

When disabled:

- Handles and link lines are hidden.
- Links remain active in runtime graph state.
- The dashboard returns to the normal clean composition surface.

## Connection Handles

Handles should be subtle native controls, not large developer-node ports.

Handle types:

- Output port: object can emit data, filter, query, logical, style, semantic, or future signal values.
- Input port: object can consume a runtime signal.
- Context sharing remains a separate semantic Context Link concept, not the default meaning of a wire.

Rules:

- Handles must be theme-aware.
- Handles must align to object edges without shifting layout.
- Handles must not interfere with drag, resize, menu, or pin controls.
- Handles should only appear in Engineer Mode or during a deliberate context wiring gesture.
- Handles should stay small and quiet. They are Engineer affordances, not primary dashboard controls.

## Link Creation

1. User presses a source handle.
2. A soft line follows the pointer.
3. Valid targets show subtle affordance.
4. Dropping on a valid target creates a persisted directional `Link`.
5. Dropping elsewhere cancels without side effects.
6. Link persistence updates after successful creation.
7. Hovering a handle highlights only the committed links connected to that object; unrelated links remain subdued.

Do not rely on arbitrary timers. Pointer state, preview state, and committed link state must be separate.

## Link Rendering

Use a lightweight overlay above the dashboard grid.

Visual rules:

- Smooth lines
- Soft glow
- Theme-aware color
- No hard-coded blue
- No harsh node-editor styling
- No layout shift
- No clipping under panels, popovers, modals, or drag ghosts

Link paths should update after:

- Drag
- Resize
- Collapse/expand
- Window resize
- Layout load/reset
- Panel membership change
- Future canvas pan

Save/load must include committed directional `Link`, semantic `ContextLink`, and relationship graph state. Loading should restore valid links by object id and discard stale links whose source or target objects no longer exist.

- Future canvas zoom
- Future workspace region collapse/expand

## Spatial Workspace Compatibility

Engineer Mode must remain coherent on a future zoomable canvas.

- Link overlays should use canvas/world coordinates, not brittle viewport-only assumptions.
- Handles must stay attached to their source and target under pan and zoom.
- Link glow and stroke weight should remain visually balanced across zoom levels.
- Overview zoom may simplify links, but must not hide active dataflow in a misleading way.
- Panning and zooming must not mutate `Link` or `ContextLink` state.
- Selecting or deleting links must work at supported zoom levels.

## Link Selection And Deletion

- Clicking a link selects it.
- Selected link uses subtle emphasis.
- Delete action removes the selected runtime link from the graph.
- Deleting a widget or panel removes related links.
- Link deletion must persist.

## Persistence

Persist directional links with layout/profile data:

- `id`
- `source` output port
- `target` input port
- `signalType`
- `direction`
- `enabled`
- Optional visual route metadata only if needed

Do not persist transient pointer preview data.

Context Links continue to persist separately as semantic context-sharing records. Default Engineer wire drags should not create Context Links; dedicated context-link tooling may do so when the user explicitly wants shared or inherited context across physical regions.

## Implementation Plan

### Phase 4: Minimal Engineer Mode

- Add `engineer-mode.js`.
- Add top toolbar toggle.
- Add input/output port rendering based on object capabilities.
- Add directional dataflow link creation gesture.
- Add `link-renderer.js` overlay.
- Persist `Link` records.
- Keep semantic `ContextLink` records separate for explicit context-sharing tools.

### Phase 4: Link Behavior

- Feed runtime links into future dataflow/query/computation evaluation.
- Feed Context Links into `context-engine.js`.
- Update link routes after layout changes.
- Support select and delete.

### Phase 6: Tests

- Toggle Engineer Mode on/off.
- Handles show and hide correctly.
- Link creation works.
- Link deletion works.
- Links persist after reload.
- Directional links preserve output-to-input flow.
- Context Links affect downstream context when explicitly created.
- Normal mode hides wiring visuals but keeps links active.
- Future spatial tests cover link routing after pan, zoom, region collapse, drag, resize, and layout load.
