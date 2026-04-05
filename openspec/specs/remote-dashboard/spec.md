# remote-dashboard Specification

## Purpose
TBD - created by archiving change headless-stack. Update Purpose after archive.
## Requirements
### Requirement: System serves a web dashboard on LAN
The system SHALL serve a responsive web dashboard accessible from any browser on the local network.

#### Scenario: Access dashboard from LAN
- **WHEN** user navigates to `http://<device-ip>:8000` from another device on the same network
- **THEN** the system serves the dashboard HTML page

#### Scenario: Dashboard loads on localhost
- **WHEN** user navigates to `http://localhost:8000` on the host device
- **THEN** the system serves the dashboard HTML page

### Requirement: Dashboard displays net cash overview
The dashboard SHALL prominently display the current net cash total excluding tax-flagged transactions.

#### Scenario: Net cash display
- **WHEN** the dashboard loads
- **THEN** the net cash total is fetched from `/api/v1/side-hustle/net-cash` and displayed

#### Scenario: Net cash updates on refresh
- **WHEN** user refreshes the dashboard
- **THEN** the net cash total reflects the latest data

### Requirement: Dashboard shows card countdown list
The dashboard SHALL display all registered credit cards with their days remaining countdown.

#### Scenario: Card list rendering
- **WHEN** the dashboard loads
- **THEN** all cards are fetched from `/api/v1/cards` and displayed with days remaining

#### Scenario: Overdue card highlighting
- **WHEN** a card has negative days_remaining
- **THEN** the card is visually highlighted in red on the dashboard

### Requirement: Dashboard allows adding side-hustle payments
The dashboard SHALL provide a form to add new side-hustle payments.

#### Scenario: Add payment via form
- **WHEN** user fills out the payment form and submits
- **THEN** the system sends a POST request to `/api/v1/side-hustle/payments` and refreshes the payment list

#### Scenario: Form validation feedback
- **WHEN** user submits the form with missing required fields
- **THEN** the dashboard displays validation errors without submitting

### Requirement: Dashboard allows managing credit cards
The dashboard SHALL provide functionality to add, edit, and remove credit cards.

#### Scenario: Add new card via form
- **WHEN** user fills out the card registration form and submits
- **THEN** the system sends a POST request to `/api/v1/cards` and refreshes the card list

#### Scenario: Delete card confirmation
- **WHEN** user clicks delete on a card
- **THEN** the dashboard shows a confirmation dialog before sending the DELETE request

