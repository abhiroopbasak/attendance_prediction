from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
import requests
from pprint import pprint
import csv
import holidays
from wsgiref.util import FileWrapper
from sklearn import linear_model
import pandas as pd
import numpy as np
import holidays
import csv



def index(request):
  return render(request,"Star_landing.html")



def getdata(request):
  client=MongoClient("mongodb+srv://admin_project:project@clusterlarkai1.idztf.mongodb.net/student?retryWrites=true&w=majority")
  db=client.get_database('studentdb')
  records=db.student

  db=list(records.find())

  csv_columns=['_id','date','time','temperature','humidity','male','female','subject','teacher','department','section','semester','promixity_to_exam','distm10','distl10','holiday','attendance']

  csv_file='db.csv'

  with open(csv_file,'w') as csvfile:
    writer=csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer.writeheader()
    for data in db:
      writer.writerow(data)



def register(request):
  client=MongoClient("mongodb+srv://admin_project:project@clusterlarkai1.idztf.mongodb.net/register?retryWrites=true&w=majority")
  rg=client.get_database('registration')
  regi=rg.register
  
  def regi_inp(r_name,r_email,r_cname,r_password):
    new_user={
      'name' : r_name,
      'email' : r_email,
      'cname' : r_cname,
      'password' : r_password
    }
    regi.insert_one(new_user)

  r_name=request.GET['name']
  r_email=request.GET['email']
  r_cname=request.GET['cname']
  r_password=request.GET['password']
  #r_cpassword=request.GET['cpassword']

  regi_inp(r_name,r_email,r_cname,r_password)

  return render(request,"Star_landing.html",{'register':'Registration Successful'})
  




def login(request):
  client=MongoClient("mongodb+srv://admin_project:project@clusterlarkai1.idztf.mongodb.net/register?retryWrites=true&w=majority")
  rg=client.get_database('registration')
  regi=rg.register
  
  rg=list(regi.find())

  r_email=request.GET['email']
  r_password=request.GET['password']

  flag=0
  for i in range(0,len(rg)):

    if (rg[i]['email']==r_email and rg[i]['password']==r_password):
        flag=1
        break
    
        
      

  r_name=rg[i]['name']
  r_cname=rg[i]['cname']        
  if flag==1:        
    getdata(request)
    return render(request,"star_profile.html",{'name':r_name,'cname':r_cname})
  else:
    return render(request,"Star_landing.html",{'invalid':'Invalid Credentials'})



    



def fillup(request):
  in_date=request.GET['date']
  in_time=request.GET['time']
  in_male=int(request.GET['male'])
  in_female=int(request.GET['female'])
  in_subject=request.GET['subject']
  in_teacher=request.GET['teacher']
  in_department=request.GET['dept']
  in_section=request.GET['sec']
  in_semester=int(request.GET['sem'])
  in_proximity_to_exam=int(request.GET['exam'])
  in_distm10=int(request.GET['dm10'])
  in_distl10=int(request.GET['dl10'])
  in_attendance=int(request.GET['attendance'])



  client=MongoClient("mongodb+srv://admin_project:project@clusterlarkai1.idztf.mongodb.net/student?retryWrites=true&w=majority")
  db=client.get_database('studentdb')
  records=db.student
  records.count_documents({})




  def dbinput(in_date,in_time,in_temperature,in_humidity,in_male,in_female,in_subject,in_teacher,in_department,in_section,in_semester,in_proximity_to_exam,in_distm10,in_distl10,in_holiday,in_attendance):
    new_student={
      'date' : in_date,
      'time' : in_time,
      'temperature' : in_temperature,
      'humidity' : in_humidity,
      'male' : in_male,
      'female' : in_female,
      'subject' : in_subject,
      'teacher' : in_teacher,
      'department' : in_department,
      'section' : in_section,
      'semester' : in_semester,
      'promixity_to_exam' : in_proximity_to_exam,
      'distm10' : in_distm10,
      'distl10' : in_distl10,
      'holiday' : in_holiday,
      'attendance' : in_attendance
    }
    records.insert_one(new_student)




  def weather_data(query):
	  res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
	  return res.json()


  city='Kolkata'
  query="q="+city
  result=weather_data(query)
  ind_holiday = holidays.India(years=2021)
  in_temperature=result['main']['temp']
  in_weather=result['weather'][0]['main']
  in_humidity=result['main']['humidity']
  
  in_holiday=( in_date in ind_holiday)

  #if(in_department=='IT' and in_section=='A' and in_sem==3):
   # in_distm10=
   # in_distl10=
  

  

  dbinput(in_date,in_time,in_temperature,in_humidity,in_male,in_female,in_subject,in_teacher,in_department,in_section,in_semester,in_proximity_to_exam,in_distm10,in_distl10,in_holiday,in_attendance)



#in_date='2021-01-15'
#in_time='07:50'
#in_male=44
#in_female=20
#in_subject='Maths'
#in_teacher='Mr.Pal'
#in_department='IT'
#in_section='A'
#in_semester=3
#in_proximity_to_exam=4
#in_distm10=50
#in_distl10=14
#in_holiday=( in_date in ind_holiday)
#in_attendance=50

  return render(request,'star_profile.html')





def prediction(request):


  def weather_data(query):
	  res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
	  return res.json()

  import pandas as pd

  df=pd.read_csv("db.csv")

 


  in_date=request.GET['date']
  in_time=request.GET['time']
  in_proximity_to_exam=int(request.GET['exam'])

  city='Kolkata'
  query="q="+city
  result=weather_data(query)
  in_temperature=result['main']['temp']
  in_humidity=result['main']['humidity']
 


# Importing the dataset

  reg=linear_model.LinearRegression()
  reg.fit(df[['temperature','humidity','promixity_to_exam']],df.attendance)
  reg.coef_
  reg.intercept_
  preg=reg.predict([[in_temperature,in_humidity,in_proximity_to_exam]])
  preg=int(preg)
  

  df=df.drop('_id',axis=1)
  df=df.drop('date',axis=1)
  df=df.drop('time',axis=1)
  df=df.drop('subject',axis=1)
  df=df.drop('teacher',axis=1)
  df=df.drop('holiday',axis=1)
  df=df.drop('department',axis=1)
  df=df.drop('section',axis=1)
#df=df.drop('distm10',axis=1)
#df=df.drop('distl10',axis=1)
#df=df.drop('male',axis=1)
#df=df.drop('female',axis=1)
  X = df.iloc[:, :-1].values
  y = df.iloc[:, 1].values
# Splitting the dataset into the Training set and Test set
  from sklearn.model_selection import train_test_split
  X_train, X_test, y_train, y_test = train_test_split(X, y,     test_size = 1/3, random_state = 42)
# Fitting Simple Linear Regression to the Training set
  from sklearn.linear_model import LinearRegression
  regressor = LinearRegression()
  regressor.fit(X_train, y_train)
# Predicting the Test set results
  y_pred = regressor.predict(X_test)
# Explained variance score: 1 is perfect prediction
  score=regressor.score(X_test, y_test)

  ascore=score*(100)

  return render(request,"Star_prediction.html",{'prediction':preg,'date':in_date,'accuracy':ascore})  


def predict(request):
  return render(request,"Star_prediction.html")