# Authentication System

## Purpose

The authentication system should eventually support secure multi-user access while preserving the dashboard's Apple-glass polish and direct-manipulation feel.

Authentication is a platform layer, not a visual redesign. Login, logout, session renewal, and account settings should feel integrated with the workspace instead of like a detached admin portal.

## Supported Auth Modes

Initial/future supported modes:

- Local username/password accounts.
- OAuth2 providers.
- SSO providers.
- Optional future MFA/2FA.

Potential providers:

- Google
- GitHub
- Microsoft
- Internal auth
- Enterprise SSO later

Provider labels must remain generic in the core architecture. Provider-specific code should live behind adapters.

## Account Model

Recommended neutral model:

- `User`
- `IdentityProvider`
- `UserIdentity`
- `Session`
- `RefreshToken`
- `WorkspaceMembership`
- `Role`

User fields:

- `id`
- `displayName`
- `email`
- `avatarUrl`
- `status`
- `createdAt`
- `lastLoginAt`

Local credential fields must never be exposed to the frontend:

- `passwordHash`
- `passwordUpdatedAt`
- `failedLoginCount`
- `lockedUntil`

## Session And Token Pipeline

Use one of these architectures:

- Secure server-side session cookie.
- Short-lived JWT access token plus secure refresh token.

Rules:

- Cookies must be `HttpOnly`, `Secure` in production, and `SameSite=Lax` or stricter where practical.
- Refresh tokens must be rotatable and revocable.
- Logout must invalidate the active session.
- Expiration must fail closed and redirect/recover cleanly.
- Role and permission changes must refresh without corrupting workspace state.
- "Remember me" may extend refresh lifetime but must not weaken session invalidation.

## Login UX

Login should use the existing visual language:

- Glass surface.
- Compact grouped controls.
- Theme-aware inputs.
- Soft shadow and border rhythm.
- Clear but quiet error states.
- No default browser-looking forms.

Avoid:

- Generic admin login screens.
- Provider button clutter.
- Heavy enterprise banners.
- Modal loops during normal dashboard work.

## Password Security

Local accounts require:

- Strong password hashing using Argon2id or bcrypt with current recommended parameters.
- Unique salt per password.
- No plaintext password storage.
- Rate limiting on login and password reset endpoints.
- Generic error messages that do not reveal account existence.
- Secure password reset tokens with short expiration.

## OAuth / SSO Security

OAuth and SSO flows require:

- State parameter validation.
- PKCE where applicable.
- Strict redirect URI allowlist.
- Provider identity linking rules.
- Server-side token exchange.
- No provider secrets in browser-visible payloads.
- Clear account linking and unlinking behavior.

## API Requirements

- Every API endpoint must receive authenticated identity from trusted session middleware.
- Mutation endpoints must validate role and object permissions server-side.
- Frontend hiding is only visual affordance, never authorization.
- Unauthorized API calls must return consistent `401` or `403` responses.
- Session renewal must not retry destructive mutations automatically without explicit idempotency handling.

## Persistence

Persist:

- User accounts.
- Identity provider links.
- Sessions or refresh tokens.
- Workspace memberships.
- Role assignments.
- Audit metadata needed for security review.

Do not persist:

- Raw OAuth tokens unless explicitly required and encrypted.
- Passwords or reset tokens in plaintext.
- MFA recovery codes without hashing/encryption.

## Future MFA / 2FA

Possible future methods:

- TOTP authenticator app.
- WebAuthn/passkeys.
- Recovery codes.
- Enterprise MFA through SSO.

MFA UI should be calm and integrated, not a separate product experience.

## Testing

Authentication tests should cover:

- Login success and failure.
- Logout invalidation.
- Session expiration.
- Remember-me behavior.
- OAuth state validation.
- Password hashing and reset token expiration.
- CSRF behavior for mutations.
- `401` and `403` API responses.
- No secrets in browser-visible responses.
