# Theme System

## Purpose

The theme system separates three concerns:

- Light/dark mode
- Accent color
- Workspace background tone

These layers must work together without hard-coded product colors or one-off surfaces.

## Light/Dark Mode

Light/dark mode controls the base contrast model:

- Text contrast
- Surface depth
- Border strength
- Shadow strength
- Field backgrounds
- Popover and modal layering

Mode state is stored separately from background tone so users can keep different background presets for light and dark workspaces.

## Accent Color

Accent color controls:

- Widget and panel emphasis
- Active pills and selected states
- Hover glow
- Context indicators
- Primary command buttons

Accent color must flow through tokens such as `--blue`, `--panel-accent`, `--panel-accent-rgb`, and `--panel-accent-text`. Do not hard-code the current blue in new components.

## Background Tone

Background tone controls the ambient workspace background only. It should not overpower widgets, panels, forms, or popovers.

Rules:

- Background tone must preserve readability.
- Glass surfaces must still float clearly above the page.
- Background tone must not change widget accent color.
- Background tone must not introduce decorative wallpaper or loud saturation.
- Light and dark mode each keep their own selected tone.

## Surface Tokens

Use these tokens before adding new values:

- `--bg`
- `--bg-end`
- `--surface`
- `--surface-raised`
- `--surface-soft`
- `--glass-surface`
- `--glass-surface-strong`
- `--glass-border`
- `--glass-highlight`
- `--field-bg`
- `--field-border`
- `--shadow-glass`
- `--shadow-control`

## Component Rules

- Top bars, settings sections, menus, popovers, dialogs, and save bars should use glass surface tokens.
- Inputs should use field tokens, not raw white or raw dark backgrounds.
- Hover and focus states should use accent color mixed with the surface token.
- Shadows should follow `--shadow-glass` for containers and `--shadow-control` for controls.
- Radius should follow the existing rhythm: large surfaces use `--radius-lg`, compact controls use pill or 14px-18px rounded geometry.

## Workspace Toolbar

The toolbar uses all three theme layers:

- Accent color: primary commands, active modes, hover glow, accent marker.
- Background tone: ambient page atmosphere only.
- Light/dark mode: contrast, shadow strength, and glass surface density.

Workspace chrome should use one shared glass layer with ghosted controls rather than repeated bordered command islands. Active modes, hover glow, and the compact create affordance may use `--blue`, but only through token-based gradients or color mixes.

Background tone controls belong with appearance/environment actions, not layout or composition actions.

## Implementation Notes

- Initial theme and background attributes are applied in `base.html` before CSS loads.
- Runtime changes are handled in `app.js`.
- CSS should read from `html[data-theme]` and `html[data-background]`.
- Background preset names are documented in `docs/background-presets.md`.
