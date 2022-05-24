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

CREATE VIEW IF NOT EXISTS price_changes_from_last_recorded (
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
        
CREATE VIEW IF NOT EXISTS price_changes_weekly (
    prod_id,
    week,
    price_change_from_prev_week
) AS
SELECT
    prod_id,
    week,
    SUM(price_change_from_last_recorded) AS price_change_from_prev_week
FROM price_changes_daily
GROUP BY prod_id, week;
