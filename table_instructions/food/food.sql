create table food(
    name varchar(128) NOT NULL ,
    price numeric(4,2) NOT NULL ,
    name_start_time timestamp NOT NULL default NOW(),
    is_active BOOLEAN not null default True,
    PRIMARY KEY(name, name_start_time)
);



Alter table food_factor
add column food_name varchar(128) NOT NULL,
add column food_start_time timestamp NOT NULL default NOW(),
add FOREIGN KEY (food_name, food_start_time) REFERENCES food on delete no action;


CREATE OR REPLACE FUNCTION insert_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, action)
            VALUES(NEW.name, NEW.name_start_time, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, action)
            VALUES(NEW.name, NEW.name_start_time, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_food_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO food_log(name, name_start_time, action)
            VALUES(OLD.name, OLD.name_start_time, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_food_log_trigger AFTER INSERT ON food
    FOR EACH ROW EXECUTE PROCEDURE insert_food_log();
CREATE TRIGGER update_food_log_trigger AFTER UPDATE ON food
    FOR EACH ROW EXECUTE PROCEDURE update_food_log();
CREATE TRIGGER delete_food_log_trigger AFTER DELETE ON food
    FOR EACH ROW EXECUTE PROCEDURE delete_food_log();
