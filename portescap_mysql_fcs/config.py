from configparser import ConfigParser
import os, inspect

#Specifying directory and file path for config file
current_filename = inspect.getframeinfo(inspect.currentframe()).filename
print(current_filename)
parent_dir_filename = os.path.dirname(os.path.abspath(current_filename))
parent_proj_dir = os.path.dirname(parent_dir_filename)
print(parent_proj_dir)
db_config_path = os.path.join(parent_dir_filename, 'config', 'db.ini')
print(db_config_path)

def config(section, filename=db_config_path):
    # read config file
    parser = ConfigParser()
    parser.read(filename)
    # create a parser
    if section == 'db':
        return dict(host=os.environ['DB_HOST'], port=os.environ['DB_PORT'], database=os.environ['DB_DATABASE'],
                    schema=os.environ['DB_SCHEMA'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'])

    if section == 'mysql':
        return dict(host=os.environ['MYSQLDB_HOST'], port=os.environ['MYSQLDB_PORT'],
                    database=os.environ['MYSQLDB_DATABASE'],
                    user=os.environ['MYSQLDB_USER'], password=os.environ['MYSQLDB_PASSWORD'])

    if section == 'neewee_tables':
        print("GET vars", os.environ.items())
        print(os.environ['FOLDER_DATA'])
        return {'in4db_neewee': os.environ['IN_NEEWEE'], 'testsystem1_neewee': os.environ['TEST_NEEWEE']}

    if section == 'mysql_tables':
        print("GET vars", os.environ.items())
        print(os.environ['FOLDER_DATA'])
        return {'in4db_mysql': os.environ['IN_NMYSQL'], 'testsystem1_mysql': os.environ['TEST_MYSQL']}


#
# def config(section,filename=db_config_path):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)
#
#     # get section, default to postgresql
#     db = {}
#
#     # Checks to see if section (postgresql) parser exists
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#
#     # Returns an error if a parameter is called that is not listed in the initialization file
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))
#
#     return db