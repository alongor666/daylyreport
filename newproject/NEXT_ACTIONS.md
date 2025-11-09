# Next Actions Tracker

## Ingestion (Phase 2)
- [ ] Draft `docs/data/SCHEMA_CONTRACT.md` describing 76 字段 + 派生字段。
- [ ] Create `scripts/ingestion/schema.py` with Pydantic models + value enums。
- [ ] Implement `scripts/ingest_daily.py` CLI with options：`--input`, `--batch-date`, `--mapping`。
- [ ] Seed `data/mappings/staff_mapping.sample.json` for local dev。

## Backend (Phase 3)
- [ ] Initialize Poetry project inside `backend/` (`pyproject.toml`, `poetry.lock`).
- [ ] Scaffold FastAPI app (`app/main.py`, `app/api/routes`, `app/services`).
- [ ] Implement DuckDB connection helper + repository layer。
- [ ] Add PyTest setup + sample contract test for `/api/health`。

## Frontend (Phase 4)
- [ ] Initialize Vite + Vue + TS project (`frontend/`).
- [ ] Define Pinia stores (`filter`, `data`), API client, theme tokens。
- [ ] Build `GlobalFilterToolbar`, `KpiCard`, `WeekComparisonChart` skeleton components。
- [ ] Configure ESLint + Prettier + Vitest + Playwright。

## Tooling & QA (Phase 5)
- [ ] Create `scripts/run_dev.sh` orchestrating ingestion watcher + backend + frontend。
- [ ] Prepare `.github/workflows/ci.yml` or equivalent under `infra/`。
- [ ] Draft `scripts/smoke_check.sh` to hit `/health`, `/api/filter-options`, and run headless UI sanity。

## Documentation (Phase 6)
- [ ] Author `docs/ARCHITECTURE.md` (C4 view + data flow)。
- [ ] Author `docs/API_CONTRACTS.md` (OpenAPI excerpts + sample payloads)。
- [ ] Author `docs/QA_CHECKLIST.md` referencing validation要求。
