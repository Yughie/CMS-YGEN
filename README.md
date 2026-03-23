# CMS-YGEN

A polymorphic, multi-industry CMS platform designed to support different business domains from one shared system.

## What We Are Going To Build

We are building a CMS that can dynamically handle content for different industries, including:

- Real estate
- Product-based businesses
- Rental businesses
- Other future industry verticals

The goal is one strong core platform with reusable patterns, plus industry-specific extensions where needed.

## Project Vision

- Build once, extend many times.
- Keep a stable shared content model while allowing industry-specific fields and workflows.
- Maintain modern, production-quality code standards in both backend and frontend.
- Avoid deprecated framework patterns and keep the stack up to date.

## Tech Stack

- Backend: Django (modern best practices, deprecation-aware)
- Frontend: React + Tailwind CSS
- API: Django-based API layer for CMS content delivery and management
- Data: Relational-first modeling with explicit constraints and queryable fields

## High-Level Architecture

### Backend (Django)

- A shared content core for common fields (slug, status, publish windows, ownership, metadata)
- Industry modules that extend the core through clear relationships
- Service/domain layer for business rules
- Thin API/view layer for transport and validation boundaries
- Strong migration discipline and data integrity constraints

### Frontend (React + Tailwind)

- Reusable UI primitives and layout components
- Content block rendering system (component registry/mapping)
- Industry-specific blocks built on top of shared components
- Responsive and accessible UI with clear loading/error/empty states

## Implementation Plan

### Phase 1: Foundation

- Set up baseline backend and frontend architecture conventions
- Define shared CMS content contract
- Define coding standards, linting, and testing strategy

### Phase 2: Core CMS

- Implement base content models and lifecycle rules
- Build core CRUD/API endpoints
- Build foundational frontend pages and reusable components

### Phase 3: Industry Modules

- Add first two industry implementations (example: real estate and products)
- Validate polymorphic behavior end to end
- Extend frontend rendering for industry-specific sections

### Phase 4: Reliability and Scale

- Improve performance (query optimization, code splitting, caching where applicable)
- Harden security and permissions
- Expand automated test coverage
- Prepare for additional industry modules

## Engineering Standards

### Backend Standards

- Use modern Django APIs and avoid deprecated patterns
- Keep business logic outside transport layers
- Enforce constraints and indexes intentionally
- Prevent N+1 queries with proper ORM optimization
- Add tests for non-trivial logic and API behavior

### Frontend Standards

- Use modern React patterns (functional components and hooks)
- Keep components composable and focused
- Use Tailwind consistently with shared design tokens
- Ensure accessibility and responsive behavior by default
- Add tests for component behavior and integration paths

## Repository Structure

- `backend/` Django services, models, API, business logic, tests
- `frontend/` React application, Tailwind styling, UI components, tests
- `.github/agents/` Custom project agents for backend and frontend workflows

## Definition of Done for Features

A feature is considered done when:

- Requirements are implemented end to end
- Tests are added/updated and passing
- No deprecated framework usage is introduced
- Accessibility and responsive behavior are verified (frontend)
- Migrations and backward compatibility concerns are addressed (backend)

## Immediate Next Steps

1. Define the base content model and extension strategy in backend.
2. Define API contracts for shared and industry-specific content blocks.
3. Scaffold frontend content-rendering registry for dynamic CMS blocks.
4. Implement first industry vertical as a reference implementation.

## Backend Quick Start (uv)

1. Change into the backend directory:
   - `cd backend`
2. Create the virtual environment (already in repo setup):
   - `uv venv .venv`
3. Install dependencies from project metadata:
   - `uv sync`
4. Run migrations:
   - `uv run python manage.py migrate`
5. Start the backend server:
   - `uv run python manage.py runserver`
6. Generate sample CMS content:
   - `uv run python manage.py seed_sample_content`
   - Optional reset: `uv run python manage.py seed_sample_content --reset`

## Frontend Quick Start (React + Tailwind)

1. Change into frontend directory:
   - `cd frontend`
2. Install dependencies:
   - `npm install`
3. Create frontend env file from example:
   - copy `.env.example` to `.env`
4. Ensure API base points to backend:
   - `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1`
5. Run frontend:
   - `npm run dev`

Frontend routes:

- `/` content list view
- `/content/:slug` content detail view

Available starter API endpoints:

- `GET /api/v1/health/`
- `GET /api/v1/contents/`

Backend content features now include:

- Base content `description` for long-form summaries.
- Dynamic content blocks per content item (`hero`, `rich_text`, `gallery`, `cta`) with ordered positions.
- Image asset management per content item with captions, alt text, sort order, and one primary image.

## Long-Term Outcome

A scalable CMS platform where adding a new industry is an extension task, not a full rewrite.
