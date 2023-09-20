
import configparser
config = configparser.ConfigParser()
config['Token'] = {'access_token': ''}
with open('config.ini', 'w') as configfile:
    config.write(configfile)