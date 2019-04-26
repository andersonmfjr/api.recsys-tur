import pymysql.cursors
import pandas as pd
import os
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '../..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

class Database:
    def __init__(self):
        self.con = pymysql.connect(
            host=os.getenv('HOST_DB'),
            user=os.getenv('USER_DB'),
            password=os.getenv('PASS_DB'),
            db=os.getenv('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def insertUser(self, email):
        sql = "INSERT INTO `user` (`id`, `email`) VALUES (%s, %s)"
        self.cur.execute(sql, (None, email))
        self.con.commit()
        user = self.findUserByEmail(email)
        return user

    # users
    def findAllUsers(self):
        sql = "SELECT * FROM user"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def findUserById(self, id):
        sql = "SELECT * from user where id = " + str(id)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def findUserByEmail(self, email):
        sql = "SELECT * from user where email = %s"
        self.cur.execute(sql, (email))
        result = self.cur.fetchone()
        return result

    def deleteUserById(self, id):
        sql = "DELETE from user where id = " + str(id)
        self.cur.execute(sql, str(id))
        self.con.commit()

    def deleteUserByEmail(self, email):
        sql = "DELETE from user where email = %s"
        self.cur.execute(sql, email)
        self.con.commit()

    # places
    def findAllPlaces(self):
        sql = "SELECT * FROM place"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def findFourByIdPlaces(self, id1, id2, id3, id4):
        sql = "SELECT * FROM place WHERE id = %s OR id = %s OR id = %s OR id = %s"
        self.cur.execute(sql, (str(id1), str(id2), str(id3), str(id4)))
        result = self.cur.fetchall()
        return result

    def findByIdPlaces(self, id):
        sql = "SELECT * FROM place WHERE id = %s"
        self.cur.execute(sql, (str(id)))
        result = self.cur.fetchone()
        return result

    def findRandomPlaces(self):
        sql = "SELECT * FROM place ORDER BY RAND() LIMIT 4"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    # rating
    def insertRating(self, userId, placeId, rate):
        sql = "INSERT INTO `rating` (`id`, `user_id`, `place_id`, `rate`) VALUES (%s, %s, %s, %s)"
        self.cur.execute(sql, (None, str(userId), str(placeId), str(rate)))
        self.con.commit()

    def findAllRatings(self):
        sql = "SELECT * FROM rating"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    # sugestion
    def insertSugestion(
        self, userId, placeId, ratePrevision, rateUser, algorithm
    ):
        sql = "INSERT INTO `gratification` (`user_id`, `place_id`, `rate_prevision`, `rate_user`, `algorithm`) VALUES (%s, %s, %s, %s, %s)"
        self.cur.execute(
            sql, (
                str(userId), str(placeId), str(ratePrevision), str(rateUser),
                str(algorithm)
            )
        )
        self.con.commit()

    def importCsv(self):
        data = pd.read_csv(
            '/home/gabriellima/ratings.csv',
            names=['userId', 'placeId', 'rate']
        )
        tuples = [tuple(x) for x in data.values]
        with open("/home/gabriellima/touristm.txt", "w") as stream:
            for x in tuples:
                v = str(x) + ','
                print(v, file=stream)

            print('Ok')
