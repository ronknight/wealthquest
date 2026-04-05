# native-alerts Specification

## Purpose
TBD - created by archiving change headless-stack. Update Purpose after archive.
## Requirements
### Requirement: System triggers Android notification via termux-api
The system SHALL send native Android notifications using the `termux-notification` command when an alert condition is met.

#### Scenario: Notification for card due soon
- **WHEN** a card's days_remaining equals its alert threshold
- **THEN** the system executes `termux-notification` with card name and days remaining

#### Scenario: Notification includes actionable details
- **WHEN** a notification is triggered
- **THEN** the notification body contains the card name, due date, and days remaining

### Requirement: User can test notification delivery
The system SHALL provide an endpoint to manually trigger a test notification.

#### Scenario: Send test notification
- **WHEN** user sends a POST request to `/api/v1/alerts/test`
- **THEN** the system triggers a test notification and returns success status

#### Scenario: termux-api not available
- **WHEN** the test endpoint is called but termux-api is not installed
- **THEN** the system returns a 500 Internal Server Error with guidance to install termux-api

### Requirement: System logs all notification attempts
The system SHALL record every notification attempt in a log table for auditing and debugging.

#### Scenario: Log successful notification
- **WHEN** a notification is successfully sent
- **THEN** the system logs the timestamp, card ID, notification type, and status as "sent"

#### Scenario: Log failed notification
- **WHEN** a notification fails to send
- **THEN** the system logs the timestamp, card ID, notification type, status as "failed", and error message

### Requirement: User can view notification history
The system SHALL provide an endpoint to retrieve the notification log.

#### Scenario: Retrieve all notifications
- **WHEN** user sends a GET request to `/api/v1/alerts/history`
- **THEN** the system returns a JSON array of all notification attempts ordered by timestamp descending

#### Scenario: Filter by card
- **WHEN** user sends a GET request with `card_id` query parameter
- **THEN** the system returns only notifications for that specific card

