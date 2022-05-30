CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    brand TEXT,
    category TEXT,
    product_group_id TEXT,
    grammage TEXT,
    vatCode TEXT,
    rank TEXT,
    attributes TEXT,
    eanCodes TEXT
);

CREATE TABLE IF NOT EXISTS prices (
    prod_id TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    price_normal REAL NOT NULL,
    price_sale REAL,
    PRIMARY KEY (prod_id, timestamp),
    FOREIGN KEY (prod_id) REFERENCES products(id)
);

DROP VIEW IF EXISTS price_changes;
CREATE VIEW IF NOT EXISTS price_changes (
    prod_id,
    timestamp,
    week,
    price_now,
    price_last_recorded,
    price_change_from_last_recorded
) AS
SELECT
    prod_id,
    timestamp,
    CAST(strftime('%W', datetime(timestamp, 'unixepoch')) AS INTEGER) AS week,
    price_normal AS price_now,
    ( LAG(price_normal, 1, price_normal) OVER (PARTITION BY prod_id ORDER BY timestamp) ) AS price_last_recorded,
    ( price_normal - LAG(price_normal, 1, price_normal) OVER (PARTITION BY prod_id ORDER BY timestamp) ) AS price_change_from_last_recorded
FROM prices;

DROP VIEW IF EXISTS price_changes_weekly;
CREATE VIEW IF NOT EXISTS price_changes_weekly (
    prod_id,
    week,
    closing_price_last_week,
    closing_price_this_week,
    price_change_from_prev_week
) AS
SELECT DISTINCT
    prod_id,
    week,
    ( FIRST_VALUE(price_last_recorded) OVER week_window ) AS closing_price_last_week,
    ( LAST_VALUE(price_now) OVER week_window ) AS closing_price_this_week,
    ( SUM(price_change_from_last_recorded) OVER week_window ) AS price_change_from_prev_week
FROM price_changes
WINDOW week_window AS (PARTITION BY prod_id, week ORDER BY timestamp ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY prod_id, week ASC
