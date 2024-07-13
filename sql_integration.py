import os
import os.path
from time import sleep
try:
    import mysql.connector
    from mysql.connector import Error
except ModuleNotFoundError:
    os.system('wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-py3_8.2.0-1debian12_amd64.deb')
    os.system('apt install ./mysql-connector-python-py3_8.2.0-1debian12_amd64.deb -y')
    os.system('rm mysql-connector-python-py3_8.2.0-1debian12_amd64.deb')
    import mysql.connector
    from mysql.connector import Error
#import cx_Oracle


class UnknownAliasError(Exception):
    def __init__(self, message):
        self.message = message


class utils:
    def list_dir(dir):
        list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        return list
    

    def clear_data():
        list = utils.list_dir('./data')
        for i in range(len(list)):
            os.remove(f'./data/{list[i]}')


    def create_data_folder():
        try:
            os.makedirs('./data')
        except FileExistsError:
            pass


class basic_sql:
    def execute_query(connection, query):
        print('started executing query')
        cursor = connection.cursor(buffered=True, dictionary=True)

        try:
            debug = True
            cursor.execute(query)
            if 'SELECT' not in query.upper():
                connection.commit()
                print('INSERTED SUCCESSFULLY')
                return True
            else:
                if debug == True:
                    print(f'execute_query query: {query}')
                results = str(cursor.fetchall()).replace('}, {', '\n').replace('}]', '').replace('[{', '').replace("'", '')
                if debug == True:
                    print(f'execute_query results: {results}')
                results = results.split('\n')
                results_modified = []
                for i in range(len(results)):
                    if debug == True:
                        print('Pass 1')
                    results2 = results[i]
                    results2 = results2.split(', ')
                    results2_modified = ''
                    for j in range(len(results2)):
                        if debug == True:
                            print('Pass 2')
                        results3 = results2[j]
                        results3 = (results3.split(': '))[1]
                        if j == 0:
                            results2_modified = results2_modified + results3
                        else:
                            results2_modified = results2_modified + ', ' + results3
                        if debug == True:
                            print('Pass 3')
                    if i != len(results):
                        results2_modified = results2_modified
                    results_modified.append(results2_modified)
                results = results_modified
                print(f'sql_integration_query result: {results}')
                return results
            print("Query executed successfully")   

        except Exception as e:
            print(f"Error executing query: {e}")

        finally:
            print("Closing cursor and connection")
            cursor.close()
            connection.close()


    def create_connection(host_name, user_name, user_password, db_name):
        print('Creating connection with DB')
        if db_name == None:
            connection = None
            try:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password
                )
                print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")
            return connection
        
        else:
            connection = None
            try:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    database=db_name
                )
                print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")
            return connection


class oracle_sql:
    def __init__(self):
        utils.create_data_folder()
        oracle_sql.get_tnsnames()
        oracle_sql.read_tnsnames()


    def get_tnsnames():
        def get_file(path):
            file = open(path, 'r').readlines()
            return file
        

        def exclude_useless(file):
            tnsnames = ''
            for i in range(len(file)):
                line = file[i]
                # exclude comments
                line = (line.split('#'))[0]
                # replace useless characters
                line = line.replace(' ', '').replace('\n', '')
                # skip blank line
                if line != '':
                    tnsnames = tnsnames + line + '\n'
                
                # remove return line char
                tnsnames = tnsnames.split('\n')
                var = ''
                for i in range(len(tnsnames)):
                    line = tnsnames[i]
                    var = var + line.replace('\n', '')
                tnsnames = var
            return tnsnames


        def reformat_in_list(file):
            # reformat in list
            tnsnames = [*file]
            status = 0
            str = ''
            list = []
            for i in range(len(tnsnames)):
                char = tnsnames[i]
                if char == '(':
                    status += 1
                    if str != '':
                        list.append(str)
                    str = ''
                elif char == ')':
                    status -= 1
                    if str != '':
                        list.append(str)
                    if status == 0:
                        list.append('\n')
                    str = ''
                else:
                    str += char
            return list


        def add_delimiter(file):
            tnsnames = ''
            for i in range(len(file)):
                if '\n' not in file[i]:
                    file[i] += ','
                tnsnames += file[i]
            return tnsnames
        

        def remove_useless_delimiter(file):
            tnsnames = file.split('\n')
            str = ''
            for i in range(len(tnsnames)):
                line = tnsnames[i]
                line = line.split(',')
                new_line = ''
                for j in range(len(line)):
                    item = line[j]
                    if item != '':
                        if j != len(line)-2:
                            delimiter = ','
                        else:
                            delimiter = ''
                        new_line += item + delimiter                   
                new_line += '\n'
                str += new_line
            return str


        def format_in_csv(file):
            tnsnames = file.split('\n')
            str = ''
            for i in range(len(tnsnames)):
                line = tnsnames[i]
                line = line.split(',')
                new_line = ''
                for j in range(len(line)):
                    item = line[j]
                    if item != '':
                        if j == 0:
                            item = 'ALIAS='+(item.split('='))[0]
                        if j != len(line)-1:
                            delimiter = ','
                        else:
                            delimiter = ''
                        new_line += item + delimiter
                str += new_line + '\n'
            return str


        def remove_useless_data_in_csv(file):
            tnsnames = file.split('\n')
            for i in range(len(tnsnames)):
                tnsnames[i] = tnsnames[i].replace(
                    'DESCRIPTION=,',
                    '').replace(
                        'ADDRESS=,', 
                        '').replace(
                            'ADDRESS_LIST=,',
                            '').replace(
                                'CONNECT_DATA=,', 
                                '') + '\n'
            return tnsnames
        

        def create_csv(file):
            open('./data/tnsnames.csv', 'w').writelines(file)


        oracle_path = (open('oracle.conf', 'r').readline()).replace('\n', '')
        file = get_file(oracle_path)
        file = exclude_useless(file)
        file = reformat_in_list(file)
        file = add_delimiter(file)
        file = remove_useless_delimiter(file)
        file = format_in_csv(file)
        file = remove_useless_data_in_csv(file)
        create_csv(file)
        

    def read_tnsnames():
        global tns_alias
        global tns_protocol
        global tns_host
        global tns_port
        global tns_server
        global tns_service_name


        tns_alias = []
        tns_protocol = []
        tns_host = []
        tns_port = []
        tns_server = []
        tns_service_name = []

        file = open('./data/tnsnames.csv', 'r').readlines()
        
        for i in range(len(file)):
            line = (file[i]).replace('\n', '')
            if line != '\n':
                line = line.split(',')
                for j in range(len(line)):
                    item = line[j]
                    if 'ALIAS' in item:
                        tns_alias.append((item.split('='))[1])
                    elif 'PROTOCOL' in item:
                        tns_protocol.append((item.split('='))[1])
                    elif 'HOST' in item:
                        tns_host.append((item.split('='))[1])
                    elif 'PORT' in item:
                        tns_port.append((item.split('='))[1])
                    elif 'SERVER' in item:
                        tns_server.append((item.split('='))[1])
                    elif 'SERVICE_NAME' in item:
                        tns_service_name.append((item.split('='))[1])
        
        utils.clear_data()


    def get_info(alias):
        oracle_sql()
        for i in range(len(tns_alias)):
            if alias in tns_alias[i]:
                info = [tns_alias[i], 
                        tns_protocol[i], 
                        tns_host[i], 
                        tns_port[i], 
                        tns_server[i], 
                        tns_service_name[i]]
        if len(info) == 0:
            raise UnknownAliasError(f'{alias} IS NOT IN THE TNSNAMES.')
        return info


    def request(request, alias, user, password):
        info = oracle_sql.get_info(alias)
        alias = info[0]
        host = info[2]
        port = info[3]
        service_name = info[5]

        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name) # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

        c = conn.cursor()
        c.execute(request) # use triple quotes if you want to spread your query across multiple lines
        result = []
        for row in c:
            var = ''
            for i in range(len(row)):
                if i == 0:
                    delimiter = ''
                else:
                    delimiter = ','
                var = var + delimiter + str(row[i])
            result.append(var + '\n')
        conn.close()
        open('results.csv', 'w').writelines(result)
        return result
