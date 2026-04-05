## 1. Project Setup

- [x] 1.1 Initialize Python project structure with `src/`, `tests/`, and `static/` directories
- [x] 1.2 Create `requirements.txt` with FastAPI, uvicorn, SQLAlchemy, Pydantic dependencies
- [x] 1.3 Set up SQLite database schema file with tables: transactions, cards, alerts, notification_logs
- [x] 1.4 Configure FastAPI application entry point with CORS middleware for LAN access
- [x] 1.5 Add basic health check endpoint at `/api/v1/health`

## 2. Side-Hustle Tracker Backend

- [x] 2.1 Create SQLAlchemy models for side-hustle payments (amount, date, source, tax_flag)
- [x] 2.2 Implement POST `/api/v1/side-hustle/payments` endpoint with validation
- [x] 2.3 Implement GET `/api/v1/side-hustle/payments` endpoint with optional date range filtering
- [x] 2.4 Implement PUT `/api/v1/side-hustle/payments/{id}` endpoint for updates
- [x] 2.5 Implement DELETE `/api/v1/side-hustle/payments/{id}` endpoint
- [x] 2.6 Implement GET `/api/v1/side-hustle/net-cash` endpoint with tax exclusion logic
- [x] 2.7 Write unit tests for all side-hustle endpoints

## 3. Card Watchdog Backend

- [x] 3.1 Create SQLAlchemy models for credit cards (name, statement_date, due_date, balance, alert_threshold)
- [x] 3.2 Implement POST `/api/v1/cards` endpoint with validation
- [x] 3.3 Implement GET `/api/v1/cards` endpoint with days_remaining calculation and urgency ordering
- [x] 3.4 Implement PUT `/api/v1/cards/{id}/alert-threshold` endpoint
- [x] 3.5 Implement PUT `/api/v1/cards/{id}` endpoint for card updates
- [x] 3.6 Implement DELETE `/api/v1/cards/{id}` endpoint
- [x] 3.7 Write unit tests for all card endpoints

## 4. Native Alerts Integration

- [x] 4.1 Create notification engine module with subprocess calls to `termux-notification`
- [x] 4.2 Implement alert trigger logic that checks card days_remaining against alert_threshold
- [x] 4.3 Create SQLAlchemy model for notification_logs (timestamp, card_id, type, status, error_message)
- [x] 4.4 Implement POST `/api/v1/alerts/test` endpoint for manual notification testing
- [x] 4.5 Implement GET `/api/v1/alerts/history` endpoint with optional card_id filtering
- [x] 4.6 Add error handling for missing termux-api with user-friendly error messages
- [x] 4.7 Write unit tests for notification engine and alert endpoints

## 5. Background Alert Scheduler

- [x] 5.1 Implement background task scheduler using FastAPI's lifespan events
- [x] 5.2 Create periodic check that runs every hour to evaluate alert conditions
- [x] 5.3 Implement deduplication logic to prevent duplicate notifications for same condition
- [x] 5.4 Test scheduler with mock termux-notification commands

## 6. Remote Dashboard Frontend

- [x] 6.1 Create base HTML template with responsive CSS layout
- [x] 6.2 Implement net cash overview section with API integration
- [x] 6.3 Implement card countdown list with urgency highlighting for overdue cards
- [x] 6.4 Create side-hustle payment form with client-side validation
- [x] 6.5 Create credit card management form (add/edit/delete) with confirmation dialogs
- [x] 6.6 Add notification history viewer section
- [x] 6.7 Implement auto-refresh functionality for real-time data updates
- [x] 6.8 Test dashboard accessibility from multiple devices on LAN

## 7. Integration & Testing

- [x] 7.1 End-to-end test: Add payment via dashboard and verify in database
- [x] 7.2 End-to-end test: Register card and verify countdown calculation
- [x] 7.3 End-to-end test: Trigger alert and verify notification appears on Android
- [x] 7.4 Performance test: Dashboard loads within 2 seconds on LAN
- [x] 7.5 Error handling test: Graceful degradation when termux-api is unavailable
- [x] 7.6 Security test: Verify no external network exposure beyond LAN

## 8. WealthQuest Enhancements

- [x] 8.1 Implement JWT-based authentication system with Login/Logout
- [x] 8.2 Add Role-Based Access Control (Admin vs Viewer roles)
- [x] 8.3 Implement multi-template UI engine (Modern, Retro, Trainer themes)
- [x] 8.4 Add Recurring Transaction support ("Plan" module)
- [x] 8.5 Implement JSON database Export and Import functionality
- [x] 8.6 Integrate QR Code generator for LAN access sharing
- [x] 8.7 Create terminal-style Debug Console for log management
- [x] 8.8 Implement full CRUD (editing) for all transaction entries
- [x] 8.9 Enhance data model with `notes` and `category` (Main vs Side) support
- [x] 8.10 Initialize public Git repository with `.gitignore` and deployment scripts
