CREATE TABLE IF NOT EXISTS invoicing_data (
    id UUID PRIMARY KEY,
    order_id UUID,
    company_id UUID,
    gross_value INT,
    vat INT
);
