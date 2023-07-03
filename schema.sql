-- Create Stock table
CREATE TABLE IF NOT EXISTS financial_data (
    symbol TEXT NOT NULL,
    date DATE NOT NULL,
    open_price REAL NOT NULL,
    close_price REAL NOT NULL,
    volume INTEGER NOT NULL,
    PRIMARY KEY (symbol, date)
);


CREATE INDEX date_index on financial_data(date);
CREATE INDEX symbol_index on financial_data(symbol);