CREATE TABLE IF NOT EXISTS public.customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255)
);

INSERT INTO public.customers (first_name, last_name, email)
VALUES ('ask', 'ak', 'sak@example.com');

UPDATE public.customers
SET email = 'sak1@example.com'
WHERE first_name = 'ask' AND last_name = 'ak';

DELETE FROM public.customers
WHERE first_name = 'ask' AND last_name = 'ak';
