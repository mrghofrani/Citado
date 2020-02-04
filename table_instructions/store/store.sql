create table store(
    id serial,
    name varchar(64) not null,
    PRIMARY KEY(id)
);

alter table material
add column store int not null,
add FOREIGN KEY (store) REFERENCES store on delete cascade;

CREATE OR REPLACE FUNCTION insert_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_log(store_id, action)
            VALUES(NEW.id, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_log(store_id, action)
            VALUES(NEW.id, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_store_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO store_log(store_id, action)
            VALUES(OLD.id, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_store_log_trigger AFTER INSERT ON store
    FOR EACH ROW EXECUTE PROCEDURE insert_store_log();
CREATE TRIGGER update_store_log_trigger AFTER UPDATE ON store
    FOR EACH ROW EXECUTE PROCEDURE update_store_log();
CREATE TRIGGER delete_store_log_trigger AFTER DELETE ON store
    FOR EACH ROW EXECUTE PROCEDURE delete_store_log();
