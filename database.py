import psycopg2


def get_connection():
    return psycopg2.connect(user="engmrgh",
                            password="h3ll9db",
                            host="localhost",
                            port="5432",
                            database="citado")


def insert(postgres_insert_query, values, table):
    connection, cursor = None, None
    result = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(postgres_insert_query, values)
        if "returning" in postgres_insert_query.lower():
            result = cursor.fetchone()[0]
        connection.commit()
        count = cursor.rowcount
        print(count, f"Record inserted successfully into {table} table")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(f"Failed to insert record into {table} table ", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return result


def update(postgres_update_query, values, table):
    connection, cursor = None, None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(postgres_update_query, values)
        connection.commit()
        count = cursor.rowcount
        print(count, f"Record Updated successfully in table {table} ")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(f"Failed to update record into {table} table ", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def query(postgres_query, table, values=tuple()):
    connection, cursor = None, None
    result = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(postgres_query, values)
        result = cursor.fetchall()
        print(f"Record Read successfully from table {table} ")
    except (Exception, psycopg2.Error) as error:
        if connection:
            print(f"Failed to fetch record from {table} table ", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return result


def delete(postgres_delete_query, values, table):
    connection, cursor = None, None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(postgres_delete_query, values)
        connection.commit()
        count = cursor.rowcount
        print(count, f"Record Deleted successfully from table {table}")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(f"Failed to update record into {table} table ", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def file_executer(file_path):
    connection, cursor = None, None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        with open(file_path) as file:
            cursor.execute(file.read())
            connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Failed to insert record into table {file_path}", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

