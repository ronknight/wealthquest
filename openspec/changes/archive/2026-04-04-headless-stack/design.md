## Context

This design document outlines the implementation of **WealthQuest**, a self-hosted, lightweight financial ecosystem. It builds on the proposal.md which established the need for a solution combining a Python backend, Termux Android integration, and a multi-themed remote dashboard. The design prioritizes local data control, security through JWT, and a flexible user experience inspired by 1980s gaming and modern professional standards.

Constraints include:
- No cloud storage (data remains local).
- Performance requirements for real-time alerts.
- LAN-only communication for security.
- Compatibility with Termux environment.

## Goals / Non-Goals

**Goals:**
- Provide Frictionless financial tracking with clear Main vs Side-Hustle distinction.
- Enable cross-device access via LAN with QR-code sharing.
- Facilitate automated recurring transactions and alerts.
- Support multiple users with Role-Based Access Control (RBAC).

**Non-Goals:**
- Public internet hosting (LAN focus).
- Complex investment tracking or AI-based forecasting.

## Decisions

1. **Backend Framework: FastAPI**
   - Chose for performance and asynchronous support for background tasks.

2. **Security: JWT with RBAC**
   - Implemented `OAuth2PasswordBearer` with JWT tokens.
   - Roles: `admin` (full mutations) and `viewer` (read-only).
   - Password hashing via `Passlib` (bcrypt).

3. **Frontend: multi-page SPA with Theme Engine**
   - Built with Vanilla JS to keep it lightweight.
   - Implemented a dynamic theme engine using CSS variables and terminology dictionaries.
   - Themes: **Modern** (Professional), **Retro** (8-Bit), **Trainer** (Pokemon).

4. **Data Management: Atomic JSON Portability**
   - Added endpoints for full database Export/Import.
   - Use atomic operations to ensure schema consistency during imports.

5. **Automation: Lifespan-based Scheduler**
   - Leveraged FastAPI's `lifespan` context manager to run an hourly background task for both alerts and recurring transactions.

## Risks / Trade-offs

1. [Local IP volatility] → Mitigation: Display host IP and URL prominently in the Admin UI.
2. [Data overwrite risk] → Mitigation: Require Admin role and explicit confirmation for database imports.
3. [Termux-API availability] → Mitigation: Graceful fallback and logging in the Audit Trail.

## Open Questions (Resolved)

1. **Export/Import**: Implemented JSON-based backup in the Admin module.
2. **Categorization**: Introduced `category` (main/side) to transactions.
3. **Multi-user**: Added a `User` model and login flow.
