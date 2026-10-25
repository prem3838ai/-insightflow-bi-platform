# Sample data dictionary

The included `data/sample/sales_data.csv` is synthetic and contains 900 transaction rows. It is generated for demonstration and should not be interpreted as real business performance.

| Field | Type | Description |
|---|---|---|
| order_id | string | Unique demo order identifier |
| order_date | ISO date | Date of transaction |
| customer_id | string | Synthetic customer identifier |
| region | category | North, South, East, West, or Central |
| sales_channel | category | Online, Retail, or Partner |
| product | category | Product name |
| category | category | Product category |
| quantity | integer | Units on the transaction row |
| unit_price | decimal | Unit price before discount |
| discount_pct | decimal | Discount fraction, e.g. 0.10 = 10% |
| revenue | decimal | Revenue after discount |
| cost | decimal | Total cost for the row |
| profit | decimal | Revenue minus cost |
