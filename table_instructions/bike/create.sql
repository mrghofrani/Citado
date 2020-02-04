create table bike_delivery(
    first_name VARCHAR(64) not null,
    last_name VARCHAR(64) not null,
    national_code CHAR(10) not null,
    mobile_number NUMERIC(12,0) not null,
    PRIMARY KEY(national_code)
);

Alter table factor
add column bike_delivery CHAR(10),
add FOREIGN KEY (bike_delivery) REFERENCES bike_delivery;

CREATE OR REPLACE FUNCTION insert_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, action)
            VALUES(NEW.national_code, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, action)
            VALUES(NEW.national_code, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_bike_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO bike_log(national_code, action)
            VALUES(OLD.national_code, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_bike_log_trigger AFTER INSERT ON bike_delivery
    FOR EACH ROW EXECUTE PROCEDURE insert_bike_log();
CREATE TRIGGER update_bike_log_trigger AFTER UPDATE ON bike_delivery
    FOR EACH ROW EXECUTE PROCEDURE update_bike_log();
CREATE TRIGGER delete_bike_log_trigger AFTER DELETE ON bike_delivery
    FOR EACH ROW EXECUTE PROCEDURE delete_bike_log();