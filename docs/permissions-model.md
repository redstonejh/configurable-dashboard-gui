# Permissions Model

## Purpose

Permissions define who can view, edit, configure, wire, share, or administer dashboard workspaces and objects.

The model should feel elegant and contextual in the UI, but enforcement must happen server-side for every mutation and sensitive read.

## Core Roles

### Admin

Full workspace control:

- Manage workspace settings.
- Manage users and roles.
- Create, edit, move, resize, pin, delete, and configure objects.
- Save, load, restore, and manage layout profiles.
- Use Engineer Mode fully.
- Create, delete, and edit context links.
- Manage data sources.
- Manage permissions.

### Editor

Builder and configuration access:

- Create and edit widgets.
- Move and resize panels and widgets.
- Save layout profiles.
- Configure dashboard objects.
- Use context systems.
- Use Engineer Mode only if granted.

### Viewer

Read-only workspace access:

- View dashboard content.
- Interact with filters, search, timeframe, and context controls if allowed.
- Cannot alter layout, persistence, object config, links, permissions, or data sources.

### Custom Roles

Future configurable roles may define:

- Workspace-scoped permissions.
- Object-level overrides.
- Engineer Mode privileges.
- Data source privileges.
- Sharing privileges.

Custom role behavior must remain deterministic and auditable.

## Permission Vocabulary

Recommended permission keys:

- `workspace:view`
- `workspace:edit`
- `workspace:admin`
- `workspace:share`
- `layout:save`
- `layout:restore`
- `object:create`
- `object:view`
- `object:edit`
- `object:move`
- `object:resize`
- `object:delete`
- `object:configure`
- `context:emit`
- `context:consume`
- `context:attach`
- `engineer:view`
- `engineer:link:create`
- `engineer:link:delete`
- `datasource:view`
- `datasource:manage`
- `permissions:manage`

## Object-Level Permissions

All universal dashboard objects should eventually support permission metadata:

- `ownerId`
- `workspaceId`
- `visibility`
- `editableBy`
- `movableBy`
- `resizableBy`
- `configurableBy`
- `engineerEditableBy`
- `contextAllowedBy`
- `locked`
- `pinned`

Objects include:

- Widgets
- Panels
- Context panels
- Timeframe widgets
- Search widgets
- Graph widgets
- Table widgets
- Calendar widgets
- Engineer Mode links
- Spatial regions

## Workspace-Level Permissions

Workspace membership grants baseline access.

Workspace fields:

- `ownerId`
- `visibility`
- `defaultRole`
- `members`
- `sharedLinks`
- `roleBindings`

Workspace permissions are inherited by objects unless object-level permissions override them.

## Context Permissions

Context propagation can reveal or alter meaningful data views, so it needs permission checks.

Rules:

- A user must be allowed to interact with a context source before emitting context from it.
- A user must be allowed to view a target before context can update its visible data.
- Attaching context to a panel requires `context:attach` on the panel and compatible source permission.
- Engineer Mode links require source and target permission checks.
- Restricted widgets must not leak data through derived stat counts, filtered graphs, or search results.

## Engineer Mode Permissions

Recommended defaults:

- Admin: create, delete, edit, and view links.
- Editor: view links and interact with context; create/delete links only if granted.
- Viewer: optionally view context flow, but cannot rewire.

Unauthorized wiring actions should be visually unavailable and rejected server-side.

## UI Rules

Permissions UI should be:

- Contextual.
- Compact.
- Glass-styled.
- Spatially integrated.
- Clear without being heavy.

Prefer:

- Small access indicators.
- Share capsules.
- Collaborator pills.
- Lightweight object access menus.
- Subtle lock/read-only badges.

Avoid:

- Giant permission matrices as the primary UX.
- Constant modal interruptions.
- Enterprise admin clutter.

## Server-Side Enforcement

Never rely on frontend hiding.

Every mutation must check:

1. Authenticated user.
2. Workspace membership.
3. Role permission.
4. Object-level override.
5. Data source permission if data is involved.

Every sensitive read must check visibility and data access.

## Testing

Permission tests should cover:

- Admin can perform all workspace operations.
- Editor can edit allowed objects but cannot manage users by default.
- Viewer cannot mutate layout or object config.
- Object-level restrictions override workspace role.
- Engineer Mode link creation/deletion is rejected when unauthorized.
- Hidden/restricted widgets do not leak through context, stats, search, or graph aggregation.
- API rejects unauthorized requests even if the UI is manually manipulated.
