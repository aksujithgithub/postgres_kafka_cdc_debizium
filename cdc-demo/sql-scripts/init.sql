CREATE TABLE IF NOT EXISTS public.customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255)
);

INSERT INTO public.customers (first_name, last_name, email)
VALUES ('ask', 'ak', 'sak@example.com');


