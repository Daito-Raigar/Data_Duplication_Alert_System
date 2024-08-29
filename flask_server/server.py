from flask import Flask,jsonify
from flask_cors import CORS #both front end and backend at diff server 5000 and 3000 to run it we do this


app = Flask(__name__)
CORS(app)
@app.route('/api/data',methods = ['GET'])
def get_data():
    data = { 
        "message":"Hello this is api end point"  #data to get from backend to frontend
        "Connection done successfully"
        "Jamsith"
    }
    return jsonify(data)  #to return data into json file


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

#http://localhost:5000/api/data