# -*- coding: utf-8 -*-


import pandas as pd
import pyodbc
import arcpy,os

arcpy.env.overwriteOutput = True


def get_sql_cursor( server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):

    # Create the connection string
    conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}; Trusted_Connection=yes"

    # Connect to the SQL server
    conn   = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return conn,cursor


def get_data(cursor,tbl_name):
    # Execute the query

    cursor.execute(f"SELECT * FROM {tbl_name}")
    columns = [column[0] for column in cursor.description]
 
    cursor.execute("SELECT * FROM {}".format(tbl_name))
    rows = cursor.fetchall()
    df   = pd.DataFrame.from_records(rows,columns = columns)

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
        if len(i)> 0:
            return f"'{i}'"
        return "'null'"
    elif str(i) == 'nan':
        return '0'
    elif isinstance(i,tuple):
        return "'" + str(i) + "'"
    else:
        return str(int(i))

def create_SQL_table(df,table_name, server = 'MEDADHOZE-LAP\SQLEXPRESS', database = 'test', username = '', password = ''):


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
    cursor.execute(f'DROP TABLE {table_name}')

    cursor.execute(sql)
    print ('Created table')
    cursor.commit()

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

    cursor.execute(f'SET IDENTITY_INSERT {table_name} ON')
    cursor.commit()

    try:
        cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN SHAPEWKT NVARCHAR(4000)")
        cursor.commit()
    except:
        pass

    num_error = 0
    for item in varlist:
        all_temp = '('
        for i in item:
            temp =  str_to_sql(i) + ","
            all_temp += temp
        all_temp = all_temp[:-1] + ')'

        try:
            query = f"INSERT into {table_name} ({col_insert}) VALUES {all_temp}"
            cursor.execute(query)
            cursor.commit()
        except:
            num_error += 1
            pass
    

    print ('Number of rows that didnt enter the database: {}'.format(num_error))
    print ('can be cause because double key value or geometry is to big')

    conn.close()



def Read_Fc(addr,num_rows = 9999999):

    print ("read: Read Fc")
    columns = [f.name for f in arcpy.ListFields(addr) if f.name not in ('SHAPE','Shape')] + ['SHAPE@WKT']
    df       = pd.DataFrame(data = [row for row in arcpy.da.SearchCursor\
               (addr,columns,"\"OBJECTID\" < {}".format(num_rows))],columns = columns)

    return df



def Create_Layer_from_df(merge,New_layer):

    print ("Create Later from df")
    print ("total rows: {}".format(str(merge.shape[0])))

    columns          = list(merge.columns)
    

    list_            = merge.values.tolist()

    dict_type = {'MULTIPOLYGON':'POLYGON','POINT':'POINT','LINE':'POLYLINE','POLYLINE':'POLYLINE'}

    if  'SHAPEWKT' in columns:
        geom_type = merge['SHAPEWKT'].tolist()[0]
        geom_type = ''.join([x for x in geom_type if x.isalpha()])
        geom = dict_type[geom_type]


    gdb_proc,fc_name = os.path.split(New_layer)
    Fc_rimon         = arcpy.CreateFeatureclass_management (gdb_proc, fc_name, geom)

    dict_types = {'int64':'LONG','object':'TEXT','float64':'DOUBLE',\
                  'int32':'SHORT','<M8[ns]':'DATE','datetime64[ns]':'DATE'}

    dict_col_type = {col_name:dict_types[str(type_)] for col_name, type_ in merge.dtypes.to_dict().items()}

    for i in columns:
        if i not in ('OBJECTID','SHAPEWKT'):
            arcpy.AddField_management(Fc_rimon,i,dict_col_type[i])


    columns = [i for i in columns if i != 'SHAPEWKT']
    columns = columns + ['SHAPE@']
    in_rows = arcpy.da.InsertCursor(Fc_rimon,columns)


    for i in list_:
        if str(i[-1]) != 'nan':
            in_rows.insertRow (i[:-1] + [arcpy.FromWKT(str(i[-1]))])
        else:
            in_rows.insertRow (i[:-1] + [None])



def Create_Table_from_df(merge,New_layer):

    print ("Create Table from df")
    print ("total Assets: {}".format(str(merge.shape[0])))

    columns          = list(merge.columns)
    gdb_proc,fc_name = os.path.split(New_layer)

    Fc_rimon = arcpy.CreateTable_management(gdb_proc, fc_name)

    dict_types = {'int64':'LONG','object':'TEXT','float64':'DOUBLE',\
                  'int32':'SHORT','<M8[ns]':'DATE','datetime64[ns]':'DATE'}

    dict_col_type = {col_name:dict_types[str(type_)] for col_name, type_ in merge.dtypes.to_dict().items()}

    for i in columns:arcpy.AddField_management(Fc_rimon,i,dict_col_type[i])

    in_rows = arcpy.da.InsertCursor(Fc_rimon,columns)
    list_   = merge.values.tolist()
    for i in list_:in_rows.insertRow (i)
    del in_rows


layer     = r'C:\Users\Administrator\Desktop\ArcpyToolsBox\test\New File Geodatabase.gdb\Parcels2D'
New_layer = layer + '_new'

df        = Read_Fc(layer)

create_SQL_table (df,'tryme')
insert_to_SQL    (df,'tryme')

conn,cursor = get_sql_cursor()
df2         = get_data(cursor,'tryme')

Create_Layer_from_df(df2,New_layer)

# Create_Table_from_df(df2,New_layer)







# df_1 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\GviaToshavim.xlsx"     )
# df_2 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\InteriorToshavim.xlsx" )
# df_3 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\RevahaToshavim.xlsx"   )
# df_4 = pd.read_excel(r"C:\Users\Administrator\Desktop\medad\Previous_work\nadav\SchoolToshavim.xlsx"   )


# create_SQL_table (df_1,'GviaToshavim')
# insert_to_SQL    (df_1,'GviaToshavim')

# create_SQL_table (df_2,'InteriorToshavim')
# insert_to_SQL    (df_2,'InteriorToshavim')

# create_SQL_table (df_3,'RevahaToshavim'  )
# insert_to_SQL    (df_3,'RevahaToshavim')

# create_SQL_table (df_4,'SchoolToshavim'  )
# insert_to_SQL    (df_4,'SchoolToshavim')


# conn,cursor = get_sql_cursor()

# df_GviaToshavim     = get_data(cursor,'GviaToshavim')
# df_InteriorToshavim = get_data(cursor,'InteriorToshavim')
# df_RevahaToshavim   = get_data(cursor,'RevahaToshavim')
# df_SchoolToshavim   = get_data(cursor,'SchoolToshavim')



# ['IntID', 'TZ', 'FName', 'LName', 'Gender', 'STREET_COD', 'STREET_NAME','HouseNum', 'Floor', 'Appt', 'Tel', 'Mobile', 'eMail', 'MStatusCode','MStatus', 'SpouseTZ', 'FatherTZ', 'MotherTZ', 'BDate', 'Active']



# df_RevahaToshavim['FName'] = df_RevahaToshavim['FullName'].apply(lambda x: x.split(' ')[0])
# df_RevahaToshavim['LName'] = df_RevahaToshavim['FullName'].apply(lambda x: x.split(' ')[1])

# dict_colums = {'IDKEY':'IntID','HouseNumber':'HouseNum'}
# df_RevahaToshavim.rename(columns =dict_colums,inplace = True)


# result = pd.concat([df_GviaToshavim,  df_RevahaToshavim], axis=0)

# # print (result)

# print (df_GviaToshavim.columns)

# print (df_InteriorToshavim.columns)

# print (df_SchoolToshavim.columns)





# print (df_GviaToshavim.shape[1])
# print (df_InteriorToshavim.shape[1])
# print (df_RevahaToshavim.shape[1])
# print (df_SchoolToshavim.shape[1])




# print (result)
# result.drop_duplicates(subset='A', keep='first', inplace=True)

