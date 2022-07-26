from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    db = mongo.company
    print("DB connected")
    mongo.server_info()
except:
    print("Cannot connect to db")


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {"First_name": request.form["fname"], "Last_name": request.form["lname"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps({"message": "user created", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("************")
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read users", "exception": f"{ex}"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users', methods=['GET'])
def read_users():
    try:
        data = list(db.users.find())
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read users", "exception": f"{ex}"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                "First_name": request.form["fname"],
                "Last_name": request.form["lname"]
            }}
        )
        if dbResponse.modified_count==1:
            return Response(
                response=json.dumps({"message": f"updated data for user {request.form['fname']+' '+request.form['lname']}"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message": f"nothing to update for user {request.form['fname']+' '+request.form['lname']}"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": f"cannot update user {id}", "exception": f"{ex}"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one(
            {"_id": ObjectId(id)}
        )
        if dbResponse.deleted_count>0:
            return Response(
                response=json.dumps(
                    {"message": f"data deleted for user {id}"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {"message": f"No user with userid {id} is present"}),  # db.users[id]
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": f"cannot delete user {id}", "exception": f"{ex}"}),
            status=500,
            mimetype="application/json"
        )


@app.route('/users/fname/<name>', methods=['GET'])
def read_userss(name):
    try:
        data = list(db.users.find({"First_name":name}))
        for user in data:
            user['_id'] = str(user['_id'])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read users", "exception": f"{ex}"}),
            status=500,
            mimetype="application/json"
        )



if __name__ == '__main__':
    app.run(debug=True)
