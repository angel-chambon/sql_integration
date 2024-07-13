How to use sql_integration step by step:

0- Import the module:
from path_to_module_folder.sql_integration.sql_integration import *

FOR THE BASIC SQL :
    1- Connect to database using:
    connection = create_connection(database, user, password, shema)

    2- Set your query:
    table = exemple_table
    query = f"""
    SELECT * FROM
    {table}
    ;
    """

    3- Execute your query:
    execute_query(connection, query)  


    Its simple :D

FOR ORACLE SQL WITH ODBC DRIVER (tnsnames.ora):
    1- SET UP THE PATH OF THE tnsnames.ora DIRECTLY IN THE oracle.conf
    2- YOU CAN USE THE FUNCTION oracle_sql.get_info(alias) TO RETURN DATA OF THE ODBC DRIVER IN LIST FORM :
        2.1 THE FORMAT OF THE LIST : [alias, protocol, host, port, server, service_name]
    3- YOU CAN USE THE FUNCTION oracle_sql.request(request, alias, user, password) TO EXECUTE SQL REQUEST WITH ALIAS
        3.1- WHEN YOU USE THE REQUEST FUNCTION, THE GET_INFO FUNCTION IS DIRECTLY USE, NO NEED TO CALL IT BEFORE.

Enjoy !
