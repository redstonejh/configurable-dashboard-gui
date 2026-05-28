# Dashboard Testing Methodology

This document defines testing strategy by bug class. Each section maps to a category of regressions
we have experienced, with test tier, likely file locations, and automation guidance.

---

## Bug Class 1 — Widget Chrome / Layout Cleanup

**What to test manually**
- No redundant title+subtitle pair visible on stock widgets
- No "Last 30 days" or equivalent footer text in widget body
- No phantom header or footer spacing gaps
- Content-well borders are equal and minimal (no asymmetric padding)

**Automated regression**
- Architecture contract: verify `widgetTitle`, `widgetSubtitle`, `widgetFooter` CSS classes do not
  produce double-rendered text in the DOM when a widget is created via the registry
- Playwright smoke: after adding a stat widget and a chart widget, assert
  `widget-card .widget-footer-text` is absent or empty

**Likely file areas**
- `app/static/widget-registry.js` — widget render templates
- `app/static/dashboard-grid.css` — `.widget-card`, `.widget-body`, `.widget-header` sizing
- `app/static/themes.css` — per-widget chrome variables

**Test tier:** Smoke + regression archive for confirmed regressions

---

## Bug Class 2 — Customization / Menu Behavior

**What to test manually**
- Right-click on a widget opens customization menu near pointer position
- Double-click customization is fully absent (no event, no menu)
- Left-click config menus open at/above the clicked object, not at page origin
- No secondary "appearance/config form" window appears alongside menus
- Menus use `.global-overlay` / portal layer, never Z-fighting with widget chrome
- After closing, menus do not intercept pointer events (click-through check)

**Automated regression**
- Playwright: right-click widget → `expect(page.locator(".customization-menu"))` to be visible within
  reasonable offset of click coordinates
- Playwright: assert `.global-overlay` or top-layer portal is parent of open menu
- Playwright: after menu close, click outside area → assert menu locator count = 0 and subsequent
  widget interaction succeeds

**Likely file areas**
- `app/static/app.js` — right-click handler, `showCustomizationMenu`
- `app/static/menu-overlay.js` — portal/overlay positioning
- `app/static/dashboard-grid.css` — z-index layers

**Test tier:** Feature-local (customization path); regression archive for pointer-capture escapes

---

## Bug Class 3 — Object-Specific Customization

**What to test manually**
- **Anchors**: each menu button (rename, delete, change link target) actually fires its action
- **Dividers**: right-click context menu is accessible; left-click does not open config
- **Time Panel**: customization menu opens and "Delete" removes the widget
- **Stat widgets**: right-click opens customization, options are actionable
- **Normal widgets/panels**: customization menu still works after all of the above changes

**Automated regression**
- Playwright: for each object type add one instance, right-click, assert menu appears
- Playwright: for anchor — click "Delete" button in menu, assert anchor count decreases
- Playwright: for divider — left-click, assert no menu; right-click, assert menu

**Likely file areas**
- `app/static/app.js` — per-object context menu logic, `WORKSPACE_OBJECT_TYPES`
- `app/static/widget-registry.js` — stat/timeframe widget event handlers

**Test tier:** Feature-local per object type; smoke for "customization opens" on each type

---

## Bug Class 4 — Stat Widget Click Safety

**What to test manually**
- Left-click on a stat widget value does NOT mutate global filter or context state
- After clicking a stat widget, other widgets still render correctly (no blank/error states)
- Console has no uncaught errors after stat click
- Error suppression (`window.onerror = null` style hacks) is absent

**Automated regression**
- Playwright: add stat widget, left-click it, then assert `page.console_errors == []` and all other
  widgets remain visible
- Architecture contract: `assert "window.onerror = null" not in APP_JS` and
  `assert "console.error = " not in APP_JS`

**Likely file areas**
- `app/static/widget-registry.js` — stat widget click handler
- `app/static/app.js` — global context mutation entry points

**Test tier:** Regression archive (confirmed incident); architecture contract for suppression check

---

## Bug Class 5 — Anchor Rail Behavior

**What to test manually**
- Anchors render as compact rail objects, not grid-positioned widgets
- Add anchor, delete it, add another → no forced layout gap remains
- During drag, ghost preview visually tracks pointer (no teleport / offset drift)
- Placeholder position and final committed position agree
- Drop commit normalizes to a compact ordered stack (no stale absolute row offsets)

**Automated regression**
- Playwright: add anchor, assert it is inside `.workspace-anchor-layer` not `.widget-layout`
- Playwright: add anchor, delete, add another, assert anchor rail has no unexpected top margin
- Playwright: drag anchor, assert placeholder follows pointer within ±32 px
- Architecture contract: `assert "usesAnchorLayer: true" in APP_JS`

**Likely file areas**
- `app/static/app.js` — `saveFloatingAnchors`, anchor drag handlers
- `app/static/dashboard-grid.css` — `.workspace-anchor-layer`, `.workspace-anchor-object`

**Test tier:** Feature-local drag tests (currently exist in e2e suite); architecture contract for layer

---

## Bug Class 6 — Panel Containment / Context

**What to test manually**
- Widgets dragged into an open panel inherit panel's ambient context (date range, filters)
- After drag into panel, widget still shows data (context not dropped)
- Dragging into a collapsed panel does nothing (no absorption)
- Panel-contained widget customization menus render above panel chrome, not clipped

**Automated regression**
- Playwright: exists — `test_panel_context_is_additional_widget_inheritance_layer`
- Playwright: exists — `test_widget_hover_over_collapsed_panel_does_not_absorb`
- Playwright: exists — `test_widget_drags_directly_into_open_panel_and_round_trips`
- Gap: no test for menu z-ordering above panel chrome; add visual/manual check

**Likely file areas**
- `app/static/app.js` — `resolveWorkspaceContextForItem`, panel drag entry
- `app/static/panel-containment.js` — containment detection

**Test tier:** Feature-local (strong existing coverage); manual for menu z-ordering

---

## Bug Class 7 — Expand / Collapse Layout

**What to test manually**
- Opening a panel pushes widgets below it downward without scrambling other columns
- Collapsing restores the original positions below the panel
- Temporary displacement does not persist after collapse
- Save with open panel, reload → correct layout (panel open, widgets in right positions)
- Save with closed panel, reload → correct layout

**Automated regression**
- Playwright: exists — `test_adding_many_panels_appends_without_global_layout_scramble`
- Gap: no dedicated save/load with open panel test; add regression test

**Likely file areas**
- `app/static/app.js` — `expandPanelLayout`, `collapsePanelLayout`, `saveWidgetLayouts`

**Test tier:** Feature-local; regression archive for save/load determinism

---

## Bug Class 8 — Drag / Resize Interaction Laws

**What to test manually**
- Live ghost follows pointer throughout drag (no jump at pickup)
- Snapped preview position matches final committed position
- Resize uses live clone/source separation (source stays, clone resizes live)
- Minimum-size widgets commit at minimum, not smaller
- After any drag/resize, all DOM classes (`.dashboard-live-resize`, `.dashboard-resize-preview`,
  `.dashboard-resize-source`, `.dashboard-active-resize`) are cleaned up
- `body.panel-resize-active`, `body.panel-interaction-active` are false after interaction ends

**Automated regression**
- `assert_no_resize_artifacts` and `assert_no_undo_artifacts` helpers exist — used in many tests
- `resize_camera_state` helper validates scale/transform cleanup
- Architecture contract: `scheduleWorkspaceVisualLodRefresh` in reflow body (performance contracts)

**Likely file areas**
- `app/static/app.js` — drag FSM, resize handlers
- `app/static/collision-reflow.js` — layout commit paths

**Test tier:** Already well-covered by existing Playwright tests; regression archive for new variants

---

## Bug Class 9 — Background / Material System

**What to test manually**
- Changing background preset updates immediately (no page reload required)
- Adaptive color CSS variables are based on target luminance, not previous-state luminance
- Bright, mid, and dark backgrounds all remain legible (text contrast OK)
- Liquid-glass overlay layers do not intercept clicks on widgets beneath them
- Navbar chrome is not accidentally painted by object-glass rules

**Automated regression**
- Playwright: exists — `test_background_presets_do_not_change_shared_glass_materials`
- Playwright: exists — `test_background_palette_hover_previews_without_saving`
- Gap: no automated luminance-based adaptive variable check; add manual verification step
- Architecture contract: assert `--bg-adaptive-` variables defined in `themes.css`

**Likely file areas**
- `app/static/themes.css` — adaptive variables, glass layers
- `app/static/app.js` — background preset application
- `app/static/menu-overlay.js` — overlay pointer-events

**Test tier:** Smoke (preset applies); visual/manual for luminance adaptation and glass click-through

---

## Bug Class 10 — Navbar / Add Menu Behavior

**What to test manually**
- `+` add menu and layout menu expand smoothly without layout jump
- Nested submenus align horizontally with parent menu top edge (not offset downward)
- After closing any submenu, pointer events pass through to items beneath
- Add menu contents are accessible and not clipped by viewport edge

**Automated regression**
- Playwright: exists — `test_add_object_menu_uses_categorized_right_expanding_submenus`
- Playwright: exists — `test_add_object_menu_hugs_content_and_scrolls_when_viewport_constrained`
- Playwright: exists — `test_nav_dropdowns_use_floating_glass_menu_system_without_restyling_object_settings`

**Likely file areas**
- `app/static/app.js` — navbar menu open/close handlers
- `app/static/menu-overlay.js` — submenu positioning

**Test tier:** Feature-local (existing good coverage); manual for submenu horizontal alignment pixel-check

---

## Bug Class 11 — Object Deletion / Persistence

**What to test manually**
- Widget delete (via customization menu) removes from DOM and does not reappear on reload
- Panel delete extracts child widgets to workspace (not lost)
- Anchor delete removes from anchor rail and persists
- Divider delete removes region and context divider persists on reload as absent
- Time Panel delete works through customization menu path
- `saveWidgetLayouts`, `savePanelLayouts`, `saveFloatingAnchors`, `saveWorkspaceContexts` all
  called after deletion

**Automated regression**
- Playwright: exists — `test_deleting_panel_extracts_child_widgets_and_undo_restores_containment`
- Playwright: exists — `test_deleting_panel_child_widget_clears_interaction_lock`
- Gap: no test for anchor delete + reload; no test for divider delete + reload
- Architecture contract: all four `save*` functions present in `APP_JS`

**Likely file areas**
- `app/static/app.js` — delete handlers per object type
- `app/static/widget-registry.js` — widget-level delete dispatch

**Test tier:** Feature-local for panel/widget; regression archive gaps for anchor/divider persistence

---

## Test Tier Legend

| Tier | Description |
|------|-------------|
| **Smoke** | Must pass on every run; covers "can the page load and can core objects be created" |
| **Feature-local** | Covers one feature area end-to-end; fails should be diagnosed in that area |
| **Regression archive** | Test written specifically because a bug occurred; must never be deleted |
| **Architecture contract** | Fast static string-search over source files; no browser needed |
| **Visual/manual** | Cannot be reliably automated; requires human inspection; call out in PR description |

## Manual-Only Verification Checklist

These items cannot be judged by automated tests and require human eyes:

- [ ] Submenu horizontal alignment to parent top edge
- [ ] Luminance-adaptive CSS variable correctness on bright/dark backgrounds
- [ ] Liquid-glass layer click-through on all themes
- [ ] Drag ghost visual tracking smoothness (frame-by-frame feel)
- [ ] Menu pointer-events after close (click-through on exact close frame)
- [ ] Anchor drag preview offset alignment
- [ ] Widget chrome visual regression (title/subtitle/footer spacing)
