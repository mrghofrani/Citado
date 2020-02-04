create table material(
    name VARCHAR(64),
    price NUMERIC(4, 2) not null,
    store int not null,
    FOREIGN KEY (store) REFERENCES store on delete cascade,
    PRIMARY KEY (name)
);

alter table store_factor_material
add column material VARCHAR(64),
add FOREIGN KEY (material) REFERENCES material on delete no action;


CREATE OR REPLACE FUNCTION insert_material_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO material_log(name, action)
            VALUES(NEW.name, 'insert');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_material_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO material_log(name, action)
            VALUES(NEW.name, 'update');
            RETURN NEW;
        END;
    $$LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_material_log()
  RETURNS trigger AS $$
          BEGIN
            INSERT INTO material_log(name, action)
            VALUES(OLD.name, 'delete');
            RETURN OLD;
        END;
    $$LANGUAGE plpgsql;

CREATE TRIGGER insert_material_log_trigger AFTER INSERT ON material
    FOR EACH ROW EXECUTE PROCEDURE insert_material_log();
CREATE TRIGGER update_material_log_trigger AFTER UPDATE ON material
    FOR EACH ROW EXECUTE PROCEDURE update_material_log();
CREATE TRIGGER delete_material_log_trigger AFTER DELETE ON material
    FOR EACH ROW EXECUTE PROCEDURE delete_material_log();
