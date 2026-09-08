# PlantPulse

### Ethanol Plant Operations & Asset Management Platform

> **Status:** 🚧 Self-developed portfolio project — in active development (currently pre-Phase 0 / architecture & planning stage).
> This is an independently designed and built project used to apply AWS/DevOps experience to an industrial (ethanol plant) use case. **It is not deployed in, or affiliated with, any employer's production environment.**

**PlantPulse** is a full-stack, cloud-native platform for managing assets, maintenance, and operations at an ethanol manufacturing plant — built to demonstrate end-to-end skills across application development, AWS infrastructure, Terraform, Docker, and CI/CD.

---

## Table of Contents

- [Overview](#overview)
- [Why This Project](#why-this-project)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [User Roles & RBAC](#user-roles--rbac)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
- [Cost Awareness](#cost-awareness)
- [License](#license)

---

## Overview

Ethanol plants run many physical assets — tanks, pumps, motors, boilers, fermenters, distillation and dehydration units — across multiple process areas. Without a central system, asset records and maintenance history are typically scattered across spreadsheets, with no scheduling, no audit trail, and no role-based access control.

This platform provides:

- A central **asset registry** with full lifecycle tracking (`Planned → Procured → Received → Installed → Commissioned → Operational → Under Maintenance → Retired`)
- A **maintenance module**: preventive, corrective, and breakdown maintenance with work orders, technician assignment, and spare-parts tracking
- **Role-based access control** matching real plant roles
- A **dashboard** with operational KPIs
- A full **audit trail** for accountability
- Infrastructure that is **fully AWS-deployed and Terraform-managed**, with a real CI/CD pipeline

> This is an **IT/operations management platform** — not a PLC/SCADA industrial control system. It does not control physical equipment.

## Why This Project

Built independently to:

1. Apply existing AWS, DevOps, IAM, and infrastructure experience to a realistic, end-to-end system
2. Learn the ethanol plant domain deeply enough to model it accurately
3. Practice Infrastructure-as-Code, CI/CD, containerization, monitoring, and RBAC in a project with real depth
4. Produce a project that holds up to detailed technical interview questioning

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Frontend | React + TypeScript | SPA, component library TBD (Phase 6) |
| Backend | Python (FastAPI) | Async REST API, auto-generated OpenAPI docs |
| Database | PostgreSQL | Managed via SQLAlchemy + Alembic migrations |
| Auth | JWT (Phase 7), AWS Cognito (later) | RBAC enforced server-side |
| Containers | Docker, Docker Compose | Local dev parity with cloud |
| IaC | Terraform | VPC, ECS, RDS, ALB, ECR, IAM, Secrets Manager |
| CI/CD | GitHub Actions (OIDC to AWS) | No long-lived AWS keys |
| Cloud | AWS (ECS Fargate, RDS, S3, CloudFront, Route 53, CloudWatch) | |

## Architecture

Three-tier architecture: React SPA → FastAPI REST API → PostgreSQL, containerized locally and deployed to AWS ECS Fargate behind an Application Load Balancer, with RDS in a private subnet.

Full system and AWS architecture diagrams, service-by-service reasoning (why/alternatives/cost/security), and networking design live in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Repository Structure

```
plantpulse/
├── frontend/                  # React + TypeScript SPA
├── backend/
│   ├── app/
│   │   ├── api/                 # route modules
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── core/                 # config, security, RBAC deps
│   │   └── services/             # business logic
│   └── alembic/                  # migrations
├── infrastructure/
│   └── terraform/
│       ├── modules/              # vpc, ecs, rds, alb, etc.
│       └── envs/                  # dev / staging / prod tfvars
├── docker/                    # Dockerfiles, docker-compose.yml
├── .github/workflows/         # CI and CD pipelines
├── docs/                      # architecture, database, security, deployment docs
├── scripts/                   # helper scripts (seed data, local setup)
├── database/                  # ER diagrams, seed SQL
├── tests/                     # backend + frontend tests
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
└── .gitignore
```

## User Roles & RBAC

| Role | Access |
|---|---|
| **Admin** | Full access, including user/role management |
| **Plant Manager** | Dashboard, plant/area data, reports, read-only assets |
| **Maintenance Manager** | Full access to assets, maintenance, work orders, reports |
| **Maintenance Engineer** | Assets (read/update), work orders (create/update), maintenance records |
| **Technician** | Assigned work orders only |
| **Store/Inventory User** | Spare parts & inventory transactions |
| **Viewer** | Read-only |

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 0 | Project definition & architecture | 🔜 Next |
| 1 | Business/domain understanding | ⬜ |
| 2 | Requirements | ⬜ |
| 3 | System architecture | ⬜ |
| 4 | Database design | ⬜ |
| 5 | Backend development | ⬜ |
| 6 | Frontend development | ⬜ |
| 7 | Authentication & RBAC | ⬜ |
| 8 | Dockerization | ⬜ |
| 9 | Local deployment | ⬜ |
| 10 | Testing | ⬜ |
| 11 | GitHub repository setup | ⬜ |
| 12 | CI pipeline | ⬜ |
| 13 | AWS networking | ⬜ |
| 14 | AWS infrastructure (Terraform) | ⬜ |
| 15 | Container registry (ECR) | ⬜ |
| 16 | ECS deployment | ⬜ |
| 17 | RDS deployment | ⬜ |
| 18 | Frontend deployment | ⬜ |
| 19 | Monitoring & logging | ⬜ |
| 20 | Security hardening | ⬜ |
| 21 | CI/CD | ⬜ |
| 22 | Production-style improvements | ⬜ |
| 23 | Documentation | ⬜ |
| 24 | Interview preparation | ⬜ |

## Documentation

| Doc | Contents |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design, AWS architecture, requirements, tech decisions |
| `docs/DATABASE.md` | ER diagram, schema, migrations *(added in Phase 4)* |
| `docs/AWS_ARCHITECTURE.md` | Service-by-service AWS reasoning *(added in Phase 13/14)* |
| `docs/DEVOPS.md` | CI/CD pipeline design *(added in Phase 12)* |
| `SECURITY.md` | App and infra security model *(added in Phase 7/20)* |
| `docs/DEPLOYMENT.md` | How to deploy to AWS *(added in Phase 16+)* |
| `docs/COST.md` | Cost breakdown & shutdown checklist *(added in Phase 14)* |
| `docs/TROUBLESHOOTING.md` | Common errors & fixes *(growing throughout)* |
| `docs/INTERVIEW_GUIDE.md` | Project story & Q&A prep *(added in Phase 24)* |

## Getting Started

_Local setup instructions will be added in Phase 9 (Local Deployment) once the backend, frontend, and Docker Compose setup exist._

## Cost Awareness

This project is self-funded, so cost control is a first-class concern: smallest viable instance sizes, `terraform destroy` between sessions, short CloudWatch log retention, and explicit flagging of costly services (e.g. NAT Gateway) before they're provisioned. Full checklist in `docs/COST.md` (Phase 14).

## License

Personal portfolio project. All rights reserved unless a license is added later.
