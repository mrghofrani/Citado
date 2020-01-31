CREATE TABLE customer(
    national_code char(10),
    first_name varchar(32) not null,
    last_name varchar(32) not null,
    mobile_number char(12) not null,
    age numeric(3,0) not null,
    PRIMARY KEY (national_code)
);

CREATE TABLE address(
    phone char(7),
    name varchar(128) not null,
    address varchar(512) not null,
    customer char(10) not null,
    PRIMARY KEY(phone),
    FOREIGN KEY (customer) REFERENCES customer
);

CREATE TABLE bike(
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

CREATE TABLE factor_of_food(
    id serial,
    date date not null,
    PRIMARY KEY (id)
);

CREATE TABLE factor_customer(
    factor_id int,
    customer_national_code char(10),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (customer_national_code) REFERENCES customer
);

CREATE TABLE factor_address(
    factor_id int,
    address_phone char(7),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (address_phone) REFERENCES address
);

CREATE TABLE food_factor(
    factor_int int,
    food_name varchar(128),
    food_name_start_time date,
    food_price_start_time date,
    quantity int not null,
    PRIMARY KEY (factor_int, food_name, food_name_start_time),
    FOREIGN KEY (factor_int) REFERENCES factor_of_food,
    FOREIGN KEY (food_name, food_name_start_time, food_price_start_time) REFERENCES food
);

CREATE TABLE delivery(
    factor_id int,
    address_phone char(7),
    bike_delivery_national_code char(10),
    PRIMARY KEY(factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (address_phone) REFERENCES address,
    FOREIGN KEY (bike_delivery_national_code) REFERENCES bike
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

CREATE TABLE factor_of_ingredient(
    id serial,
    date date not null,
    PRIMARY KEY (id)
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
    FOREIGN KEY (factor_id) REFERENCES factor_of_ingredient,
    FOREIGN KEY (store_name, store_start_time) REFERENCES store
);

CREATE TABLE factor_ingredient(
    factor_id int,
    ingredient_name varchar(32),
    ingredient_start_time date,
    quantity int not null,
    PRIMARY KEY (factor_id, ingredient_name, ingredient_start_time),
    FOREIGN KEY (factor_id) REFERENCES factor_of_ingredient,
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

CREATE TRIGGER validate_bike_delivery_mobile_number BEFORE INSERT ON bike
    FOR EACH ROW EXECUTE PROCEDURE check_mobile();


CREATE TABLE customer_log(
    national_code char(10),
    first_name varchar(32) not null,
    last_name varchar(32) not null,
    mobile_number char(12) not null,
    age numeric(3,0) not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (national_code)
);

CREATE TABLE address_log(
    phone char(7),
    name varchar(128) not null,
    address varchar(512) not null,
    customer char(10) not null,
    PRIMARY KEY(phone),
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    FOREIGN KEY (customer) REFERENCES customer
);

CREATE TABLE bike_log(
    national_code char(10),
    first_name varchar(32) not null,
    last_name varchar(32) not null,
    mobile_number char(12) not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (national_code)
);

CREATE TABLE food_log (
    name varchar(128) NOT NULL ,
    price numeric(4,2) NOT NULL ,
    name_start_time date NOT NULL ,
    name_end_time date NOT NULL ,
    price_start_time date NOT NULL ,
    price_end_time date NOT NULL ,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY(name, name_start_time, price_start_time)
);

CREATE TABLE factor_of_food_log(
    id serial,
    date date not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE factor_customer_log(
    factor_id int,
    customer_national_code char(10),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (customer_national_code) REFERENCES customer,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL
);

CREATE TABLE factor_address_log(
    factor_id int,
    address_phone char(7),
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (address_phone) REFERENCES address,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL
);

CREATE TABLE food_factor_log(
    factor_int int,
    food_name varchar(128),
    food_name_start_time date,
    food_price_start_time date,
    quantity int not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (factor_int, food_name, food_name_start_time),
    FOREIGN KEY (factor_int) REFERENCES factor_of_food,
    FOREIGN KEY (food_name, food_name_start_time, food_price_start_time) REFERENCES food
);

CREATE TABLE delivery_log(
    factor_id int,
    address_phone char(7),
    bike_delivery_national_code char(10),
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY(factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_food,
    FOREIGN KEY (address_phone) REFERENCES address,
    FOREIGN KEY (bike_delivery_national_code) REFERENCES bike
);

CREATE TABLE store_log(
    name varchar(128) not null,
    start_time date not null,
    end_time date not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (name, start_time)
);

CREATE TABLE ingredient_log(
    name varchar(32),
    price numeric(4,2) not null,
    start_time date,
    end_time date not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (name, start_time)
);

CREATE TABLE factor_of_ingredient_log(
    id serial,
    date date not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE store_ingredient_log(
    store_name varchar(128),
    store_start_time date,
    ingredient_name varchar(32),
    ingredient_start_time date,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (store_name, store_start_time, ingredient_name, ingredient_start_time),
    FOREIGN KEY (store_name, store_start_time) REFERENCES store,
    FOREIGN KEY (ingredient_name, ingredient_start_time) REFERENCES  ingredient
);

CREATE TABLE store_factor_log(
    factor_id int,
    store_name varchar(128),
    store_start_time date,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (factor_id),
    FOREIGN KEY (factor_id) REFERENCES factor_of_ingredient,
    FOREIGN KEY (store_name, store_start_time) REFERENCES store
);

CREATE TABLE factor_ingredient_log(
    factor_id int,
    ingredient_name varchar(32),
    ingredient_start_time date,
    quantity int not null,
    log_time timestamp NOT NULL default NOW(),
    action varchar(10) NOT NULL,
    PRIMARY KEY (factor_id, ingredient_name, ingredient_start_time),
    FOREIGN KEY (factor_id) REFERENCES factor_of_ingredient,
    FOREIGN KEY (ingredient_name, ingredient_start_time) REFERENCES ingredient
);

CREATE OR REPLACE FUNCTION insert_customer_log() RETURNS trigger AS $$
    BEGIN
        INSERT INTO customer_log(national_code, first_name, last_name, age, mobile_number, action)
        VALUES(NEW.national_code, NEW.first_name, NEW.last_name, NEW.age, NEW.mobile_number, 'insert');
        RETURN NEW;
    END;
    $$LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_customer_log() RETURNS trigger AS $$
        BEGIN
            INSERT INTO customer_log(national_code, first_name, last_name, age, mobile_number, action)
            VALUES(NEW.national_code, NEW.first_name, NEW.last_name, NEW.age, NEW.mobile_number, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_customer_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO customer_log(national_code, first_name, last_name, age, mobile_number, action)
            VALUES(OLD.national_code, OLD.first_name, OLD.last_name, OLD.age, OLD.mobile_number, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_customer_log_trigger AFTER INSERT ON customer
    FOR EACH ROW EXECUTE PROCEDURE insert_customer_log();
CREATE TRIGGER update_customer_log_trigger AFTER UPDATE ON customer
    FOR EACH ROW EXECUTE PROCEDURE update_customer_log();
CREATE TRIGGER delete_customer_log_trigger AFTER DELETE ON customer
    FOR EACH ROW EXECUTE PROCEDURE delete_customer_log();

CREATE OR REPLACE FUNCTION insert_address_log()
  RETURNS trigger AS $$

        BEGIN
            INSERT INTO address_log(phone, address, customer, name, action)
            VALUES(NEW.phone, NEW.address, NEW.customer, NEW.name,'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO address_log(phone, address, customer, name, action)
            VALUES(NEW.phone, NEW.address, NEW.customer, NEW.name, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO address_log(phone, address, customer, name, action)
            VALUES(NEW.phone, NEW.address, NEW.customer, NEW.name, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_customer_log_trigger AFTER INSERT ON address
    FOR EACH ROW EXECUTE PROCEDURE insert_address_log();
CREATE TRIGGER update_address_log_trigger AFTER UPDATE ON address
    FOR EACH ROW EXECUTE PROCEDURE update_address_log();
CREATE TRIGGER delete_address_log_trigger AFTER DELETE ON address
    FOR EACH ROW EXECUTE PROCEDURE delete_address_log();

CREATE OR REPLACE FUNCTION insert_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, first_name, last_name, mobile_number, action)
            VALUES(NEW.national_code,NEW.first_name, NEW.last_name, NEW.mobile_number, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, first_name, last_name, mobile_number, action)
            VALUES(NEW.national_code,NEW.first_name, NEW.last_name, NEW.mobile_number, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, first_name, last_name, mobile_number, action)
            VALUES(OLD.national_code,OLD.first_name, OLD.last_name, OLD.mobile_number, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_bike_log_trigger AFTER INSERT ON bike
    FOR EACH ROW EXECUTE PROCEDURE insert_bike_log();
CREATE TRIGGER update_bike_log_trigger AFTER UPDATE ON bike
    FOR EACH ROW EXECUTE PROCEDURE update_bike_log();
CREATE TRIGGER delete_bike_log_trigger AFTER DELETE ON bike
    FOR EACH ROW EXECUTE PROCEDURE delete_bike_log();

CREATE OR REPLACE FUNCTION insert_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, price, price_start_time, price_end_time, name_end_time, action)
            VALUES(NEW.name, NEW.name_start_time, NEW.price, NEW.price_start_time, NEW.price_end_time, NEW.name_end_time, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, price, price_start_time, price_end_time, name_end_time, action)
            VALUES(NEW.name, NEW.name_start_time, NEW.price, NEW.price_start_time, NEW.price_end_time, NEW.name_end_time, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, price, price_start_time, price_end_time, name_end_time, action)
            VALUES(OLD.name, OLD.name_start_time, OLD.price, OLD.price_start_time, OLD.price_end_time, OLD.name_end_time, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_food_log_trigger AFTER INSERT ON food
    FOR EACH ROW EXECUTE PROCEDURE insert_food_log();
CREATE TRIGGER update_food_log_trigger AFTER UPDATE ON food
    FOR EACH ROW EXECUTE PROCEDURE update_food_log();
CREATE TRIGGER delete_food_log_trigger AFTER DELETE ON food
    FOR EACH ROW EXECUTE PROCEDURE delete_food_log();


CREATE OR REPLACE FUNCTION insert_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_food_log(id, date, action)
            VALUES(NEW.id, NEW.date, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_food_log(id, date, action)
            VALUES(NEW.id, NEW.date, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_food_log(id, date, action)
            VALUES(OLD.id, NEW.date, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_factor_log_trigger AFTER INSERT ON factor_of_food
    FOR EACH ROW EXECUTE PROCEDURE insert_food_factor_log();
CREATE TRIGGER update_factor_log_trigger AFTER UPDATE ON factor_of_food
    FOR EACH ROW EXECUTE PROCEDURE update_food_factor_log();
CREATE TRIGGER delete_factor_log_trigger AFTER DELETE ON factor_of_food
    FOR EACH ROW EXECUTE PROCEDURE delete_food_factor_log();


CREATE OR REPLACE FUNCTION insert_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_factor_log(factor_int, food_name, food_name , action, quantity)
            VALUES(NEW.factor_int, NEW.food_name, NEW.food_name, 'insert', NEW.quantity);
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_factor_log(factor_int, food_name, food_name , action, quantity)
            VALUES(NEW.factor_int, NEW.food_name, NEW.food_name, 'update', NEW.quantity);
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_food_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_factor_log(factor_int, food_name, food_name , action, quantity)
            VALUES(OLD.factor_int, OLD.food_name, OLD.food_name, 'delete', OLD.quantity);
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_factor_log_trigger AFTER INSERT ON food_factor
    FOR EACH ROW EXECUTE PROCEDURE insert_food_factor_log();
CREATE TRIGGER update_factor_log_trigger AFTER UPDATE ON food_factor
    FOR EACH ROW EXECUTE PROCEDURE update_food_factor_log();
CREATE TRIGGER delete_food_factor_log_trigger AFTER DELETE ON food_factor
    FOR EACH ROW EXECUTE PROCEDURE delete_food_factor_log();


CREATE OR REPLACE FUNCTION insert_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store(name, start_time, end_time, action)
            VALUES(NEW.name, NEW.start_time, NEW.end_time ,'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store(name, start_time, end_time, action)
            VALUES(NEW.name, NEW.start_time, NEW.end_time ,'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store(name, start_time, end_time, action)
            VALUES(NEW.name, NEW.start_time, NEW.end_time ,'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_log_trigger AFTER INSERT ON store
    FOR EACH ROW EXECUTE PROCEDURE insert_store_log();
CREATE TRIGGER update_store_log_trigger AFTER UPDATE ON store
    FOR EACH ROW EXECUTE PROCEDURE update_store_log();
CREATE TRIGGER delete_store_log_trigger AFTER DELETE ON store
    FOR EACH ROW EXECUTE PROCEDURE delete_store_log();

CREATE OR REPLACE FUNCTION insert_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO ingredient_log(name, price, end_time, action)
            VALUES(NEW.name, NEW.price, NEW.end_time, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO ingredient_log(name, price, end_time, action)
            VALUES(NEW.name, NEW.price, NEW.end_time, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO ingredient_log(name, price, end_time, action)
            VALUES(OLD.name, OLD.price, OLD.end_time, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_material_log_trigger AFTER INSERT ON ingredient
    FOR EACH ROW EXECUTE PROCEDURE insert_ingredient_log();
CREATE TRIGGER update_material_log_trigger AFTER UPDATE ON ingredient
    FOR EACH ROW EXECUTE PROCEDURE update_ingredient_log();
CREATE TRIGGER delete_material_log_trigger AFTER DELETE ON ingredient
    FOR EACH ROW EXECUTE PROCEDURE delete_ingredient_log();


CREATE OR REPLACE FUNCTION insert_ingredient_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_ingredient_log(id, date, action)
            VALUES(NEW.id, NEW.date, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ingredient_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_ingredient_log(id, date, action)
            VALUES(NEW.id, NEW.date, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_ingredient_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_of_ingredient_log(id, date, action)
            VALUES(OLD.id, OLD.date, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON factor_of_ingredient
    FOR EACH ROW EXECUTE PROCEDURE insert_ingredient_factor_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON factor_of_ingredient
    FOR EACH ROW EXECUTE PROCEDURE update_ingredient_factor_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON factor_of_ingredient
    FOR EACH ROW EXECUTE PROCEDURE delete_ingredient_factor_log();


CREATE OR REPLACE FUNCTION insert_delivery_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO delivery_log(factor_id, address_phone, bike_delivery_national_code, action)
            VALUES(NEW.factor_id, NEW.address_phone, NEW.bike_delivery_national_code, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_delivery_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO delivery_log(factor_id, address_phone, bike_delivery_national_code, action)
            VALUES(NEW.factor_id, NEW.address_phone, NEW.bike_delivery_national_code, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_delivery_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO delivery_log(factor_id, address_phone, bike_delivery_national_code, action)
            VALUES(OLD.factor_id, OLD.address_phone, OLD.bike_delivery_national_code, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON delivery
    FOR EACH ROW EXECUTE PROCEDURE insert_delivery_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON delivery
    FOR EACH ROW EXECUTE PROCEDURE update_delivery_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON delivery
    FOR EACH ROW EXECUTE PROCEDURE delete_delivery_log();


CREATE OR REPLACE FUNCTION insert_factor_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_address_log(factor_id, address_phone, action)
            VALUES(NEW.factor_id, NEW.address_phone, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_factor_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_address_log(factor_id, address_phone, action)
            VALUES(NEW.factor_id, NEW.address_phone, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_factor_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_address_log(factor_id, address_phone, action)
            VALUES(OLD.factor_id, OLD.address_phone, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON factor_address
    FOR EACH ROW EXECUTE PROCEDURE insert_factor_address_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON factor_address
    FOR EACH ROW EXECUTE PROCEDURE update_factor_address_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON factor_address
    FOR EACH ROW EXECUTE PROCEDURE delete_factor_address_log();



CREATE OR REPLACE FUNCTION insert_factor_customer_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_customer_log(factor_id, customer_national_code, action)
            VALUES(NEW.factor_id, NEW.customer_national_code, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_factor_customer_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_customer_log(factor_id, customer_national_code, action)
            VALUES(NEW.factor_id, NEW.customer_national_code, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_factor_customer_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_customer_log(factor_id, customer_national_code, action)
            VALUES(OLD.factor_id, OLD.customer_national_code, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON factor_customer
    FOR EACH ROW EXECUTE PROCEDURE insert_factor_customer_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON factor_customer
    FOR EACH ROW EXECUTE PROCEDURE update_factor_customer_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON factor_customer
    FOR EACH ROW EXECUTE PROCEDURE delete_factor_customer_log();


CREATE OR REPLACE FUNCTION insert_factor_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_ingredient_log(factor_id, ingredient_name, ingredient_start_time, quantity, action)
            VALUES(NEW.factor_id, NEW.ingredient_name, NEW.ingredient_start_time, NEW.quantity, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_factor_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_ingredient_log(factor_id, ingredient_name, ingredient_start_time, quantity, action)
            VALUES(NEW.factor_id, NEW.ingredient_name, NEW.ingredient_start_time, NEW.quantity, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_factor_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO factor_ingredient_log(factor_id, ingredient_name, ingredient_start_time, quantity, action)
            VALUES(OLD.factor_id, OLD.ingredient_name, OLD.ingredient_start_time, OLD.quantity, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON factor_ingredient
    FOR EACH ROW EXECUTE PROCEDURE insert_factor_ingredient_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON factor_ingredient
    FOR EACH ROW EXECUTE PROCEDURE update_factor_ingredient_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON factor_ingredient
    FOR EACH ROW EXECUTE PROCEDURE delete_factor_ingredient_log();


CREATE OR REPLACE FUNCTION insert_store_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_factor_log(factor_id, store_name, store_start_time, action)
            VALUES(NEW.factor_id, NEW.store_name, NEW.store_start_time, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_store_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_factor_log(factor_id, store_name, store_start_time, action)
            VALUES(NEW.factor_id, NEW.store_name, NEW.store_start_time, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_store_factor_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_factor_log(factor_id, store_name, store_start_time, action)
            VALUES(OLD.factor_id, OLD.store_name, OLD.store_start_time, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON store_factor
    FOR EACH ROW EXECUTE PROCEDURE insert_store_factor_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON store_factor
    FOR EACH ROW EXECUTE PROCEDURE update_store_factor_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON store_factor
    FOR EACH ROW EXECUTE PROCEDURE delete_store_factor_log();



CREATE OR REPLACE FUNCTION insert_store_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_ingredient_log(store_name, store_start_time, ingredient_name, ingredient_start_time, action)
            VALUES(NEW.store_name, NEW.store_start_time, NEW.ingredient_name, NEW.ingredient_start_time, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_store_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_ingredient_log(store_name, store_start_time, ingredient_name, ingredient_start_time, action)
            VALUES(NEW.store_name, NEW.store_start_time, NEW.ingredient_name, NEW.ingredient_start_time, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_store_ingredient_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_ingredient_log(store_name, store_start_time, ingredient_name, ingredient_start_time, action)
            VALUES(OLD.store_name, OLD.store_start_time, OLD.ingredient_name, OLD.ingredient_start_time, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_factor_log_trigger AFTER INSERT ON store_ingredient
    FOR EACH ROW EXECUTE PROCEDURE insert_store_ingredient_log();
CREATE TRIGGER update_store_factor_log_trigger AFTER UPDATE ON store_ingredient
    FOR EACH ROW EXECUTE PROCEDURE update_store_ingredient_log();
CREATE TRIGGER delete_store_factor_log_trigger AFTER DELETE ON store_ingredient
    FOR EACH ROW EXECUTE PROCEDURE delete_store_ingredient_log();


