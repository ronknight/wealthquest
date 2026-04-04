## Why

Many individuals need to track personal finances including side-income and credit card payments but face challenges with fragmented tools or over-engineered solutions. This ecosystem provides a self-hosted, lightweight combination of a Python REST API with an Android frontend via Termux, enabling remote access from any browser while maintaining full data control on the user's own device. It solves the need for integrated transaction logging, automated due date alerts, and a unified web dashboard without relying on third-party cloud services or heavy desktop applications.

## What Changes

* Introduce a new FastAPI backend with SQLite persistence exposing REST endpoints for transactions, cards, and alerts
* Implement Termux integration for native Android notifications via termux-api
* Add remote web dashboard for viewing and managing financial data
* Enable side-hustle tracking with tax-aware categorization

## Capabilities

### New Capabilities

Transactions and side income are handled here.
- `side-hustle-tracker`: Dedicated logging for side income separate from regular transactions, with options to include/exclude tax from net cash view

Notifications for credit cards and alerts
- `card-watchdog`: Automated countdown for credit card due dates with user-configurable reminder thresholds
- `native-alerts`: Android system notifications via termux-api triggered from server-side events

Web interfaces for remote access
- `remote-dashboard`: A responsive web interface accessible from any browser on the LAN for viewing and managing data

### Modified Capabilities

*(None - these are all new capabilities)*

## Impact

* New Python package: FastAPI, SQLAlchemy, Pydantic
* New Android/Termux integration components: shell scripts or subprocess calls to termux-notification
* New SQLite database schema (transactions, cards, alerts, notification logs)
* New static assets for the web dashboard (HTML/CSS/JS, possibly a lightweight framework)
* No impact on existing systems or APIs