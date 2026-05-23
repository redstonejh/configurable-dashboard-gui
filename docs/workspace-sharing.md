# Workspace Sharing

## Purpose

Workspace sharing turns dashboards into collaborative spatial operating environments. Sharing should feel lightweight, contextual, and polished, while preserving strict server-side access control.

## Workspace Types

Future workspace types:

- Personal workspace.
- Shared workspace.
- Team workspace.
- Organization workspace.

A workspace is more than a saved dashboard. It owns:

- Layout profiles.
- Spatial placement.
- Widget and panel configuration.
- Context scopes.
- Engineer Mode links.
- Theme and background settings.
- Members and roles.
- Sharing and permission settings.

## Ownership

Each workspace should have:

- One owner or ownership group.
- Membership records.
- Role bindings.
- Optional transfer ownership behavior.
- Optional archived/deleted state.

Ownership grants administrative control unless restricted by an organization policy later.

## Collaboration Model

Recommended models:

- Invite by email or identity.
- Assign role at invite time.
- Accept invitation into workspace membership.
- Remove or downgrade collaborators.
- Optional shared link for viewer access later.

Membership fields:

- `workspaceId`
- `userId`
- `role`
- `status`
- `invitedBy`
- `joinedAt`
- `expiresAt`

## Sharing Targets

Potential sharing scopes:

- Entire workspace.
- Layout profile.
- Panel.
- Context scope.
- Individual widget.
- Spatial region.

Initial implementation should prioritize whole-workspace sharing. Object-level sharing can follow once object permissions are stable.

## Sharing UX

Sharing should match the dashboard visual language:

- Floating share capsule.
- Workspace collaborators pill.
- Compact invite surface.
- Theme-aware role picker.
- Subtle access indicators on restricted objects.

Avoid:

- Heavy admin forms.
- Large table-first permission screens as the main experience.
- Modal interruptions for every interaction.

## Role-Aware UI

The UI may reflect permissions:

- Viewer sees read-only layout controls.
- Editor sees create/edit controls.
- Admin sees sharing and permission controls.
- Restricted objects show subtle lock or access indicators.

This is only affordance. The backend must still enforce access.

## Workspace Persistence

Persist:

- Workspace metadata.
- Members and roles.
- Invites.
- Layout profiles.
- Sparse placement.
- Widget config.
- Panel membership.
- Context scopes.
- Engineer Mode links.
- Permissions.
- Theme preset.
- Background preset.
- Workspace atmosphere settings.

Restore must preserve:

- Exact layout state.
- Sparse spatial layout.
- Context relationships.
- Permission state.
- Collaborator membership.
- Theme/background state.

## Collaborative History

Future history systems may include:

- Layout history.
- Workspace history.
- Context-change history.
- Collaborator activity.
- Undo/restore checkpoints.

History should support deterministic restoration without losing spatial continuity.

## Conflict Handling

Future real-time collaboration should define:

- Who can edit an object.
- How simultaneous edits resolve.
- How layout locks or edit presence indicators work.
- How undo behaves with multiple users.

Do not add real-time collaboration until single-user persistence, permissions, and object identity are stable.

## Testing

Sharing tests should cover:

- Invite creation and acceptance.
- Role assignment.
- Role downgrade/upgrade.
- Removed collaborators lose access.
- Workspace owner retains admin control.
- Shared workspace loads exact layout and theme state.
- Viewer cannot mutate shared workspace.
- Editor can mutate allowed workspace objects.
- Permission changes take effect without corrupting active layout state.
