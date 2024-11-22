CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    date DATE,
    company_id UUID,
    company_name VARCHAR(255),
    crate_type VARCHAR(50),
    contact_data TEXT,
    salesowners TEXT
);
