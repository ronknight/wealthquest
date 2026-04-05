## ADDED Requirements

### Requirement: User can log a side-hustle payment
The system SHALL allow users to record a side-hustle payment with amount, date, source, and optional tax flag.

#### Scenario: Successful payment logging
- **WHEN** user submits a POST request to `/api/v1/side-hustle/payments` with valid payment data
- **THEN** the system stores the payment and returns a 201 Created response with the payment ID

#### Scenario: Missing required fields
- **WHEN** user submits a POST request without amount or date
- **THEN** the system returns a 400 Bad Request error with details of missing fields

### Requirement: User can view all side-hustle payments
The system SHALL provide an endpoint to retrieve all logged side-hustle payments, optionally filtered by date range.

#### Scenario: Retrieve all payments
- **WHEN** user sends a GET request to `/api/v1/side-hustle/payments`
- **THEN** the system returns a JSON array of all payments ordered by date descending

#### Scenario: Filter by date range
- **WHEN** user sends a GET request with `start_date` and `end_date` query parameters
- **THEN** the system returns only payments within that date range

### Requirement: User can calculate net cash excluding tax
The system SHALL provide a net cash summary that excludes payments marked as taxable.

#### Scenario: Net cash calculation
- **WHEN** user sends a GET request to `/api/v1/side-hustle/net-cash`
- **THEN** the system returns total income minus any flagged tax amounts

#### Scenario: All payments are taxable
- **WHEN** all payments have the tax flag set to true
- **THEN** the net cash total is zero

### Requirement: User can edit or delete a side-hustle payment
The system SHALL allow users to update or remove existing side-hustle payments.

#### Scenario: Update a payment
- **WHEN** user sends a PUT request to `/api/v1/side-hustle/payments/{id}` with updated data
- **THEN** the system updates the payment and returns the modified record

#### Scenario: Delete a payment
- **WHEN** user sends a DELETE request to `/api/v1/side-hustle/payments/{id}`
- **THEN** the system removes the payment and returns a 204 No Content response