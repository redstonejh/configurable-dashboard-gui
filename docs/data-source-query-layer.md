# Data Source And Query Layer

## Purpose

The long-term data layer should let the dashboard consume structured data from many sources and let widgets derive, transform, filter, and visualize that data without hard-coded domain logic.

This system must stay generic. It must not assume alerts, security events, business metrics, fixed schemas, or specific field names.

## Supported Source Direction

The platform should eventually support configurable sources such as:

- REST APIs
- GraphQL APIs
- SQL databases
- SQLite
- PostgreSQL
- MySQL
- CSV and JSON uploads
- Local files
- Webhooks
- Internal adapters and connectors
- Streaming or live sources

Each source should be represented abstractly through neutral adapter metadata, not source-specific widget code.

## Core Concepts

- `DataSource`: Connection definition and adapter type.
- `Dataset`: Named table, endpoint, file, query result, or stream topic exposed by a source.
- `QueryDefinition`: Neutral query/request description for a dataset.
- `FieldMap`: Visual mapping from source fields to widget roles.
- `TransformStep`: Sort, filter, derive, normalize, group, or reshape operation.
- `Aggregation`: Count, sum, average, min, max, distinct count, ratio, trend, or custom computed metric.
- `ComputedField`: Derived value based on fields, formulas, or aggregate expressions.
- `DataBinding`: Widget-level connection from source/query output to display roles.
- `QueryResult`: Normalized rows, columns, metadata, errors, and timing information.

## Adapter Rules

- Adapters normalize source access into a common query/result shape.
- Adapters must not leak domain concepts into widget rendering.
- Adapters own connection details, auth details, pagination, request shape, and raw source quirks.
- Widgets should consume normalized `QueryResult` objects.
- Source-specific credentials and secrets must never be exposed to browser code.
- Connector errors should be visible in a generic, user-safe way.

## Widget Data Binding

When configuring a widget, users should be able to:

- Choose a data source.
- Choose a dataset or query.
- Map fields visually.
- Define filters.
- Define transformations.
- Define aggregations.
- Define display formatting.

### Stat Binding

Stat widgets should support:

- Total count
- Average
- Sum
- Max/min
- Distinct count
- Calculated metric
- Optional context emission when clicked

### Graph Binding

Graph widgets should support:

- X-axis field
- Y-axis field
- Aggregation method
- Grouping
- Timeframe
- Stacked or split series
- Context-driven filtering

### Table Binding

Table widgets should support:

- Selected columns
- Sorting
- Filtering
- Grouping
- Pagination
- Conditional formatting

## Computed Values And Formulas

Widgets should eventually support computed expressions.

Users should be able to:

- Reference fields.
- Perform math.
- Perform aggregation.
- Derive calculated values.
- Transform or filter data.

Example expressions:

```text
count(status == "red")
sum(revenue)
avg(duration)
success / total * 100
WHERE category = "critical"
```

Long-term expression options:

- SQL-like expressions
- Formula language
- Lightweight computed fields
- Aggregation pipelines

Formula execution must be sandboxed, deterministic, and testable. Avoid evaluating arbitrary JavaScript from user input.

## Stat + Tracker Behavior

Stat widgets can become interactive context emitters.

Example:

- `5 Critical`
- `12 Warning`
- `42 Healthy`

When clicked:

- The stat emits a generic context/filter.
- Connected tables, graphs, calendars, and panels react.
- Downstream widgets inherit that context through panel scope or explicit links.

This creates tactile data exploration without forcing users into forms.

## Visual Query Philosophy

The dashboard should not become:

- A giant SQL editor
- A BI configuration maze
- A form-heavy dashboard builder

Prioritize:

- Direct manipulation
- Contextual composition
- Visual configuration
- Progressive complexity
- Clean defaults
- Discoverable advanced features

Normal users should be able to click, filter, and explore visually. Advanced users should be able to use formulas, mappings, Engineer Mode context wiring, and custom query expressions.

## Architecture Direction

Potential modules:

- `data-source-registry.js`
- `data-binding-editor.js`
- `query-builder.js`
- `query-engine.js`
- `computed-field-engine.js`
- `transform-pipeline.js`
- `adapter-client.js`
- `query-cache.js`
- `live-update-engine.js`

Backend direction:

- Keep FastAPI endpoints generic.
- Add adapter interfaces server-side.
- Keep secrets and credentials server-side.
- Normalize query results before they reach widgets.
- Use SQLite for local metadata and cached results where appropriate.

## Persistence

Persist:

- Data source definitions, excluding secrets in browser-visible payloads.
- Dataset/query definitions.
- Widget data bindings.
- Field mappings.
- Transform steps.
- Aggregation settings.
- Computed fields.
- Cache policy.
- Live update settings.

Do not persist transient query previews as layout state.

## Implementation Plan

### Phase 2A: Metadata Foundation

- Add neutral model documentation for `DataSource`, `Dataset`, `QueryDefinition`, `DataBinding`, `FieldMap`, `TransformStep`, `Aggregation`, and `ComputedField`.
- Store only placeholder/demo data initially.
- Keep the widget registry independent from concrete adapters.

### Phase 3A: Local Query Engine

- Implement local JSON/table query evaluation for demo data.
- Support stat count/sum/avg/min/max/distinct.
- Support table filtering and sorting.
- Support graph grouping and aggregation.
- Route context filters through the same query path.

### Phase 4A: Visual Binding UI

- Add visual field mapping controls inside existing glass/pill/modal patterns.
- Keep simple presets for normal users.
- Hide formulas and advanced expressions behind progressive disclosure.

### Phase 5A: Adapter Layer

- Add server-side adapter interface.
- Start with SQLite and uploaded CSV/JSON.
- Add REST/GraphQL only after the local query contract is stable.

### Phase 6A: Caching And Live Updates

- Add query caching.
- Add refresh policies.
- Add live/streaming hooks only after static query behavior is stable and tested.

## Testing Requirements

- Data source creation with neutral labels.
- Dataset/query selection.
- Field mapping persistence.
- Stat aggregations.
- Table filtering/sorting.
- Graph grouping.
- Formula validation and safe failure.
- Context-driven query updates.
- Query errors displayed without breaking layout.
- No domain-specific strings in source, bindings, tests, or UI.
