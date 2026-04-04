## Context

This design document outlines the implementation of the headless-stack financial tracking ecosystem. It builds on the proposal.md which established the need for a self-hosted, lightweight solution combining Python backend, Termux Android integration, and a remote dashboard. The design prioritizes local data control with minimal external dependencies, leveraging SQLite for storage and Termux-api for native Android notifications.

Constraints include:
- No cloud storage (data must remain local on user devices)
- Performance requirements for real-time alerts
- Compatibility with Termux environment limitations
- LAN-only communication for security

Stakeholders: Individual users managing personal finances, with potential expansion to small teams.

## Goals / Non-Goals

**Goals:**
- Provide frictionless financial tracking with side-incom\e integration
- Enable cross-device access via LAN
- Facilitate automated alerts without third-party services

**Non-Goals:**
- Support multi-user accounts (single-user focus for now)
- Cloud synchronization (local device requirement)
- Complex tax calculations beyond basic categorization

## Decisions

1. **Backend Framework: FastAPI vs. Flask**
   - Chose FastAPI for performance and built-in dependency injection
   - Alternatives considered: Flask (simpler but less performant), Django (overkill for scope)

2. **Data Storage: SQLite vs. PostgreSQL**
   - Selected SQLite for simplicity and zero-configuration
   - Alternatives: PostgreSQL (better scalability but requires server setup)

3. **Notification System: Termux-api vs. Push APIs**
   - Implemented Termux-api for direct Android integration
   - Alternatives: Firebase Cloud Messaging (requires internet), local push services\n
4. **Web Dashboard Technology**
   - Will use lightweight Vanilla JS with HTML/CSS for responsiveness
   - Alternatives: React/Vue (more complex, heavier dependency)

5. **REST API Design**
   - Followed RESTful principles with versioning
   - Endpoint structure: `/api/v1/transactions`, `/api/v1/cards`, etc.

## Risks / Trade-offs

1. [SQLite Limitations] → Mitigation: Optimize queries, use indexing for frequently accessed fields
2. [Termux API Restrictions] → Mitigation: Cache notification history locally
3. [LAN Dependency] → Mitigation: Plan for Wi-Fi fallback mechanisms
4. [Android Permissions] → Mitigation: Request necessary permissions at app install

## Open Questions

1. Should the web dashboard include data export functionality? (Needs specification in specs.md)
2. How to handle transaction categorization rules - manual input or AI suggestions?
3. What alert threshold configurations to include by default?