# Background Presets

## Purpose

Background presets provide subtle workspace atmosphere while preserving contrast, readability, glass depth, and dashboard focus.

They are not wallpapers and should not become decorative theme chaos.

## Light Presets

- `warm-white`: A warm neutral workspace tone.
- `cool-white`: A cooler white workspace tone.
- `soft-grey`: A quiet neutral grey.
- `light-blue-grey`: A restrained blue-grey.
- `blue-mist`: A subtle blue mist.
- `frosted-light`: The default light frosted neutral.

## Dark Presets

- `charcoal`: The default dark charcoal.
- `graphite`: A slightly lifted graphite tone.
- `soft-black`: A deeper low-light tone.
- `deep-navy`: A restrained navy atmosphere.
- `dark-blue-grey`: A dark blue-grey neutral.
- `midnight-blue`: A deeper blue workspace.
- `dark-frosted`: A dark frosted neutral.

## Rules

- Presets must update `--bg`, `--bg-end`, and any necessary supporting surface tone.
- Presets must not override accent color.
- Presets must not reduce text contrast.
- Presets must not flatten glass surfaces.
- Presets must not require component-specific overrides.
- New presets require visual checks on dashboard, settings, forms, popovers, and modals.

## Toolbar Integration

Background selection is an appearance/environment action in the workspace toolbar.

- The background tone control should live with theme mode and settings.
- Changing background tone should not change active accent color.
- Command islands must remain legible and elevated above every background preset.
- Toolbar screenshots should cover at least one light preset and one dark preset.

## Testing

Visual checks should include:

- Dashboard in light mode with at least two backgrounds.
- Dashboard in dark mode with at least two backgrounds.
- Settings page with form fields.
- Dropdowns and popovers.
- Dialogs or modal-like surfaces.
- Multiple accent colors combined with multiple backgrounds.
