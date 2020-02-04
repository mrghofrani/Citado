create table Address(
    id serial,
	name VARCHAR(64),
    address VARCHAR(128) not null,
    phone_number NUMERIC(7,0) not null,
    customer CHAR(10) not null,
    FOREIGN KEY (customer) REFERENCES Customer,
    PRIMARY KEY (id)
);

alter table factor
add column address int,
add FOREIGN KEY(address) REFERENCES address on delete set null;


CREATE OR REPLACE FUNCTION insert_address_log()
  RETURNS trigger AS $$

        BEGIN
            INSERT INTO address_log(address_id, action)
            VALUES(NEW.id, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO address_log(address_id, action)
            VALUES(NEW.id, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_address_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO address_log(address_id, action)
            VALUES(OLD.id, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_customer_log_trigger AFTER INSERT ON address
    FOR EACH ROW EXECUTE PROCEDURE insert_address_log();
CREATE TRIGGER update_address_log_trigger AFTER UPDATE ON address
    FOR EACH ROW EXECUTE PROCEDURE update_address_log();
CREATE TRIGGER delete_address_log_trigger AFTER DELETE ON address
    FOR EACH ROW EXECUTE PROCEDURE delete_address_log();
