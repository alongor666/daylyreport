# Implementation Roadmap

## Phase 0 — Foundations
- Confirm scope using `context.md` / `prompt.md` artifacts (already committed).
- Decide on tech stack:
  - **Ingestion**: Python 3.11, DuckDB, Pandas, Pydantic for schema validation.
  - **Backend**: FastAPI + Uvicorn, SQLModel (DuckDB), Redis (optional) for caching.
  - **Frontend**: Vue 3 + Vite + Pinia + TypeScript + ECharts, Vitest + Playwright.
  - **Tooling**: Poetry (backend), pnpm or npm (frontend), Taskfile/Makefile for DX.

## Phase 1 — Repository Scaffolding
1. Create directories: `backend/`, `frontend/`, `data/`, `scripts/`, `docs/`, `infra/`.
2. Add base configs:
   - `pyproject.toml` (backend) with FastAPI, DuckDB, Pandas, Pydantic, SQLModel.
   - `package.json` (frontend) with Vue, Pinia, ECharts, Axios, Vite, Vitest, Playwright.
   - `.editorconfig`, `.gitignore`, `.prettierrc`, `.eslintrc.cjs`, `.ruff.toml`.
3. Provide `.env.example` capturing shared settings (data paths, ports, feature flags).
4. Author high-level README referencing context/prompt and outline run commands.

## Phase 2 — Data Ingestion Pipeline
1. Define schema contract (Pydantic models) for the 76 columns + derived fields.
2. Implement `scripts/ingest_daily.py`:
   - CLI arguments: `--input`, `--batch-date`, `--output-db`, `--mapping-file`.
   - Steps: load Excel/CSV → validate → enrich with mapping → compute derived flags → write to DuckDB tables (`raw_records`, `daily_agg`, `policy_staff_map`) → produce `mismatch_count` metrics.
   - Emit JSON summary + log file under `data/logs/`.
3. Add unit tests (PyTest) for ingestion (happy path + missing column + conflicting mapping).
4. Document ingestion flow in `docs/data/INGESTION.md`.

## Phase 3 — Backend Services
1. FastAPI app structure:
   - `app/main.py`, `app/api/routes/*.py`, `app/core/config.py`, `app/services/*.py`, `app/schemas/*.py`, `app/db/duckdb.py`.
2. Implement endpoints defined in `context.md` + `prompt.md`, including validation & caching.
3. Add business logic modules:
   - KPI windows service (day/last7d/last30d, wanInt outputs, ratios from ingestion table).
   - Week comparison service (D/D-7/D-14) with label formatting.
   - Filter service using policy mapping + enumerations.
4. Tests:
   - PyTest with TestClient covering each endpoint and edge cases (empty data, invalid filters, anchor date out of range).
   - Contract schemas (Pydantic/JSON Schema) stored under `backend/app/schemas/contracts/`.
5. Provide `backend/start.sh` and `backend/Taskfile.yml` for local dev.

## Phase 4 — Frontend SPA
1. Scaffold Vite + Vue 3 + TypeScript + Pinia project in `frontend/`.
2. Implement global layout:
   - Sticky filter toolbar (data scope toggle, metric toggle, time buttons, cascaded selects, chips summary).
   - KPI grid with `KpiCard` component supporting `valueType` + sparkline.
   - Week comparison chart using ECharts with 6-column tooltip, D / D-7 / D-14 bar groups.
   - Ratio cards/pie charts + premium range distribution.
3. State management:
   - `stores/filter.ts` for options, active filters, policy locking.
   - `stores/data.ts` for KPI/Chart/pie data, caching, validation banners.
   - `services/api.ts` centralizing Axios instance & typing.
4. Testing & QA:
   - Vitest component tests (KpiCard formatting, filter logic).
   - Playwright flows for filter cascade, color thresholds, tooltip text.
5. Theming & accessibility per `context.md` color rules and ARIA hints.

## Phase 5 — Tooling & CI
1. Scripts:
   - `scripts/run_dev.sh`: orchestrate ingestion watch + backend + frontend.
   - `scripts/smoke_check.sh`: hit `/health`, `/api/filter-options`, run headless UI sanity (Playwright).
2. CI Pipeline (GitHub Actions sample): lint → backend tests → frontend tests → build.
3. Docker Compose for local stack (DuckDB file volume, backend, frontend, redis optional proxy).

## Phase 6 — Documentation & Handoff
1. Update `newproject/README.md` with quick start, architecture diagram, validation checklist.
2. Add `docs/ARCHITECTURE.md`, `docs/API_CONTRACTS.md`, `docs/DATA_DICTIONARY.md`, `docs/QA_CHECKLIST.md`.
3. Capture demo instructions (screenshots/recording script) per prompt.
4. Final smoke test + summary report referencing acceptance criteria.

## Immediate Next Actions
1. Scaffold directory tree + config placeholders (Phase 1 step 1-2).
2. Draft `.env.example`, `.gitignore`, repo-level README linking to context/prompt.
3. Initialize ingestion package skeleton (`backend/ingestion` or `scripts/`).
