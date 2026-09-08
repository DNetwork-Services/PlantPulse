# Requirements

> Part of **[PlantPulse](../README.md)**. Derived from the domain understanding in Phase 1 (dual feedstock route: grain + molasses). Requirement IDs are referenced by later phases (database design, API design, tests) — treat renumbering as a breaking change to avoid.

## Table of Contents

- [Module: Plant & Area](#module-plant--area-plt)
- [Module: Asset Management](#module-asset-management-ast)
- [Module: Maintenance Planning](#module-maintenance-planning-mp)
- [Module: Work Orders](#module-work-orders-wo)
- [Module: Spare Parts & Inventory](#module-spare-parts--inventory-inv)
- [Module: Users & RBAC](#module-users--rbac-usr)
- [Module: Dashboard & Reporting](#module-dashboard--reporting-dsh)
- [Module: Audit Trail](#module-audit-trail-aud)
- [Module: Authentication](#module-authentication-auth)
- [Non-Functional Requirements](#non-functional-requirements)
- [Traceability Note](#traceability-note)

---

## Module: Plant & Area (`PLT`)

| ID | Requirement |
|---|---|
| PLT-01 | System supports a single plant record (name, location, capacity, commissioning date) |
| PLT-02 | Plant is divided into **areas** (e.g. Fermentation, Distillation, Utilities) |
| PLT-03 | Each area has a `feedstock_route` tag: `grain`, `molasses`, or `shared` |
| PLT-04 | Areas can be activated/deactivated without deletion (soft state, for historical integrity) |
| PLT-05 | Each area has a responsible role (e.g. default Maintenance Manager) for notification routing (future phase) |

## Module: Asset Management (`AST`)

| ID | Requirement |
|---|---|
| AST-01 | Register an asset with: name, asset code (unique), category, area, location detail, manufacturer, model, serial number |
| AST-02 | Each asset belongs to one `asset_category` (e.g. Fermenter, Pump, Boiler) |
| AST-03 | Track ownership metadata: purchase date, purchase cost, vendor, warranty expiry, AMC (annual maintenance contract) validity |
| AST-04 | Track asset **lifecycle status**: `Planned → Procured → Received → Installed → Commissioned → Operational → Under Maintenance → Retired` |
| AST-05 | Every lifecycle status change is recorded in `asset_lifecycle_history` with timestamp and actor |
| AST-06 | Assets can be flagged `is_critical` (true/false) — critical assets get elevated dashboard visibility |
| AST-07 | Documents (manuals, warranty certs, inspection reports) can be attached to an asset (metadata + S3 reference — actual upload wired up in Phase 8+) |
| AST-08 | Assets can be searched/filtered by category, area, status, criticality, vendor |
| AST-09 | Asset detail view shows full maintenance history (joined from `MP`/`WO` modules) |
| AST-10 | Deleting an asset is disallowed once it has maintenance history — must be retired instead (data integrity) |

## Module: Maintenance Planning (`MP`)

| ID | Requirement |
|---|---|
| MP-01 | Create a **maintenance plan** for an asset or asset category (template: what needs doing, how often) |
| MP-02 | Maintenance plans support frequency types: calendar-based (e.g. every 90 days) or usage-based (e.g. every N operating hours/cycles) — usage-based needed for molecular sieve regeneration cycles |
| MP-03 | System generates **maintenance schedules** (concrete due dates) from active plans |
| MP-04 | Overdue schedules are flagged and surfaced on the dashboard (`DSH-05`) |
| MP-05 | A schedule automatically produces a **work order** when due (or N days before, configurable) |

## Module: Work Orders (`WO`)

| ID | Requirement |
|---|---|
| WO-01 | Work orders have a `type`: `Preventive`, `Corrective`, `Breakdown` |
| WO-02 | Work order status flow: `Open → Assigned → In Progress → Completed → Closed` (with `Cancelled` as a side-exit) |
| WO-03 | A work order is linked to exactly one asset |
| WO-04 | A work order can be assigned to one technician; reassignment is logged |
| WO-05 | Completing a work order requires: work description, parts used (from `INV`), downtime duration if applicable |
| WO-06 | Breakdown-type work orders capture a **downtime record** (start time, end time, cause) automatically |
| WO-07 | Work orders have a priority: `Low`, `Medium`, `High`, `Critical` |
| WO-08 | Completed work orders roll up into `maintenance_records` for historical reporting |
| WO-09 | Technicians can only see/update work orders assigned to them (enforced via `USR` RBAC) |

## Module: Spare Parts & Inventory (`INV`)

| ID | Requirement |
|---|---|
| INV-01 | Spare parts catalog: part name, part code, unit of measure, reorder threshold |
| INV-02 | Inventory tracks current stock quantity per part |
| INV-03 | Inventory transactions record every stock in/out with reference (e.g. linked work order for stock-out) |
| INV-04 | Parts falling below reorder threshold are flagged (dashboard visibility, `DSH-06`) |
| INV-05 | Only Store/Inventory User and Admin roles can adjust stock directly; work-order completion auto-deducts stock |

## Module: Users & RBAC (`USR`)

| ID | Requirement |
|---|---|
| USR-01 | Users have: name, email (unique, login identifier), role, active/inactive status |
| USR-02 | Roles: Admin, Plant Manager, Maintenance Manager, Maintenance Engineer, Technician, Store/Inventory User, Viewer |
| USR-03 | Permissions are modeled as `role → permissions` (not hardcoded per-endpoint role checks), so new roles can be composed later |
| USR-04 | Every API endpoint declares its required permission(s); enforcement happens server-side (never trust the frontend) |
| USR-05 | Admin can create/deactivate users and reassign roles |
| USR-06 | A deactivated user cannot authenticate, but their historical actions (audit log, work orders) remain intact |

## Module: Dashboard & Reporting (`DSH`)

| ID | Requirement |
|---|---|
| DSH-01 | Total assets, active assets, assets under maintenance, critical assets (counts) |
| DSH-02 | Open work orders count, broken down by type (Preventive/Corrective/Breakdown) |
| DSH-03 | Overdue maintenance count and list |
| DSH-04 | Upcoming maintenance (next 7/30 days) |
| DSH-05 | Overdue schedules flagged distinctly (from `MP-04`) |
| DSH-06 | Low-stock spare parts flagged (from `INV-04`) |
| DSH-07 | Downtime trend chart (by area, by month) |
| DSH-08 | Dashboard content is filtered by role — e.g. Technician sees only their assigned work orders, not plant-wide KPIs |

## Module: Audit Trail (`AUD`)

| ID | Requirement |
|---|---|
| AUD-01 | Every create/update/delete on `assets`, `work_orders`, `users`, `inventory` is logged |
| AUD-02 | Audit entry captures: user, action, entity type, entity ID, timestamp, previous value (if update), new value |
| AUD-03 | Audit logs are append-only — no update/delete API exists for them, even for Admin |
| AUD-04 | Admin can view/filter the audit log by user, entity, date range |

## Module: Authentication (`AUTH`)

| ID | Requirement |
|---|---|
| AUTH-01 | Login via email + password, returns a JWT access token |
| AUTH-02 | Passwords stored hashed (bcrypt/argon2) — never plaintext, never reversible |
| AUTH-03 | JWT has a short expiry (e.g. 30–60 min); refresh mechanism added in Phase 7 |
| AUTH-04 | All API endpoints except `/login` and `/health` require a valid JWT |
| AUTH-05 | Cognito integration is a documented future upgrade path, not required for MVP (per Phase 0 constraints) |

---

## Non-Functional Requirements

(Full list already defined in `ARCHITECTURE.md`; restated here for completeness since NFRs are part of formal requirements too.)

| # | Requirement |
|---|---|
| N1 | Containerized (Docker) — runs identically on laptop and AWS |
| N2 | Infrastructure fully defined as Terraform code |
| N3 | CI on every PR: lint, tests, build; CD on merge: image push + deploy |
| N4 | Secrets never committed |
| N5 | Least-privilege IAM; app RBAC kept conceptually separate from AWS IAM |
| N6 | Structured logs + CloudWatch metrics + health checks |
| N7 | Cost-aware: destroyable environments, free-tier-first, documented shutdown |
| N8 | Reasonable performance at demo scale |
| N9 | HTTPS everywhere in cloud |
| N10 | Versioned DB migrations via Alembic |

## Traceability Note

Phase 4 (Database Design) will map each requirement above to specific tables/columns. Phase 5/6 (Backend/Frontend) will reference requirement IDs in PR descriptions and commit messages where useful (e.g. `feat: implement work order status flow (WO-02)`) — this is a small habit that makes your Git history read like a real engineering trail, not just a feature dump.
