import ConfigParser
import os
    
config = ConfigParser.ConfigParser()

configFile=os.path.join(os.path.dirname(os.path.realpath(__file__)),"settings.cfg")
config.read(configFile)



DBDRIVER = config.get('postgresql', 'dbdriver')
HOST = config.get('postgresql', 'host')
PORT = int(config.get('postgresql', 'port'))
SCHEMA = config.get('postgresql', 'schema')
DBNAME = config.get('postgresql', 'dbname')
USERNAME = config.get('postgresql', 'username')
PASSWORD = config.get('postgresql', 'password')


#==============================================================================================================================         
def write(**kwargs):
    """Write Settings for database"""     
      
    if kwargs is not None:
            for key, value in kwargs.iteritems():
                config.set('postgresql', key, value)
    with open(configFile, 'wb') as configfile:
            config.write(configfile)