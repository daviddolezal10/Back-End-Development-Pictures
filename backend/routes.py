from . import app
import os
import json
from flask import Flask, jsonify, request, make_response, abort, url_for  # noqa; F401
from backend import app

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
    return jsonify(data), 200 # Návrat seznamu obrázků v JSON formátu

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Posunutí indexu, pokud se ID počítá od 1
    corrected_index = id - 1  # Jestli data začínají indexem 1
    if 0 <= corrected_index < len(data):
        return jsonify(data[corrected_index]), 200  # Návrat položky podle indexu
    else:
        return jsonify({"error": "Picture not found"}), 404  # Vrací chybu, pokud je index mimo rozsah


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Získejte data z těla požadavku
    picture = request.get_json()  # Pokud tělo není JSON, přidejte validaci
    
    # Zkontrolujte, zda obrázek s tímto ID již neexistuje
    for item in data:
        if item['id'] == picture['id']:
            # Pokud ano, vraťte HTTP kód 302 s varováním
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    
    # Přidejte nový obrázek do seznamu
    data.append(picture)

    # Vrátí HTTP kód 201 pro úspěšnou tvorbu
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Získejte data z těla požadavku
    update_data = request.get_json()  # Ujistěte se, že tělo je ve formátu JSON

    # Najděte obrázek s daným ID v seznamu 'data'
    for picture in data:
        if picture['id'] == id:
            # Pokud existuje, aktualizujte jej s novými daty
            picture.update(update_data)
            return jsonify(picture), 200
    
    # Pokud obrázek neexistuje, vraťte HTTP kód 404
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    # Najdi index obrázku s daným ID
    for i, picture in enumerate(data):
        if picture["id"] == id:
            # Pokud ho najdeš, odstraň položku ze seznamu
            del data[i]
            # Vrať prázdnou odpověď s HTTP 204 No Content
            return "", 204
    
    # Pokud obrázek nebyl nalezen, vrať odpověď s HTTP 404 Not Found a zprávou
    return jsonify({"message": "picture not found"}), 404