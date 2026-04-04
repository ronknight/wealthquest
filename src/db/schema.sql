-- SQLite database schema for financial tracking ecosystem

-- Transactions table for side-hustle payments
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    source TEXT,
    tax_flag INTEGER DEFAULT 0
);

-- Credit cards table
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    statement_date TEXT,
    due_date TEXT NOT NULL,
    balance REAL DEFAULT 0.0,
    alert_threshold INTEGER DEFAULT 3
);

-- Alerts table for notification logs
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    card_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'sent',
    error_message TEXT,
    FOREIGN KEY (card_id) REFERENCES cards (id)
);

-- Additional logs or tables can be added here as needed