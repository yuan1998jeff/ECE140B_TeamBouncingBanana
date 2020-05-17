# Import MySQL Connector Driver
import mysql.connector as mysql
import pandas as pd 

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = 'localhost' # different than inside the container and assumes default port of 3306

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists TCourses;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE TCourses (
      id integer          AUTO_INCREMENT PRIMARY KEY,
      CourseName          VARCHAR(30) NOT NULL,
      Major               VARCHAR(30) NOT NULL,
      Requirement         VARCHAR(50) NOT NULL,
      Depth               VARCHAR(50) NOT NULL,
      CourseDescription   VARCHAR(1000) NOT NULL,
      OfferingQuarter     VARCHAR(50) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Table already exists. Not recreating it.")

## load courses.csv
data = pd.read_csv("courses.csv") 
rowNum = len(data)

print(data["Depth"][0])
for cnt in range(rowNum):
  # Insert Records
  query = "INSERT INTO TCourses (CourseName, Major, Requirement, Depth, CourseDescription, OfferingQuarter,created_at) values (%s, %s, %s, %s, %s, %s, %s);"
  value = [ data["CourseName"][cnt], data["Major"][cnt],  data["Requirement"][cnt], data["Depth"][cnt], data["CourseDescription"][cnt], data["OfferingQuarter"][cnt], '2020-02-11 12:00:00']
  
  cursor.execute(query, value)
  db.commit()


# cursor=db.cursor()
#     query = "INSERT INTO TMoves (initiateTime,startTime,endTime,direction,userId,status) values (%s,%s,%s,%s,%s,%s);"
#     values = ('2020-02-11 12:00:00',None, None,'forward','OLOLO','Pending')
#     cursor.execute(query, values)
#     db.commit()
#     db.close()


# Selecting Records
cursor.execute("select * from TCourses;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

db.close()