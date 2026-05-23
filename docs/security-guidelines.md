# Security Guidelines

## Purpose

Security must be part of the dashboard platform architecture, not a visual-only layer. The UI can be subtle and elegant, but authorization must be enforced by the backend.

## Non-Negotiables

- Never rely only on frontend hiding for permissions.
- Validate authentication and authorization on every API mutation.
- Validate sensitive reads server-side.
- Hash passwords securely.
- Protect against CSRF.
- Rate-limit authentication and sensitive endpoints.
- Invalidate sessions on logout and credential rotation.
- Keep secrets out of browser-visible payloads.
- Use HTTPS in production.
- Keep auditability in mind for future multi-user work.

## Secure API Architecture

Every request should flow through:

1. Authentication middleware.
2. Session/token validation.
3. Workspace membership lookup.
4. Role and permission check.
5. Object-level permission check where applicable.
6. Data source permission check where applicable.
7. Handler execution.
8. Audit/event logging for sensitive mutations.

Do not duplicate permission checks casually in scattered handlers. Centralize permission evaluation behind a small service/module.

## Session Security

Rules:

- Use `HttpOnly` cookies for browser sessions where practical.
- Use `Secure` cookies in production.
- Use `SameSite=Lax` or stricter unless a provider flow requires otherwise.
- Rotate refresh tokens.
- Revoke tokens on logout.
- Expire inactive sessions.
- Handle expired sessions without corrupting unsaved workspace state.

## CSRF Protection

Required for cookie-authenticated mutations:

- CSRF token on unsafe methods.
- SameSite cookie configuration.
- Origin/referer checks where useful.
- Explicit tests for rejected missing/invalid CSRF tokens.

## Password And Account Security

Use:

- Argon2id or bcrypt.
- Unique salts.
- Secure reset tokens.
- Login rate limits.
- Generic auth failure messages.
- Account lockout or progressive throttling.

Never:

- Store plaintext passwords.
- Log passwords or reset tokens.
- Return account-existence hints in auth errors.

## OAuth / SSO Security

Rules:

- Validate state.
- Use PKCE where supported.
- Keep provider secrets server-side.
- Strictly allowlist redirect URIs.
- Validate provider issuer and audience.
- Define account linking behavior.
- Store provider tokens only when needed, and encrypt at rest.

## Authorization

Authorization must check:

- User identity.
- Workspace membership.
- Role permission.
- Object-level permission.
- Data source permission.
- Engineer Mode permission for link operations.

Examples:

- Viewer cannot call layout save API.
- Editor cannot manage users by default.
- User without object access cannot read hidden widget config.
- Unauthorized Engineer Mode link creation returns `403`.

## Data Source Security

Future data connectors must protect:

- Credentials.
- API keys.
- OAuth provider tokens.
- Database connection strings.
- Query results with restricted fields.

Rules:

- Secrets are never sent to the browser.
- Query execution runs server-side or in a controlled backend layer.
- Field-level restrictions are enforced before data reaches widgets.
- Context filters must not leak counts or derived results from restricted data.

## Audit And History

Future audit events should include:

- Login/logout.
- Failed login attempts.
- Workspace role changes.
- Permission changes.
- Data source changes.
- Layout restore/save.
- Engineer Mode link creation/deletion.
- Sharing and invite changes.

Audit UI should be optional and polished, not a default clutter layer.

## Visual Security UX

Security UI should match the workspace:

- Glass surfaces.
- Compact controls.
- Theme-aware role pills.
- Subtle lock/access indicators.
- Clean sharing surfaces.
- Soft transitions and clear affordance.

Avoid:

- Generic admin styling.
- Heavy permission forms as primary flow.
- Constant warning modals.

## Testing

Security tests should include:

- Unauthenticated requests return `401`.
- Authenticated but unauthorized requests return `403`.
- Mutations reject missing/invalid CSRF tokens.
- Session expiration is handled cleanly.
- Logout invalidates session.
- Role changes affect future mutations.
- Frontend-hidden controls are not the only defense.
- Restricted data does not leak through widgets, formulas, stats, search, graphs, context, or API payloads.
