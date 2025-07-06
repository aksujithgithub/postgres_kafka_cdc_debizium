INSERT INTO public.customers (first_name, last_name, email)
VALUES ('aask', 'aak', 'saaak@example.com');

INSERT INTO public.customers (first_name, last_name, email)
VALUES ('adask', 'adak', 'saadak@example.com');

INSERT INTO public.customers (first_name, last_name, email)
VALUES ('aas2k', 'aa2k', 'saa1ak@example.com');


UPDATE public.customers
SET email = 'sakd1@example.com'
WHERE first_name = 'ask' AND last_name = 'ak';