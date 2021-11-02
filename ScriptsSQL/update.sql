 update personal_data set height = 180, weight = 77 where id = 2;

DROP TABLE public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id          SERIAL      NOT NULL,
    login       TEXT        NOT NULL UNIQUE,
    password    TEXT        NOT NULL,
    user_status VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
);
