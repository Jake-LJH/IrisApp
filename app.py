from flask import Flask,jsonify, render_template, request, redirect, url_for, abort, make_response
from model.User import User
from model.IrisPrediction import IrisData
from validation.Validator import *
from flask_cors import CORS
import numpy as np
import pickle
import datetime

app = Flask(__name__)
CORS(app)
model = pickle.load(open('iris_model.pkl', 'rb'))

#POST 1 new user - Insert
@app.route('/registerUser', methods=['POST'])
@validateRegister
def insertUser():
    try:
        userData = request.form
        username = userData['username']
        email = userData['email']
        password = userData['password']

        count = User.registerUser(username, email, password)
        
        return render_template("login.html")
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#Delete Request    
@app.route('/users/<int:userid>', methods=['DELETE'])
@login_required
def deleteUser(userid):
    try: 
        count = User.deleteUser(userid)
        
        if count == 1:
            output = {'message': 'User with '+str(userid)+' has been successfully deleted!'}
            return jsonify(output), 200
        else:
            output={'message': 'User with '+str(userid)+' does not exist!'}
            return jsonify(output), 404
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500


@app.route('/<string:url>')
def staticPage(url):
    print("static page",url)
    try:
        return render_template(url)
    except Exception as err:
        abort(404)

@app.route('/')
def default():
    try:
        return redirect("login.html")
    except Exception as err:
        abort(404)

@app.route('/login', methods=["POST"])
def loginUser():
    try:
        error = None
        htmlEmail = request.form['email']
        htmlPassword = request.form['password']
        userSQLData = User.loginUser({"email":htmlEmail,"password":htmlPassword})

        if userSQLData["jwt"] == "":
            error = 'Invalid Credentials. Please try again.'
            return render_template("login.html", error=error)

        else:
            resp = make_response(render_template("mainPage.html"))
            resp.set_cookie('jwt', userSQLData["jwt"])
            return resp
            
    except Exception as err:
        print(err)
        error = 'Invalid Credentials. Please try again.'
        return render_template("login.html", error=error)

@app.route('/predict', methods=["POST"])
@login_required
def predict():
    timestamp = datetime.datetime.utcnow()
    int_features = [float(x) for x in request.form.values()]
   
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    userIris = request.form
    sL = userIris['SepalLength']
    sW = userIris['SepalWidth']
    pL = userIris['PetalLength']
    pW = userIris['SepalWidth']
    output = prediction[0]

    IrisData.insertData(sL, sW, pL, pW, output, timestamp)
    

    return redirect('main')

@app.route('/main', methods=["GET"])
@login_required
def home():
    irisJson = IrisData.getAllPred()
    return render_template('mainPage.html', data=irisJson)

@app.route('/remove', methods=["POST"])
@login_required
def remove():
    dataId = request.form["id"]
    print(dataId)
    IrisData.deletePred(dataId)
    try:
        dataId = request.form["id"]
        IrisData.deletePred(dataId)

        return redirect("main")
    except Exception as err:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/logout') #define the api route
def logout():
    resp = make_response(redirect("login.html"))
    resp.delete_cookie('jwt')
    
    return resp


if __name__ == '__main__':
    app.run(debug=True)