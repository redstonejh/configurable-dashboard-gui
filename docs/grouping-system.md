# Grouping System

## Philosophy

Grouping behaves like multi-selection in a professional creative tool. It is a shared transform state over individual dashboard objects, not a merged container and not a rigid layout block.

Grouped items remain individually configurable, pinnable, resizable, recolorable, and deletable.

## Selection

- The Select toolbar control enters multi-selection mode.
- Clicking widgets or panels toggles their selected state.
- Selected items receive subtle glass-native selection feedback.
- Selection can include mixed object types: widgets, panels, command surfaces, tables, graphs, and future context panels.

## Movement

Dragging any selected movable item moves the selected movable set.

Rules:

- Relative grid offsets are preserved.
- Sparse empty space inside the selected set is preserved.
- Movement snaps to grid cells.
- External occupancy is respected.
- During active drag, selected members use live visual surfaces that keep exact pixel spacing while one composite footprint reserves the snapped grid area.
- Active drag and resize use the shared group boundary visual treatment so the selected outline does not shrink, darken, or change radius when interaction starts.
- Pinned selected items do not move and remain hard reservations.
- If the requested move collides with pinned or external objects, surrounding movable items resolve after the composite footprint so the group reads as one spatial object.

## Resize

Group resize is proportional and density-aware.

Rules:

- Do not force all selected items to the same size.
- Each item scales from the shared group bounds.
- Member row/top offsets inside the group remain stable so stacked panels do not fan apart while the composite footprint changes size.
- Each item clamps to its own minimum valid size.
- A single composite resized footprint drives collision and surrounding reflow; member previews are visual only and do not independently displace neighbors.
- The most constrained item defines the minimum shrink threshold.
- Widget type, panel content needs, command-surface minimums, and future graph/table density requirements must be respected.
- Resize math must not depend on which selected object has focus or which menu is open.

## Pinned Items

Pinned items inside a selection remain selected but do not move. They reserve their grid cells and can prevent or redirect a group transform.

## Persistence

Grouping is currently a temporary multi-selection transform state. Layout results from group transforms are persisted through the normal layout save system.

Future persistent logical groups should store group membership separately from grid placement.

## Testing

Regression coverage should include:

- Mixed panel/widget multi-selection.
- Group drag preserving relative spacing.
- Group drag around pinned selected items.
- Group resize with different minimum sizes.
- Sparse gaps preserved after group transforms.
- Save/load after group transforms.
