create table Customer(
    first_name VARCHAR(64) not null,
    last_name VARCHAR(64) not null,
    national_code CHAR(10) not null,
    mobile_number NUMERIC(12,0) not null,
    age NUMERIC(3,0),
    PRIMARY KEY (national_code)
);

Alter table address
add column customer CHAR(7) not null,
add FOREIGN KEY (customer) REFERENCES Customer;

Alter table factor_customer
add column customer CHAR(7) not null,
add FOREIGN KEY (customer) REFERENCES Customer;

CREATE OR REPLACE FUNCTION insert_customer_log() RETURNS trigger AS $$
    BEGIN
        INSERT INTO customer_log(national_code, age, first_name, last_name, mobile_number, action)
        VALUES(NEW.national_code, NEW.age, NEW.first_name, NEW.last_name, NEW.mobile_number, 'insert');
        RETURN NEW;
    END;
    $$LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_customer_log() RETURNS trigger AS $$
        BEGIN
            INSERT INTO customer_log(national_code, age, first_name, last_name, mobile_number, action)
            VALUES(NEW.national_code, NEW.age, NEW.first_name, NEW.last_name, NEW.mobile_number, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_customer_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO customer_log(national_code, age, first_name, last_name, mobile_number, action)
            VALUES(OLD.national_code, OLD.age, OLD.first_name, OLD.last_name, OLD.mobile_number, 'update');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_customer_log_trigger AFTER INSERT ON customer
    FOR EACH ROW EXECUTE PROCEDURE insert_customer_log();
CREATE TRIGGER update_customer_log_trigger AFTER UPDATE ON customer
    FOR EACH ROW EXECUTE PROCEDURE update_customer_log();
CREATE TRIGGER delete_customer_log_trigger AFTER DELETE ON customer
    FOR EACH ROW EXECUTE PROCEDURE delete_customer_log();
