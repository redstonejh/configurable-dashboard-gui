# AI Workspace Operator

## Purpose

The AI Workspace Operator is the first architectural layer for an assistant that builds visual analytical workspaces instead of answering only in text.

It is local and deterministic in this version. It does not call an external AI service. The important foundation is the contract:

1. inspect available data and widget capabilities
2. produce a structured, reviewable plan
3. execute only validated workspace actions
4. create registry-backed widgets, panels, calculations, and explanations
5. expose calculation/logic objects in Engineer Mode when needed

## Runtime Files

- `app/static/ai-workspace-operator.js`
  - intent classification
  - schema-aware plan generation
  - what-if scenario planning
  - action execution orchestration
  - AI Assistant widget prompt binding
- `app/static/app.js`
  - exposes `window.dashboardWorkspaceActionRuntime`
  - validates and executes safe workspace actions through existing widget/panel/dataflow systems
- `app/static/widget-registry.js`
  - renders the AI Assistant as an operator surface with Plan and Build actions

## Public Runtimes

`window.dashboardWorkspaceActionRuntime`

- `actionTypes()`
- `validateAction(action)`
- `inspectDatasets(layoutKey, profile)`
- `inspectWidgetRegistry()`
- `nextSafeRow(layoutKey, options)`
- `executeAction(action, options)`
- `executePlan(plan, options)`
- `updateWidgetConfig(widget, patch, options)`

`window.dashboardAiOperatorRuntime`

- `inspectData(layoutKey)`
- `plan(question, options)`
- `executePlan(plan, options)`
- `runPrompt(question, options)`
- `classifyIntent(question)`
- `supportedActions()`

## Safe Action Model

The operator does not mutate random layout internals directly. It emits actions such as:

- `inspectDatasets`
- `inspectSchema`
- `inspectWidgetRegistry`
- `createWidget`
- `createPanel`
- `createFilter`
- `createCalculatedField`
- `createEquationFilter`
- `createChart`
- `createTable`
- `createStat`
- `createMap`
- `createNote`
- `moveObject`
- `resizeObject`
- `createDataflowLink`
- `applyConditionalStyle`
- `createScenario`
- `summarizeWorkspace`
- `explainWidget`
- `explainCalculation`

Execution is routed through `dashboardWorkspaceActionRuntime`, which reuses existing registry, panel, persistence, context, and Engineer Mode systems.

## Planning Contract

Plans are JSON-like records:

```json
{
  "id": "ai-plan-example",
  "version": 1,
  "goal": "What if cost dropped by 12%?",
  "intent": "what-if",
  "status": "ready",
  "requiredData": ["cost", "revenue", "category"],
  "availableData": {
    "datasetId": "demo-source",
    "datasetName": "Demo Source",
    "rowCount": 120
  },
  "assumptions": [],
  "limitations": [],
  "scenario": {
    "destructive": false
  },
  "steps": []
}
```

Statuses:

- `ready`: enough data exists to build the requested workspace
- `partial`: useful visual output is possible, but missing fields or assumptions are visible
- `blocked`: no safe useful workspace can be built

Approval is not implemented yet, but the plan contract is reviewable before execution.

## Data Understanding

Dataset inspection exposes:

- source id/name/kind
- row count
- fields and types
- sample values
- numeric fields
- categorical fields
- time fields
- geospatial fields
- missing-value warnings
- empty-dataset warnings
- sample rows

The planner uses these fields to choose visualizations and to refuse or partially answer unsupported questions. It must not invent unavailable fields.

## Intent Mapping

Current deterministic mappings:

- Executive/overview request: stat cards, trend chart, status mix chart, table, optional map, explanation note
- Trend/change request: line/area trend, summary stat, recent rows table, explanation note
- Ranking/risk/attention request: ranked table, comparison chart, optional map, explanation note
- What-if request: scenario object, calculated fields, projected stat, comparison chart, scenario table, Engineer Mode equation filter, explanation note
- Fallback summary: record count, table, explanation note

## What-If Semantics

Scenarios are derived views. They do not mutate source rows.

The first version supports simple percent adjustments such as:

- cost decreases by 12%
- revenue increases by 5%
- material cost rises by 8%

The operator creates calculated fields in widget config, for example:

- adjusted value
- projected savings
- projected margin

It also creates an Engineer Mode data-filter/equation surface so the logic can be inspected without cluttering normal mode.

## Explanation Widget

The operator uses the existing Text / Notes widget as the explanation surface. The note records:

- the user question
- the answer approach
- assumptions
- limitations
- suggested next inspection steps

This keeps AI-created dashboards explainable and persistence-safe.

## Guardrails

The operator must:

- avoid unsupported widget types
- avoid unavailable fields
- mark assumptions clearly
- mark missing-data limitations clearly
- avoid destructive what-if edits
- keep calculations in widget config or explicit Engineer Mode objects
- avoid hidden persistent state
- keep normal mode calm and uncluttered
- reveal backend/equation objects only through Engineer Mode
- avoid claiming causation from correlation

## Current Limits

This version is a local deterministic operator, not an external model integration. It can classify common analytical prompt patterns and build real workspaces from inspected schema, but it does not perform open-ended natural-language reasoning beyond the implemented planning rules.
