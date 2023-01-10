




import pandas as pd
import pyodbc



def get_sql_cursor( server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):

    # Create the connection string
    conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

    # Connect to the SQL server
    conn   = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return conn,cursor



def get_data(cursor,tbl_name):
    # Execute the query
    cursor.execute("SELECT * FROM {}".format(tbl_name))

    rows = cursor.fetchall()
    df   = pd.DataFrame.from_records(rows)

    return df


def create_table_template(table_name, column_data):
    # Start building the SQL statement
    sql = "CREATE TABLE {} (".format(table_name)

    # Add the column names and datatype to the SQL statement
    for column_name, datatype, constraint in column_data:
        sql += "\n\t{} {}{}".format(column_name,datatype,constraint)

    # Add the closing parenthesis
    sql += "\n);"

    return sql



conn,cursor = get_sql_cursor()


df = get_data(cursor,'catch2017')

print (df)

column_data = [("ID", "INT"," PRIMARY KEY IDENTITY(1,1)"), 
              ("Name", "VARCHAR(255)"," NOT NULL"), 
              ("Email", "VARCHAR(255)"," NOT NULL UNIQUE"), 
              ("Phone", "VARCHAR(15)"," NOT NULL")]

sql = create_table_template("Customers", column_data)
print(sql)


# print (tsql_tamplate)

# sql = """
# CREATE TABLE Customers (
#     ID INT PRIMARY KEY IDENTITY(1,1),
#     Name VARCHAR(255) NOT NULL,
#     Email VARCHAR(255) NOT NULL UNIQUE,
#     Phone VARCHAR(15) NOT NULL
# );
# """



# cursor.execute(tsql_tamplate)

# # Commit the transaction
# conn.commit()

# # Close the connection
# conn.close()
