from biological_models_app import db
from flask import jsonify, request, Blueprint

SEIDR = Blueprint("SEIDR", __name__, url_prefix="/SEIDR")

@SEIDR.route("/AlterPresets", methods=["POST"])
def add_SEIDR_preset():
    response = {"server status": "success"}
    preset = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding a preset
        #First get id of user with active email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        presetData = preset.get("presetData")
        #Now insert preset into presets table, with the correct Foreign key
        query = "INSERT INTO seidr_presets (owner_id, preset_name, alpha, beta, recip_gamma, recip_epsilon, \
            E_0, I_0, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        cursor.execute(query, (activeid, preset.get("presetName"), presetData[0], presetData[1],
            presetData[2], presetData[3], presetData[4], presetData[5]))
        cursor.close()
        db.commit()
        response["message"] = "Saved SEIDR preset"
    return jsonify(response)

@SEIDR.route("/AlterPresets/<preset_id>", methods=["DELETE"])
def delete_SEIDR_preset(preset_id):
    response = {"server status": "success"}
    if request.method == "DELETE":
        query = "DELETE FROM seidr_presets WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (int(preset_id),))
        cursor.close()
        db.commit()
        response["message"] = "Deleted SEIDR preset"
    return jsonify(response)

@SEIDR.route("/AllPresets", methods=["POST"])
def all_SEIDR_presets():
    response = {"server status": "success"}
    post_data = request.get_json()
    if request.method == "POST": #Grab user's presets
        #First get user id, given email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (post_data.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        #Now grab all pred SEIDR for that user
        query = "SELECT id, preset_name, date FROM seidr_presets WHERE owner_id = %s"
        cursor.execute(query, (activeid,))
        response["presets"] = cursor.fetchall()
        cursor.close()
        response["message"] = "Grabbed all of user's SEIDR presets"
    return jsonify(response)

@SEIDR.route("/PresetParams/<preset_id>", methods=["GET"])
def SEIDR_preset_params(preset_id):
    response = {"server status": "success"}
    if request.method == "GET":
        #Grab data for requested preset
        query = "SELECT alpha, beta, recip_gamma, recip_epsilon, E_0, I_0 FROM seidr_presets WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset_id,))
        response["preset_params"] = cursor.fetchone()
        cursor.close()
        response["message"] = "Grabbed data for selected SEIDR preset"
    return jsonify(response)