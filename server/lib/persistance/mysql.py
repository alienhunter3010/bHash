import uuid
import mysql.connector
from etc.config import DBConfig
from lib.exceptions import AuthException


class Persistance:
    def __init__(self):
        self.cnx = mysql.connector.connect(user=DBConfig.user,
                                           password=DBConfig.password,
                                           host=DBConfig.host,
                                           database=DBConfig.database)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()

    def keepQuery(self, query, arguments):
        cursor = self.cnx.cursor()
        cursor.execute(query, arguments)
        return cursor

    def doQuery(self, query, arguments):
        cur = self.keepQuery(query, arguments)
        self.cnx.commit()
        cur.close()

    def insertQuery(self, query, arguments):
        cur = self.keepQuery(query, arguments)
        try:
            return cur.lastrowid
        finally:
            self.cnx.commit()
            cur.close()


class EnqueryPersistance(Persistance):
    postData = 'SELECT bh_posts.id AS bh_post, bh_user, username,' \
               ' MD5(LOWER(TRIM(email))) AS gravatar, content, bh_posts.created' \
               ' FROM bh_posts INNER JOIN bh_users ON bh_posts.bh_user=bh_users.id'

    def getTags(self, query, limit, additional=None):
        filters = []
        if additional is not None:
            filters.append(additional)
        filters.append(min(limit, DBConfig.securityResultLimit))
        cur = self.keepQuery(query, filters)

        result = []
        try:
            for tag in cur:
                result.append(tag[0])
        finally:
            cur.close()
        return result

    def getPosts(self, query, qfilter=None, limit=DBConfig.securityResultLimit):
        limit = min(limit, DBConfig.securityResultLimit)
        filters = (limit,) if qfilter is None else (qfilter, limit)
        cur = self.keepQuery(query, filters)

        posts = []
        try:
            for (bh_post, bh_user, username, gravatar, content, created) in cur:
                posts.append({'id': bh_post, 'username': username, 'content': content, 'created': str(created),
                              'owner': bh_user, 'gravatar': gravatar})
        finally:
            cur.close()

        for post in posts:
            post['tags'] = self.getPostTags(post['id'])
        return posts

    def getHotTags(self, limit=DBConfig.defaultResultLimit):
        query = "SELECT tag FROM bh_tags ORDER BY hot DESC LIMIT %s"
        return self.getTags(query, limit)

    def getLastTags(self, limit=DBConfig.defaultResultLimit):
        query = "SELECT tag FROM bh_tags ORDER BY lastUsed DESC LIMIT %s"
        return self.getTags(query, limit)

    def getTrendTags(self, limit=DBConfig.defaultResultLimit, trendPast=DBConfig.trendPast):
        query = "SELECT tag FROM bh_tags WHERE lastTrend > SUBDATE(NOW(), INTERVAL %s SECOND)" \
                " ORDER BY hot DESC LIMIT %s"
        return self.getTags(query, limit, additional=trendPast)

    def getPostTags(self, postid):
        query = "SELECT bh_tag AS tag FROM bh_posts_tags WHERE bh_post=%s"
        return self.getTags(query, postid)

    def getLastByUid(self, uid, limit=DBConfig.defaultResultLimit):
        query = self.postData + " WHERE bh_user=%s ORDER BY bh_posts.created DESC LIMIT %s"
        return self.getPosts(query, uid, limit)

    def getLastByUsername(self, username, limit=DBConfig.defaultResultLimit):
        query = self.postData + " WHERE username=%s ORDER BY bh_posts.created DESC LIMIT %s"
        return self.getPosts(query, username, limit)

    def getLastByTime(self, limit=DBConfig.defaultResultLimit):
        query = self.postData + " ORDER BY bh_posts.created DESC LIMIT %s"
        return self.getPosts(query, limit=limit)

    def getLastByTag(self, tag, limit=DBConfig.defaultResultLimit):
        query = self.postData + " INNER JOIN bh_posts_tags ON bh_posts_tags.bh_post=bh_posts.id" \
                                " WHERE bh_tag=%s ORDER BY bh_posts.created DESC LIMIT %s"
        return self.getPosts(query, tag, limit)

    def getPostById(self, postid):
        query = self.postData + " WHERE bh_posts.id=%s LIMIT %s"
        return self.getPosts(query, postid, 1)


class AuthPersistance(Persistance):
    def registerUser(self, login, password, email=None):
        if email is None:
            email = '{}@{}'.format(login, DBConfig.gravatarFakeDomain)
        query = "INSERT INTO bh_users SET username=%s, password=MD5(CONCAT(%s, %s)), email=%s"
        self.doQuery(query, (login, DBConfig.seed, password, email))

    def checkUser(self, login, password):
        query = "SELECT id FROM bh_users WHERE username=%s AND password=MD5(CONCAT(%s, %s))"
        cur = self.keepQuery(query, (login, DBConfig.seed, password))
        try:
            for uid in cur:
                return uid[0]
        finally:
            cur.close()
        raise AuthException('Authentication error')

    def getToken(self, uid, duration):
        query = "INSERT INTO bh_sessions SET bh_user=%s, token=%s, outofdate=ADDDATE(NOW(), INTERVAL %s SECOND)"
        token = str(uuid.uuid4())
        self.doQuery(query, (uid, token, duration))
        return token

    def checkToken(self, token):
        query = "SELECT bh_user FROM bh_sessions WHERE token=%s AND outofdate > NOW()"
        cur = self.keepQuery(query, (token, ))
        try:
            for uid in cur:
                return uid[0]
        finally:
            cur.close()
        raise AuthException('Wrong token {}'.format(token))


class PostPersistance(Persistance):
    def savePost(self, uid, content):
        query = "INSERT INTO bh_posts SET bh_user=%s, content=%s"
        return self.insertQuery(query, (uid, content))

    def saveTag(self, tag):
        # weak, I know
        query = "INSERT INTO bh_tags SET tag=%s ON DUPLICATE KEY UPDATE lastUsed=NOW(), hot=hot+1," \
                " lastTrend=IF(lastUsed > SUBDATE(NOW(), INTERVAL %s SECOND)," \
                " IF(lastTrend < SUBDATE(NOW(), INTERVAL %s SECOND), NOW(), lastTrend), lastTrend)"
        self.insertQuery(query, (tag, DBConfig.trendHeat, DBConfig.trendPast))

    def savePostTag(self, postid, tag):
        query = "INSERT INTO bh_posts_tags SET bh_tag=%s, bh_post=%s"
        self.insertQuery(query, (tag, postid))
