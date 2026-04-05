## Why

Many individuals need to track personal finances including side-income and credit card payments but face challenges with fragmented tools or over-engineered solutions. **WealthQuest** provides a self-hosted, lightweight combination of a Python REST API with an Android frontend via Termux, enabling remote access from any browser while maintaining full data control on the user's own device. It solves the need for integrated transaction logging, automated due date alerts, and a unified web dashboard without relying on third-party cloud services or heavy desktop applications.

## What Changes

* Introduce a new FastAPI backend with SQLite persistence exposing REST endpoints for transactions, cards, and alerts.
* Implement Termux integration for native Android notifications via termux-api.
* Add a responsive, multi-page web dashboard with support for multiple templates (Modern, Retro, Trainer).
* Implement secure JWT-based authentication with Role-Based Access Control (Admin and Viewer).
* Enable recurring transaction automation ("Plan" system).
* Provide data portability through JSON import/export tools.

## Capabilities

### New Capabilities

**WealthQuest Core**
- `wealth-engine`: Unified tracking for Main Income and Side Hustles with tax-aware categorization.
- `automation-planner`: Recurring transaction system for automated income and bill logging.
- `role-access-control`: Secure multi-user system with Admin (full access) and Viewer (read-only) roles.

**Notifications & Watchdog**
- `card-watchdog`: Automated countdown for credit card due dates with user-configurable reminder thresholds.
- `native-alerts`: Android system notifications via termux-api triggered from server-side events.

**User Experience**
- `multi-template-ui`: Dynamic theming engine supporting Professional (Modern), 8-Bit Game (Retro), and Pokemon (Trainer) aesthetics.
- `remote-connectivity`: QR-code based LAN sharing for instant access from laptops and other devices.
- `debug-terminal`: Integrated command-line console for audit trail management and system diagnostics.

### Modified Capabilities

*(None - these are all new capabilities)*

## Impact

* Python Package: FastAPI, SQLAlchemy, Pydantic, Passlib, Python-Jose.
* Infrastructure: SQLite database with multi-user schema, hourly background scheduler.
* Frontend: Vanilla JS SPA with Chart.js visualization and FontAwesome iconography.
* Environment: Termux on Android with termux-api integration.
