# Design Notes

## Core principle

All research modules should depend on a standardized holdings database, not on raw SEC files.

## Data model

The platform uses four core tables.

1. managers  
Stores institutional investment managers.

2. stocks  
Stores securities identified by CUSIP, issuer name, and later ticker.

3. filings  
Stores each 13F filing event.

4. holdings  
Stores individual positions reported in each filing.

## Why DuckDB

DuckDB is used because 13F data is analytical data. Most operations are scans, joins, grouping, sorting, and aggregation.

## Why a Database API

Research modules should not directly manipulate DuckDB connections. They should use a small database API. This makes the project easier to test and maintain.
