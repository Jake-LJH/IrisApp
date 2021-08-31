import os

class Settings:
    secretKey = '6w2hj*2nk4nfa089ym35\)anm52845-sreva124@$)(*17'

    #Dev
    #host='localhost'
    #database='xhhwz3gl8xn1bt8h'
    #user='root'
    #password='root'

    #Staging on heroku
    host="s29oj5odr85rij2o.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
    #os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USERNAME']
    password=os.environ['PASSWORD']
