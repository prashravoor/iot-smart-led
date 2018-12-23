from flask_mysqldb import MySQL as mysql
from MySQLdb import OperationalError
import time

class LedModel(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return "{'id': '" + self.id + "', 'name': '" + self.name + "'}"

class LedStatsModel(object):
    def __init__(self, id, startTime, duration):
        self.id = id
        self.startTime = startTime
        self.duration = duration

    def __repr__(self):
        return "{ 'id': '" +  self.id + "', 'switchOnTime': '" + str(self.startTime) + "', 'duration': '" + str(self.duration) + "'}"

class DbConnection(object):
    def __init__(self, flaskApp):
        self.sql = mysql(flaskApp)
        self.conn = self.sql.connect
        self.cursor = self.conn.cursor()

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def run(self, query):
        self.cursor.execute(query)
        self.conn.commit()


class LedDatabase(object):
    def __init__(self, flaskApp):
        self.dbconn = DbConnection(flaskApp)
    
    def get_led(self, id):
        results = self.dbconn.query("SELECT * FROM led")
        print("The results are: ", results)
        leds = [LedModel(res[0], res[1]) for res in results]
        return leds
    
    def switched_on(self, id):
        self.dbconn.run("INSERT into ledstats values ('{}', '{}', '{}')".format(id, str(time.time()), '0'))
    
    def switched_off(self, id):
        rows = self.dbconn.query("SELECT * from ledstats where id = '{}'".format(id))
        print(rows)
        try:
            # Edit the last row always
            row = rows[len(rows)-1]
            sessionTime = time.time() - float(row[1])
            self.dbconn.run("UPDATE ledstats set sessionDuration = '{}' where id = '{}' and switchOnTime = '{}'".format(str(sessionTime), id, row[1]))
        except ValueError:
            print("Failed to update time in the DB")
    
    def get_stats_for_led(self, id):
        rows = self.dbconn.query("SELECT * from ledstats where id = '{}'".format(id))
        return [LedStatsModel(r[0], r[1], r[2]) for r in rows]


# Uncomment to test DB code as a separate REST server

"""
from flask import Flask
from flask import jsonify, Response, request

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'smartled'
app.config['MYSQL_HOST'] = 'localhost'

ledDb = None
with app.app_context():
    ledDb = LedDatabase(app)

@app.route('/') 
def hello_world():
    leds = ledDb.get_led(0)
    return Response(str(leds), mimetype="application/json")

@app.route('/on/<id>')
def on(id):
    ledDb.switched_on(id)
    return Response('', status=204, mimetype='application/json')

@app.route('/off/<id>')
def off(id):
    ledDb.switched_off(id)
    return Response('', status=204, mimetype='application/json')

@app.route('/stats/<id>')
def stats(id):
    return Response(str(ledDb.get_stats_for_led(id)), status=200, mimetype='application/json')

"""