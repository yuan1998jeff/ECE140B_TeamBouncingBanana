import pandas as pd 


data = pd.read_csv("courses.csv") 

print(type(data["CourseName"][0]))