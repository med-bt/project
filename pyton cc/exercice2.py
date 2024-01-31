import mysql.connector
import re
import datetime
class brutefore():
    def db_connect(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="import", database="sakila")
        return conn
    
    def connection_attempts(self):
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS connection_attempts(
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip text,
                status text,
                attempts_datetime datetime
            );''')
    def read_data(self,file):
        file = open(file,"r+")
        lines  = file.readlines()
        ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        time_pattern = r"\d{4}\s\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}"
        ips=[]
        times=[]
        for line in lines:
            ips.append(re.search(ip_pattern,line).group())
            times.append(re.search(time_pattern,line).group())
        return [ips,times]
    def insert_data(self):
        conn = self.db_connect()
        cursor=conn.cursor()
        ips = self.read_data("logs.log")[0]
        times = self.read_data("logs.log")[1]
        for i in range(len(ips)):
            parsedtime = datetime.datetime.strptime(times[i],"%Y %b %d %H:%M:%S")
            attemptime = parsedtime.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''insert into connection_attempts(ip,attempts_datetime)
                           values ('{}','{}') '''.format(ips[i],attemptime))
    def select_3_min(self):
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("select ip from connection_attempts where attempts_datetime>NOW()-INTERVAL 3 minutes")
        data = cursor.fetchall()
        white_q = cursor.execute("select ip from whitwliste")
        white = cursor.fetchall()
        def count(x,liste):
            count=0
            for i in range(len(liste)):
                if liste[i]==x:
                    count +=1
            return count
        for ip in list(set(data)):
            if count(ip,data)>=10 and ip not in white:
                cursor.execute("UPDATE connection_attempts SET status='danger' WHERE ip='{}'".format(ip))


