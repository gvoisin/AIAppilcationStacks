# Client App (Lit + A2A/A2UI)

This folder contains the frontend shell (`Lit`) for the application and scripts to run it alone or together with the Python server.

## Prerequisites

- Node.js 20+ (recommended)
- npm
- Optional for full demo: `uv` (used to run `app/server`)

## Quick Start (Client Only)

From this folder (`app/client`):

```bash
npm install
npm run serve:shell
```

Then open the Vite dev URL (typically `http://localhost:5173`).

## Full Demo (Client + Server)

From this folder (`app/client`):

```bash
npm install
npm run demo:edge
```

This starts:

- `SHELL`: frontend (`npm run serve:shell`)
- `REST`: backend (`uv run __main__.py` from `app/server`)

Default backend URL expected by the client is `http://localhost:10002`.

## Available Scripts

- `npm run serve:shell`: runs the Lit shell in dev mode (`app/client/shell`)
- `npm run serve:agent:edge`: runs the Python server from `app/server`
- `npm run demo:edge`: runs shell + server in parallel

## What You See in the UI

The shell renders three modules (toggles in the header):

- `Traditional` -> `http://localhost:10002/traditional`
- `Chat` -> `http://localhost:10002/llm`
- `Agent` -> `http://localhost:10002` / `http://localhost:10002/agent`

## Project Structure

- [shell/app.ts](./shell/app.ts): main app container and module toggles
- [shell/components](./shell/components): UI modules (`main_traditional`, `main_chat`, `main_agent`, input/config components)
- [shell/services](./shell/services): A2UI client/router and session routing
- [shell/middleware](./shell/middleware): Vite middleware for `/a2a` proxy/event handling
- [shell/configs](./shell/configs): starter configs for module behavior and payloads
- [shell/ui/custom-components](./shell/ui/custom-components): reusable A2UI-rendered components

## Notes

- Scripts are written for PowerShell/Windows-first workflows.
- If your server runs on a different host/port, update hardcoded URLs in `shell/components` and `shell/services`.
