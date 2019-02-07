class Config:
    def __init__(self):
        raise Exception('Use this class as static placeholder')

    #
    # CHANGE ME! You can use https://ddg.gg/?q=password+strong+32
    #
    secret = 'PWFjbh#Xd9vVgYHQf&Go5D5qJ$*ZrXz3'

    urlPrefix = ''
    sessionLength = 3600

    defaultResultLimit = 10

    # Trend (UM seconds)
    trendHeat = 600      # 10 minutes
    trendPast = 5184000  # 60 days

    minUsernameLen = 5
    minPasswordLen = 6

    gravatarDefault = 'robohash'


class DBConfig(Config):
    user = 'bhash'
    password = "bHasher"
    database = 'bhash'
    host = '127.0.0.1'

    #
    # CHANGE ME before adding users!
    # You can use https://ddg.gg/?q=password+strong+32
    #
    seed = 'B6NMyYLnDiwLfKAAp)mN$Syh'

    securityResultLimit = 1000
