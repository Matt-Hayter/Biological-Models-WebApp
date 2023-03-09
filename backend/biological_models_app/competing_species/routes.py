from biological_models_app import db
from flask import jsonify, request, Blueprint
from biological_models_app.competing_species.simulation import runCompetingSpeciesSim

competing_species = Blueprint("competing_species", __name__, url_prefix="/CompetingSpecies")

@competing_species.route("/AlterPresets", methods=["POST"])
def add_CompetingSpecies_preset():
    response = {"server status": "success"}
    preset = request.get_json() #Retrieve payload from client
    #First get id of user with active email
    query = "SELECT id FROM users WHERE email = %s"
    cursor = db.cursor()
    cursor.execute(query, (preset.get("userEmail"),))
    activeid = cursor.fetchone()[0]
    presetData = preset.get("presetData")
    #Now insert preset into presets table, with the correct Foreign key
    query = "INSERT INTO competing_species_presets (owner_id, preset_name, N1_0, r1, K1, a1, \
        N2_0, r2, K2, a2, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
    cursor.execute(query, (activeid, preset.get("presetName"), presetData[0], presetData[1],
        presetData[2], presetData[3], presetData[4], presetData[5], presetData[6], presetData[7]))
    cursor.close()
    db.commit()
    response["message"] = "Saved PredPrey preset"
    return jsonify(response)

@competing_species.route("/AlterPresets/<preset_id>", methods=["DELETE"])
def delete_CompetingSpecies_preset(preset_id):
    response = {"server status": "success"}
    query = "DELETE FROM competing_species_presets WHERE id = %s"
    cursor = db.cursor()
    cursor.execute(query, (int(preset_id),))
    cursor.close()
    db.commit()
    response["message"] = "Deleted CompetingSpecies preset"
    return jsonify(response)

@competing_species.route("/AllPresets", methods=["POST"])
def all_CompetingSpecies_presets(): #Grab user's presets
    response = {"server status": "success"}
    post_data = request.get_json()
    #First get user id, given email
    query = "SELECT id FROM users WHERE email = %s"
    cursor = db.cursor()
    cursor.execute(query, (post_data.get("userEmail"),))
    activeid = cursor.fetchone()[0]
    #Now grab all competing species presets for that user
    query = "SELECT id, preset_name, date FROM competing_species_presets WHERE owner_id = %s"
    cursor.execute(query, (activeid,))
    response["presets"] = cursor.fetchall()
    cursor.close()
    response["message"] = "Grabbed all of user's competing species presets"
    return jsonify(response)

@competing_species.route("/PresetParams/<preset_id>", methods=["GET"])
def CompetingSpecies_preset_params(preset_id):
    response = {"server status": "success"}
    #Grab data for requested preset
    query = "SELECT N1_0, r1, K1, a1, N2_0, r2, K2, a2 FROM competing_species_presets WHERE id = %s"
    cursor = db.cursor()
    cursor.execute(query, (preset_id,))
    response["preset_params"] = cursor.fetchone()
    cursor.close()
    response["message"] = "Grabbed data for selected comepting species preset"
    return jsonify(response)

@competing_species.route("/RunSim", methods=["POST"])
def run_CompetingSpecies_sim():
    response = {"server status": "success"}
    sim_params = request.get_json().get("simParams")
    #Run simulation and return data
    response["sim_data"], response["graph_bounds"] = runCompetingSpeciesSim(sim_params)
    response["message"] = "Ran simulation successfully"
    return jsonify(response)