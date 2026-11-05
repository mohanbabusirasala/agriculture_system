from flask import Flask, jsonify,request
import config
app = Flask(__name__)

@app.route("/")
def home():
    return "Agricultural Crop Production Analysis System"

#regions
@app.route("/regions", methods=["GET"])
def all_regions():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM regions order by region_id asc;")
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)

#crops
@app.route("/crops", methods=["GET"])
def all_crops():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM crops order by crop_id asc;")
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)

#records
@app.route("/records", methods=["GET"])
def all_records():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM crop_records;")
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)

#Get crop records for a particular year
@app.route("/records/year/<int:year>", methods=["GET"])
def records_by_year(year):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM crop_records WHERE year=%s;", (year,))
    r = mc.fetchall()
    return jsonify(r)

#Get records for a particular crop
@app.route("/records/crop/<int:crop_id>", methods=["GET"])
def records_by_crop(crop_id):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM crop_records WHERE crop_id=%s;", (crop_id,))
    r = mc.fetchall()
    return jsonify(r)

#Get records for a particular region
@app.route("/records/region/<int:region_id>", methods=["GET"])
def records_by_region(region_id):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("SELECT * FROM crop_records WHERE region_id=%s;", (region_id,))
    r = mc.fetchall()
    return jsonify(r)


#yield = production/cultivated area
@app.route("/yield", methods=["GET"])
def crop_yield():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute("""
        SELECT
            crops.crop_name,
            regions.region_name,          
            crop_records.year,
            crop_records.cultivated_area_ha,
            crop_records.production_tonnes,
            crop_records.production_tonnes /
            crop_records.cultivated_area_ha AS yield_per_hectare
        FROM crop_records
        JOIN crops
            ON crop_records.crop_id = crops.crop_id
        JOIN regions
            ON crop_records.region_id = regions.region_id
        WHERE crop_records.cultivated_area_ha > 0
        ORDER BY crop_records.record_id ASC;
    """)
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)


