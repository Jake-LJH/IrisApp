import os

class Settings:
    secretKey = '6w2hj*2nk4nfa089ym35\)anm52845-sreva124@$)(*17'

    #Dev
    #host='localhost'
    #database='xhhwz3gl8xn1bt8h'
    #user='root'
    #password='root'

    #Staging on heroku
    host=os.environ['Host']
    database=os.environ['Database']
    user=os.environ['Username']
    password=os.environ['Password']
