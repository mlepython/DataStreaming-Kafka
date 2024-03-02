UPDATE "transactions_FACT" tf
SET date_id = dd.id
FROM "date_DIM" dd
WHERE tf.date_id IS NULL AND EXTRACT(DAY FROM tf.timestamp) = dd.day AND EXTRACT(MONTH FROM tf.timestamp) = dd.month AND EXTRACT(YEAR FROM tf.timestamp) = dd.year;
