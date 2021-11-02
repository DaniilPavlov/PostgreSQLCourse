drop table if exists who, drugs, part, part_drug, troubles, sale, sale_drug, to_consumer, relation;
create table if not exists who
(
    who_id   serial PRIMARY KEY,
    who_name varchar(100) NOT NULL
);

create table if not exists troubles
(
    trouble_id   serial PRIMARY KEY,
    trouble_name text NOT NULL
);

create table if not exists sale
(
    sale_id   serial PRIMARY KEY,
    sale_name varchar(100) NOT NULL
);


create table if not exists drugs
(
    drug_id       serial PRIMARY KEY,
    drug_name     varchar(50) NOT NULL,
    drug_who      int         NOT NULL,
    drug_troubles int         NULL,
    drug_sale     int         NOT NULL,
    constraint fb2
        FOREIGN KEY (drug_who)
            REFERENCES who (who_id),
    constraint fb3
        FOREIGN KEY (drug_troubles)
            REFERENCES troubles (trouble_id),
    constraint fb4
        FOREIGN KEY (drug_sale)
            REFERENCES sale (sale_id)
);


create table if not exists sale_drug
(
    sale_drug_id serial PRIMARY KEY,
    sale         int NOT NULL,
    drug         int NOT NULL,
    sales_now    int NOT NULL,
    constraint fb1
        FOREIGN KEY (sale)
            REFERENCES sale (sale_id),
    constraint fb2
        FOREIGN KEY (drug)
            REFERENCES drugs (drug_id)
);


create table if not exists part
(
    part_id   serial PRIMARY KEY,
    part_name varchar(100) NOT NULL
);

create table if not exists part_drug
(
    part_drag_id serial PRIMARY KEY,
    part         int  not null,
    drug         int  not null,
    date_end     date not null,
    constraint fb1
        FOREIGN KEY (drug)
            REFERENCES drugs (drug_id),

    FOREIGN KEY (part)
        REFERENCES part (part_id)
);


create table if not exists to_consumer
(
    to_consumer_id serial PRIMARY KEY,
    drug           int  NOT NULL,
    date_to        date NOT NULL,
    constraint fb1
        FOREIGN KEY (drug)
            REFERENCES part_drug (part_drag_id)
);

create table if not exists relation
(
    relation_id serial primary key,
    drug1       int not null,
    drug2       int not null,
    norm        int not null,
    constraint fb1
        FOREIGN KEY (drug1)
            REFERENCES drugs (drug_id),
    constraint fb2
        FOREIGN KEY (drug2)
            REFERENCES drugs (drug_id)
)

