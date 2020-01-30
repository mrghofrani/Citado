CREATE TABLE address(
    phone char(7),
    name varchar(128) not null,
    address varchar(512) not null,
    PRIMARY KEY(phone)
);

CREATE TABLE customer(
    national_code char(10),
    first_name varchar(32) not null,
    last_name varchar(32) not null,
    mobile_number char(12) not null,
    age numeric(3,0) not null,
    PRIMARY KEY (national_code)
);

CREATE TABLE customer_address(
    customer_national_code char(10),
    address_phone char(7),
    FOREIGN KEY (customer_national_code) REFERENCES customer,
    FOREIGN KEY (address_phone) REFERENCES address
);

CREATE TABLE bike_delivery(
    national_code char(10),
    first_name varchar(32) not null,
    last_name varchar(32) not null,
    mobile_number char(12) not null,
    PRIMARY KEY (national_code)
);

CREATE TABLE food (
    name varchar(128) NOT NULL ,
    price numeric(4,2) NOT NULL ,
    name_start_time date NOT NULL ,
    name_end_time date NOT NULL ,
    price_start_time date NOT NULL ,
    price_end_time date NOT NULL ,
    PRIMARY KEY(name, name_start_time, price_start_time)
);

CREATE TABLE factor(
    id serial,
    date date,
    PRIMARY KEY (id)
);

CREATE TABLE fact_cust_add(
    factor_id int,
    address_phone char(7),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor,
    FOREIGN KEY (address_phone) REFERENCES address
);

CREATE TABLE factor_customer(
    factor_id int,
    customer_national_code char(10),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor,
    FOREIGN KEY (customer_national_code) REFERENCES customer
);

CREATE TABLE food_fact(
    factor_int int,
    food_name varchar(128),
    food_name_start_time date,
    food_price_start_time date,
    PRIMARY KEY (factor_int, food_name, food_name_start_time),
    FOREIGN KEY (factor_int) REFERENCES factor,
    FOREIGN KEY (food_name, food_name_start_time, food_price_start_time) REFERENCES food
);

CREATE TABLE delivery(
    factor_id int,
    address_phone char(7),
    bike_delivery_national_code char(10),
    PRIMARY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor,
    FOREIGN KEY (address_phone) REFERENCES address,
    FOREIGN KEY (bike_delivery_national_code) REFERENCES bike_delivery
);

CREATE TABLE store(
    name varchar(128) not null,
    start_time date not null,
    end_time date not null,
    PRIMARY KEY (name, start_time)
);

CREATE TABLE ingredient(
    name varchar(32),
    price numeric(4,2) not null,
    start_time date,
    end_time date not null,
    PRIMARY KEY (name, start_time)
);

CREATE TABLE store_ingredient(
    store_name varchar(128),
    store_start_time date,
    ingredient_name varchar(32),
    ingredient_start_time date,
    PRIMARY KEY (store_name, store_start_time, ingredient_name, ingredient_start_time),
    FOREIGN KEY (store_name, store_start_time) REFERENCES store,
    FOREIGN KEY (ingredient_name, ingredient_start_time) REFERENCES  ingredient
);

CREATE TABLE store_factor(
    factor_id int,
    store_name varchar(128),
    store_start_time date,
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor,
    FOREIGN KEY (store_name, store_start_time) REFERENCES store
);

CREATE TABLE factor_ingredient(
    factor_id int,
    ingredient_name varchar(32),
    ingredient_start_time date,
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor,
    FOREIGN KEY (ingredient_name, ingredient_start_time) REFERENCES ingredient
);

CREATE OR REPLACE FUNCTION isnumeric(text) RETURNS BOOLEAN AS $$
    DECLARE x NUMERIC;
    BEGIN
        x = $1::NUMERIC;
        RETURN TRUE;
    EXCEPTION WHEN others THEN
        RETURN FALSE;
    END;
$$
STRICT
LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION check_phone() RETURNS TRIGGER AS $$
    BEGIN
        IF isnumeric(NEW.phone) THEN
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER validate_address_phone BEFORE INSERT ON address
    FOR EACH ROW EXECUTE PROCEDURE check_phone();

CREATE OR REPLACE FUNCTION check_mobile() RETURNS TRIGGER AS $$
    BEGIN
        IF isnumeric(NEW.mobile_number) THEN
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER validate_customer_mobile_number BEFORE INSERT ON customer
    FOR EACH ROW EXECUTE PROCEDURE check_mobile();

CREATE TRIGGER validate_bike_delivery_mobile_number BEFORE INSERT ON bike_delivery
    FOR EACH ROW EXECUTE PROCEDURE check_mobile();