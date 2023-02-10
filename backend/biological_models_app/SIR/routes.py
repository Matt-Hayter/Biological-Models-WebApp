from biological_models_app import db
from flask import jsonify, request, Blueprint
from biological_models_app.SIR.simulation import runSIRSim

SIR = Blueprint("SIR", __name__, url_prefix="/SIR")

@SIR.route("/AlterPresets", methods=["POST"])
def add_SIR_preset():
    response = {"server status": "success"}
    preset = request.get_json() #Retrieve payload from client
    #First get id of user with active email
    query = "SELECT id FROM users WHERE email = %s"
    cursor = db.cursor()
    cursor.execute(query, (preset.get("userEmail"),))
    activeid = cursor.fetchone()[0]
    presetData = preset.get("presetData")
    #Now insert preset into presets table, with the correct Foreign key
    query = "INSERT INTO sir_presets (owner_id, preset_name, I_0, beta, recip_gamma, date) \
        VALUES (%s,%s,%s,%s,%s,NOW())"
    cursor.execute(query, (activeid, preset.get("presetName"), presetData[0], presetData[1],
        presetData[2]))
    cursor.close()
    db.commit()
    response["message"] = "Saved SIR preset"
    return jsonify(response)

@SIR.route("/AlterPresets/<preset_id>", methods=["DELETE"])
def delete_SIR_preset(preset_id):
    response = {"server status": "success"}
    query = "DELETE FROM sir_presets WHERE id = %s"
    cursor = db.cursor()
    cursor.execute(query, (int(preset_id),))
    cursor.close()
    db.commit()
    response["message"] = "Deleted SIR preset"
    return jsonify(response)

@SIR.route("/AllPresets", methods=["POST"])
def all_SIR_presets(): #Grab user's presets
    response = {"server status": "success"}
    post_data = request.get_json()
    #First get user id, given email
    query = "SELECT id FROM users WHERE email = %s"
    cursor = db.cursor()
    cursor.execute(query, (post_data.get("userEmail"),))
    activeid = cursor.fetchone()[0]
    #Now grab all pred SIR for that user
    query = "SELECT id, preset_name, date FROM sir_presets WHERE owner_id = %s"
    cursor.execute(query, (activeid,))
    response["presets"] = cursor.fetchall()
    cursor.close()
    response["message"] = "Grabbed all of user's SIR presets"
    return jsonify(response)

@SIR.route("/PresetParams/<preset_id>", methods=["GET"])
def SIR_preset_params(preset_id):
    response = {"server status": "success"}
    #Grab data for requested preset
    query = "SELECT I_0, beta, recip_gamma FROM sir_presets WHERE id = %s"
    cursor = db.cursor()
    cursor.execute(query, (preset_id,))
    response["preset_params"] = cursor.fetchone()
    cursor.close()
    response["message"] = "Grabbed data for selected SIR preset"
    return jsonify(response)

@SIR.route("/RunSim", methods=["POST"])
def run_SIR_sim():
    response = {"server status": "success"}
    sim_params = request.get_json().get("simParams")
    #Run simulation and return data
    response["sim_data"], response["time_data"], response["sim_max_val"] = runSIRSim(sim_params)
    response["message"] = "Ran simulation successfully"
    return jsonify(response)