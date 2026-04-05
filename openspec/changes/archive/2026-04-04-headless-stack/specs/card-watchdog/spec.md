## ADDED Requirements

### Requirement: User can register a credit card with due date
The system SHALL allow users to add a credit card with name, statement date, due date, and current balance.

#### Scenario: Successful card registration
- **WHEN** user sends a POST request to `/api/v1/cards` with valid card data
- **THEN** the system stores the card and returns a 201 Created response with the card ID

#### Scenario: Invalid due date format
- **WHEN** user submits a due date in an invalid format
- **THEN** the system returns a 400 Bad Request error

### Requirement: System calculates days until card due date
The system SHALL automatically calculate and display the number of days remaining until each card's payment due date.

#### Scenario: Card due in 5 days
- **WHEN** user requests card details for a card due in 5 days
- **THEN** the system returns `days_remaining: 5`

#### Scenario: Card is past due
- **WHEN** user requests card details for a card whose due date has passed
- **THEN** the system returns `days_remaining: -3` (negative value indicating overdue)

### Requirement: User can configure alert threshold for card reminders
The system SHALL allow users to set a custom number of days before the due date when reminders should trigger.

#### Scenario: Set threshold to 3 days
- **WHEN** user sends a PUT request to `/api/v1/cards/{id}/alert-threshold` with `days: 3`
- **THEN** the system saves the threshold and returns confirmation

#### Scenario: Default threshold is 3 days
- **WHEN** a card is registered without specifying an alert threshold
- **THEN** the system sets the default threshold to 3 days

### Requirement: User can view all registered cards with countdown
The system SHALL provide an endpoint to retrieve all registered cards with their current countdown status.

#### Scenario: Retrieve all cards
- **WHEN** user sends a GET request to `/api/v1/cards`
- **THEN** the system returns a JSON array of all cards with days_remaining calculated

#### Scenario: Cards ordered by urgency
- **WHEN** user requests all cards
- **THEN** the system returns cards ordered by days_remaining ascending (most urgent first)