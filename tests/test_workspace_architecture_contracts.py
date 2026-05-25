from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
WIDGET_REGISTRY_JS = (ROOT / "app" / "static" / "widget-registry.js").read_text(encoding="utf-8")
ARCHITECTURE_DOC = (ROOT / "docs" / "WORKSPACE_ARCHITECTURE.md").read_text(encoding="utf-8")


def test_workspace_taxonomy_and_layout_domains_are_documented():
    for heading in (
        "Workspace Object Taxonomy",
        "Layout Domains",
        "Widget Runtime Contract",
        "Context Inheritance Backbone",
        "Save/Load And History Ownership",
    ):
        assert heading in ARCHITECTURE_DOC

    for object_name in (
        "Widget",
        "Panel",
        "Divider",
        "Anchor",
        "Context Region",
        "Panel Child Widget",
    ):
        assert object_name in ARCHITECTURE_DOC

    for domain_name in (
        "Global Workspace Grid",
        "Panel Internal Grid",
        "Anchor Rail",
        "Divider Regions",
    ):
        assert domain_name in ARCHITECTURE_DOC


def test_workspace_object_capabilities_keep_collision_domains_explicit():
    assert "const WORKSPACE_OBJECT_TYPES = Object.freeze" in APP_JS

    for object_type in ('widget: "widget"', 'panel: "panel"', 'divider: "divider"', 'anchor: "anchor"'):
        assert object_type in APP_JS

    for capability in (
        "participatesInGridCollision",
        "hasPanelContentArea",
        "usesAnchorLayer",
        "usesDividerSurface",
    ):
        assert capability in APP_JS

    anchor_capabilities = APP_JS[
        APP_JS.index("[WORKSPACE_OBJECT_TYPES.anchor]"):
        APP_JS.index("WORKSPACE_CONTEXT_MODEL_VERSION")
    ]
    assert "participatesInGridCollision: false" in anchor_capabilities
    assert "usesAnchorLayer: true" in anchor_capabilities


def test_context_engine_exposes_foundational_inheritance_helpers():
    for helper_name in (
        "deriveContextRegions",
        "resolveRegionForY",
        "getNearestDividerAbove",
        "resolveObjectContext",
        "mergeContext",
        "queryContext",
        "queryWidget",
    ):
        assert helper_name in APP_JS

    for implementation_name in (
        "deriveWorkspaceContextRegions",
        "resolveWorkspaceRegionForY",
        "nearestDividerAboveCommittedRow",
        "resolveWorkspaceContextForItem",
        "mergeWorkspaceContexts",
    ):
        assert implementation_name in APP_JS


def test_widget_runtime_registry_contract_covers_first_class_widgets():
    for registry_api in (
        "registerWidgetDefinition",
        "getWidgetDefinition",
        "createWidgetInstance",
        "renderWidget",
        "listWidgetDefinitions",
    ):
        assert registry_api in WIDGET_REGISTRY_JS

    for widget_type in (
        'type: "stat"',
        'type: "timeframe"',
        'type: "search"',
        'type: "table"',
        'type: "chart"',
    ):
        assert widget_type in WIDGET_REGISTRY_JS

    assert "unsupportedDefinition" in WIDGET_REGISTRY_JS
    assert "Unsupported widget" in WIDGET_REGISTRY_JS
    assert "resolveQuery" in WIDGET_REGISTRY_JS
    assert "capabilities" in WIDGET_REGISTRY_JS


def test_persistence_and_history_paths_include_architecture_state():
    for persistence_path in (
        "saveWidgetLayouts",
        "savePanelLayouts",
        "saveFloatingAnchors",
        "saveWorkspaceContexts",
        "saveDataSources",
    ):
        assert persistence_path in APP_JS

    for history_path in (
        "pushLiveLayoutUndo",
        "captureLayoutUndo",
        "captureLiveLayoutState",
        "restoreLiveLayoutSnapshot",
    ):
        assert history_path in APP_JS

    assert "restorePanelChildWidgets" in APP_JS
    assert "childWidgets" in APP_JS
