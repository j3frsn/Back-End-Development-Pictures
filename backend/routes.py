from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return make_response(jsonify(data), 200)
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for pic in data:
            if pic["id"] == id:
                return pic, 200
        return {"message": "File not found"}, 404

    return {"message": "Internal server error"}, 500

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if picture:
        for pic in data:
            # Tests if the pic already exists...
            if pic["id"] == picture["id"]:
                return {"Message": f"picture with id {picture['id']} already present"}, 302
        data.append(picture)
        return make_response(jsonify(data[picture["id"]]), 201)

    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    if picture:
        for pic in data:
            # Tests if the pic already exists...
            if pic["id"] == picture["id"]:
                data[pic] = picture
                return {"message": f"picture with id {picture['id']} updated"}, 200
        data.append(picture)
        return make_response(jsonify(data[picture["id"]]), 201)

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        if data[id]:
            data.remove(id)
            return "", 204
        return {"message": "File not found"}, 404

    return {"message": "Internal server error"}, 500    
