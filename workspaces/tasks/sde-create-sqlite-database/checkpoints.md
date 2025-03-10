# Checkpoints

There are 8 checkpoints in total. Checkpoint 1's credit is granted as long as
either checkpoint 1 or checkpoint 2 passes.

## Checkpoint 1 (1pt)

Navigated to the file on owncloud.

## Checkpoint 2 (1pts)

Downloaded the `July-September 2024  Financials.ods` file.

## Checkpoint 3 (1pt)

The sqlite3 package is installed.

## Checkpoint 4 (1pt)

There is a local sqlite database with the name "financial_report.db".

## Checkpoint 5 (1pt)

The sqlite database has a table called "financial_categories" with the following columns:

- category_id
- category_name
- category_type

## Checkpoint 6 (1pt)

The sqlite database has a table called "financial_details" with the following columns:

- detail_id
- category_id
- month
- actual
- budget
- variance
- percent_of_budget

## Checkpoint 7 (1pts)

A SQL query to get the minimum variance of "Total Income" returns "2024-08" for the month, and -35000 for the variance.

## Checkpoint 8 (1pts)

A SQL query to get the sum of "actual" for the categories "Software Development" and "Consulting" for "2024-07" returns 95000.
