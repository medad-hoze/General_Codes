


import pandas as pd
import pyodbc


def get_sql_cursor( server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):

    # Create the connection string
    conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}; Trusted_Connection=yes"

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
        sql += "\n\t{} {}{},".format(column_name,datatype,constraint)

    # Add the closing parenthesis
    sql += "\n);"

    return sql

def str_to_sql(i):
    if isinstance(i,str) or i.__class__.__name__ == 'Timestamp':
        i = str(i).replace("'","")
        return f"'{i}'"
    elif str(i) == 'nan':
        return '0'
    else:
        return str(int(i))

def create_SQL_table(df,table_name, server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):

    if 'TZ' in  df.columns:
        df.drop('TZ',axis = 1,inplace = True)
        


    conn,cursor = get_sql_cursor(server, database , username , password )
    dict_types  = {'int64':'NUMERIC','object':'VARCHAR(255)','float64':'REAL',\
                   'int32':'NUMERIC','<M8[ns]':'VARCHAR(255)','datetime64[ns]':'VARCHAR(255)'}

    df.columns  = df.columns.str.replace("[#,@,&,',' ']", '')
    columns     = ['name_' + str(i) for i in list(df.columns) if str(i).isdigit()]
    columns     = dict(zip(list(df.columns),columns))

    df.rename(columns =columns,inplace = True)

    dict_col_type = [(col_name,dict_types[str(type_)]) 
                    for col_name, type_ in df.dtypes.to_dict().items()]

    key_     = dict_col_type[0]
    data     = [i + (" NULL",) for i in dict_col_type[1:]]
    col_data = [(key_[0],'INT'," PRIMARY KEY IDENTITY(1,1)")]

    col_data.extend(data[0:])

    sql      = create_table_template(table_name, col_data)

    try:
        cursor.execute(sql)
        print ('Created table')
        cursor.commit()
    except:
        print ('Table already exist')
    conn.close()


def insert_to_SQL(df,table_name, server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):

    conn,cursor = get_sql_cursor(server, database , username , password )

    varlist  = df.values.tolist()

    num_of_col = len(df.columns)
    num_val    = len(varlist[0])
    if num_of_col != num_val:
        print ('Number of columns is not equal to number of values')
        return

    col_insert =  ', '.join(df.columns.to_list())

    print (col_insert)

    cursor.execute(f'SET IDENTITY_INSERT {table_name} ON')
    cursor.commit()


    for item in varlist:
        all_temp = '('
        for i in item:
            print (i)
            temp =  str_to_sql(i) + ","
            all_temp += temp
        all_temp = all_temp[:-1] + ')'

        query = f"INSERT into {table_name} ({col_insert}) VALUES {all_temp}"
        cursor.execute(query)
        cursor.commit()
    conn.close()



df_1 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\GviaToshavim.xlsx"     )
df_2 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\InteriorToshavim.xlsx" )
df_3 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\RevahaToshavim.xlsx"   )
df_4 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\SchoolToshavim.xlsx"   )



# create_SQL_table (df_1,'GviaToshavim')
# insert_to_SQL    (df_1,'GviaToshavim')



# create_SQL_table (df_2,'InteriorToshavim')
# insert_to_SQL    (df_2,'InteriorToshavim')

# create_SQL_table (df_3,'RevahaToshavim'  )
# insert_to_SQL    (df_3,'RevahaToshavim')

# create_SQL_table (df_4,'SchoolToshavim'  )
# insert_to_SQL    (df_4,'SchoolToshavim')


conn,cursor = get_sql_cursor()

df_GviaToshavim     = get_data(cursor,'GviaToshavim')
df_InteriorToshavim = get_data(cursor,'InteriorToshavim')
df_RevahaToshavim   = get_data(cursor,'RevahaToshavim')
df_SchoolToshavim   = get_data(cursor,'SchoolToshavim')



print (df_GviaToshavim)
print (df_InteriorToshavim)
print (df_RevahaToshavim)
print (df_SchoolToshavim)