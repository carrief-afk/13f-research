CREATE TABLE IF NOT EXISTS managers (
    manager_id BIGINT PRIMARY KEY,
    manager_name VARCHAR NOT NULL,
    cik VARCHAR,
    style VARCHAR,
    country VARCHAR
);

CREATE TABLE IF NOT EXISTS stocks (
    stock_id BIGINT PRIMARY KEY,
    cusip VARCHAR NOT NULL,
    ticker VARCHAR,
    issuer VARCHAR NOT NULL,
    sector VARCHAR,
    industry VARCHAR,
    exchange VARCHAR,
    market_cap DOUBLE
);

CREATE TABLE IF NOT EXISTS filings (
    filing_id BIGINT PRIMARY KEY,
    accession_number VARCHAR NOT NULL,
    quarter VARCHAR NOT NULL,
    filing_date DATE,
    manager_id BIGINT NOT NULL,
    is_amendment BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS holdings (
    holding_id BIGINT PRIMARY KEY,
    filing_id BIGINT NOT NULL,
    stock_id BIGINT NOT NULL,
    value_usd_thousands DOUBLE,
    shares DOUBLE,
    share_type VARCHAR,
    put_call VARCHAR,
    discretion VARCHAR,
    vote_sole DOUBLE,
    vote_shared DOUBLE,
    vote_none DOUBLE
);
