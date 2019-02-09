try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
import os.path


class Config:
    safeIniSetup = '/etc/bhash.conf'

    #
    # CHANGE ME!
    # default values will be overridden from Config.safeIniSetup
    # You can use https://ddg.gg/?q=password+strong+32
    #
    secret = 'this-seed-add-noise-on-session-keys'

    urlPrefix = ''
    sessionLength = 3600

    defaultResultLimit = 10

    # Trend (UM seconds)
    trendHeat = 600      # 10 minutes
    trendPast = 5184000  # 60 days

    minUsernameLen = 5
    minPasswordLen = 6

    gravatarDefault = 'robohash'
    gravatarFakeDomain = 'nowhere.org'

    def __init__(self):
        raise Exception('Use this class as static placeholder')


class DBConfig(Config):
    # default values will be overridden from Config.safeIniSetup
    user = 'bhash'
    password = "CHANGEME"
    database = 'bhash'
    host = '127.0.0.1'

    #
    # CHANGE ME before adding users!
    # You can use https://ddg.gg/?q=password+strong+32
    #
    seed = 'this-seed-add-noise-on-password-storage'

    securityResultLimit = 1000


if os.path.isfile(Config.safeIniSetup):
    config = ConfigParser()

    config.read(Config.safeIniSetup)

    Config.secret = config.get('seeds', 'session')
    DBConfig.seed = config.get('seeds', 'auth')

    DBConfig.user = config.get('db', 'user')
    DBConfig.password = config.get('db', 'password')
    DBConfig.name = config.get('db', 'name')
    DBConfig.host = config.get('db', 'host')
