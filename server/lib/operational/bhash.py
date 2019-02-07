from etc.config import Config
from lib.exceptions import OperationalException, AuthException
from lib.persistance.mysql import AuthPersistance, PostPersistance, EnqueryPersistance


class BHash:

    def hotTags(self, limit=Config.defaultResultLimit):
        db = EnqueryPersistance()
        return db.getHotTags(limit)

    def lastTags(self, limit=Config.defaultResultLimit):
        db = EnqueryPersistance()
        return db.getLastTags(limit)

    def trendTags(self, limit=Config.defaultResultLimit):
        db = EnqueryPersistance()
        return db.getTrendTags(limit, trendPast=Config.trendPast)

    def byUser(self, uid=None, username=None, limit=Config.defaultResultLimit):
        db = EnqueryPersistance()
        if uid is not None:
            return db.getLastByUid(uid, limit)
        if username is not None:
            return db.getLastByUsername(username, limit)
        raise OperationalException('A username or UID is needed')

    def byTag(self, tag, limit=Config.defaultResultLimit):
        db = EnqueryPersistance()
        return db.getLastByTag(tag, limit)

    def byId(self, id):
        db = EnqueryPersistance()
        return db.getPostById(id)

    def register(self, username, password):
        if len(username) < Config.minUsernameLen:
            raise AuthException('Username must be at least {} chr long'.format(Config.minUsernameLen))
        if len(password) < Config.minPasswordLen:
            raise AuthException('Password must be at least {} chr long'.format(Config.minPasswordLen))
        db = AuthPersistance()
        db.registerUser(username, password)

    def token(self, username, password, duration=Config.sessionLength):
        if duration is None:
            duration = Config.sessionLength
        db = AuthPersistance()
        uid = int(db.checkUser(username, password))
        if uid > 0:
            return db.getToken(uid, duration)
        raise AuthException('Auth failed')

    def publish(self, token, content, tags):
        uid = self.checkToken(token)
        db = PostPersistance()
        try:
            postid = db.savePost(uid, content)
            for tag in tags.split('#'):
                if tag.strip() == '':
                    continue
                db.saveTag(tag)
                db.savePostTag(postid, tag)
            return postid
        except:
            raise OperationalException('Unable to save content')

    def checkToken(self, token):
        db = AuthPersistance()
        uid = int(db.checkToken(token))
        if uid <= 0:
            raise OperationalException('Auth failed')
        return uid
