# Agent Flow Documentation

This folder contains exported documentation artifacts for the dynamic agent module flow.

## Files

- [`mermaid.md`](./mermaid.md)
  - Mermaid sequence diagram showing the end-to-end agent execution flow
  - Covers client request, backend orchestration, tool calls, UI generation, and follow-up UI actions

- [`agents.xlsx`](./agents.xlsx)
  - Excel workbook containing the step-by-step agent flow table
  - Columns include step, file, function/class, input, output, and external dependency

## Recommended reading order

1. Open `mermaid.md` for the high-level execution sequence
2. Open `agents.xlsx` for the implementation-level mapping by file and function

## Scope

These artifacts describe the **dynamic agent mode** flow, not the plain chat mode flow.
