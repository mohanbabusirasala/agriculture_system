from flask import Flask, jsonify, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
import os
import pandas as pd
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

from backend import config
from backend.analysis import (
    get_crop_data,
    crop_wise_report,
    region_wise_report,
    yearly_report,
    calculate_yearly_change,
    data_quality_report
)
from backend.charts import (
    create_production_chart,
    create_crop_chart,
    create_yield_chart
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file selected."

    file = request.files["file"]

    if file.filename == "":
        return "No file selected."

    if not file.filename.lower().endswith(".csv"):
        return "Please upload a CSV file."

    filename = os.path.basename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        df = pd.read_csv(file)

        required_columns = [
            "crop_name",
            "region_name",
            "year",
            "cultivated_area_ha",
            "production_tonnes",
            "rainfall_mm"
        ]

        for column in required_columns:
            if column not in df.columns:
                return "Missing required column: " + column

        if df.empty:
            return "The CSV file contains no records."

        if df[required_columns].isnull().any().any():
            return "CSV contains missing values. Please correct them."

        numeric_columns = [
            "year",
            "cultivated_area_ha",
            "production_tonnes",
            "rainfall_mm"
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

            if df[column].isnull().any():
                return "Invalid numeric values in column: " + column

        if (df["year"] <= 0).any():
            return "Year must be positive."

        if (df["cultivated_area_ha"] <= 0).any():
            return "Cultivated area must be greater than zero."

        if (df["production_tonnes"] < 0).any():
            return "Production cannot be negative."

        if (df["rainfall_mm"] < 0).any():
            return "Rainfall cannot be negative."

        if (df["crop_name"].astype(str).str.strip() == "").any():
            return "Crop names cannot be empty."

        if (df["region_name"].astype(str).str.strip() == "").any():
            return "Region names cannot be empty."

        df.to_csv(filepath, index=False)

        return (
            "CSV uploaded and validated successfully! "
            "Total records: " + str(len(df))
        )

    except Exception as e:
        return "Error processing CSV: " + str(e)

@app.route("/reports")
def reports():
    df = get_crop_data()

    crop_report = crop_wise_report(df)
    region_report = region_wise_report(df)
    year_report = calculate_yearly_change(df)
    quality_report = data_quality_report(df)

    create_production_chart()
    create_crop_chart()
    create_yield_chart()

    return render_template(
        "reports.html",
        crop_report=crop_report.to_dict(orient="records"),
        region_report=region_report.to_dict(orient="records"),
        year_report=year_report.to_dict(orient="records"),
        quality_report=quality_report.to_dict(orient="records")
    )


# Regions

@app.route("/regions", methods=["GET"])
def all_regions():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)

    mc.execute("SELECT * FROM regions ORDER BY region_id ASC")
    regions = mc.fetchall()

    mc.close()
    mydb.close()

    return render_template("regions.html", regions=regions)


# Crops
@app.route("/crops", methods=["GET"])
def all_crops():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)

    mc.execute("SELECT * FROM crops ORDER BY crop_id ASC")
    crops = mc.fetchall()

    mc.close()
    mydb.close()

    return render_template("crops.html", crops=crops)


# All crop records
@app.route("/records", methods=["GET"])
def all_records():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)

    mc.execute("""
        SELECT
            cr.record_id,
            c.crop_name,
            r.region_name,
            cr.year,
            cr.cultivated_area_ha,
            cr.production_tonnes,
            cr.rainfall_mm
        FROM crop_records cr
        JOIN crops c ON cr.crop_id = c.crop_id
        JOIN regions r ON cr.region_id = r.region_id
        ORDER BY cr.record_id ASC;
    """)

    records = mc.fetchall()

    mc.close()
    mydb.close()

    return render_template("records.html", records=records)


# Records for a particular year
@app.route("/records/year/<int:year>", methods=["GET"])
def records_by_year(year):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute(
        "SELECT * FROM crop_records WHERE year = %s;",
        (year,)
    )
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)


# Records for a particular crop
@app.route("/records/crop/<int:crop_id>", methods=["GET"])
def records_by_crop(crop_id):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute(
        "SELECT * FROM crop_records WHERE crop_id = %s;",
        (crop_id,)
    )
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)


# Records for a particular region
@app.route("/records/region/<int:region_id>", methods=["GET"])
def records_by_region(region_id):
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)
    mc.execute(
        "SELECT * FROM crop_records WHERE region_id = %s;",
        (region_id,)
    )
    r = mc.fetchall()
    mc.close()
    mydb.close()
    return jsonify(r)





# Yield = production / cultivated area
@app.route("/yield", methods=["GET"])
def yield_data():
    mydb = config.connect()
    mc = mydb.cursor(dictionary=True)

    mc.execute("""
        SELECT
            c.crop_name,
            r.region_name,
            cr.year,
            cr.cultivated_area_ha,
            cr.production_tonnes,
            cr.production_tonnes / cr.cultivated_area_ha
                AS yield_per_hectare
        FROM crop_records cr
        JOIN crops c ON cr.crop_id = c.crop_id
        JOIN regions r ON cr.region_id = r.region_id
        WHERE cr.cultivated_area_ha > 0
        ORDER BY cr.year, c.crop_name;
    """)

    records = mc.fetchall()

    mc.close()
    mydb.close()

    return render_template("yield.html", records=records)


@app.route("/farmer-register", methods=["GET", "POST"])
def farmer_register():
    if request.method == "GET":
        return render_template("farmer_register.html", message="")

    farmer_name = request.form.get("farmer_name", "").strip()
    mobile_number = request.form.get("mobile_number", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    village = request.form.get("village", "").strip()

    if not all([farmer_name, mobile_number, password,
                confirm_password, village]):
        return render_template(
            "farmer_register.html",
            message="Please fill in all fields."
        )

    if not mobile_number.isdigit() or len(mobile_number) != 10:
        return render_template(
            "farmer_register.html",
            message="Enter a valid 10-digit mobile number."
        )

    if len(password) < 8:
        return render_template(
            "farmer_register.html",
            message="Password must contain at least 8 characters."
        )

    if password != confirm_password:
        return render_template(
            "farmer_register.html",
            message="Passwords do not match."
        )

    mydb = None
    mc = None

    try:
        mydb = config.connect()
        mc = mydb.cursor()

        password_hash = generate_password_hash(password)

        mc.execute("""
            INSERT INTO farmers
                (farmer_name, mobile_number, password_hash, village)
            VALUES (%s, %s, %s, %s)
        """, (
            farmer_name,
            mobile_number,
            password_hash,
            village
        ))

        mydb.commit()

        return render_template(
            "farmer_register.html",
            message="Farmer registered successfully!"
        )

    except Exception as e:
        if mydb:
            mydb.rollback()

        if "1062" in str(e):
            message = "This mobile number is already registered."
        else:
            app.logger.exception("Farmer registration failed")
            message = "Registration failed. Please check your database connection."

        return render_template(
            "farmer_register.html",
            message=message
        )

    finally:
        if mc:
            mc.close()
        if mydb:
            mydb.close()


@app.route("/farmer-crop-details", methods=["GET", "POST"])
def farmer_crop_details():
    mydb = None
    mc = None

    try:
        mydb = config.connect()
        mc = mydb.cursor(dictionary=True)

        if request.method == "POST":
            farmer_id = request.form.get("farmer_id", type=int)
            crop_id = request.form.get("crop_id", type=int)
            region_id = request.form.get("region_id", type=int)
            year = request.form.get("year", type=int)
            area = request.form.get("cultivated_area_ha", type=float)
            production = request.form.get("production_tonnes", type=float)
            rainfall_text = request.form.get("rainfall_mm", "").strip()
            rainfall = float(rainfall_text) if rainfall_text else None

            if not all([farmer_id, crop_id, region_id, year]) or area is None or production is None:
                raise ValueError("Please enter all required details.")

            if year < 1 or year > 2100:
                raise ValueError("Enter a valid year.")

            if area <= 0 or production < 0:
                raise ValueError("Area must be positive and production cannot be negative.")

            if rainfall is not None and rainfall < 0:
                raise ValueError("Rainfall cannot be negative.")

            mc.execute(
                "SELECT farmer_id FROM farmers WHERE farmer_id = %s",
                (farmer_id,)
            )
            if not mc.fetchone():
                raise ValueError("Farmer ID not found. Please check the ID.")

            mc.execute(
                "SELECT crop_id FROM crops WHERE crop_id = %s",
                (crop_id,)
            )
            if not mc.fetchone():
                raise ValueError("Please select a valid crop.")

            mc.execute(
                "SELECT region_id FROM regions WHERE region_id = %s",
                (region_id,)
            )
            if not mc.fetchone():
                raise ValueError("Please select a valid region.")

            mc.execute("""
                INSERT INTO farmer_records
                (farmer_id, crop_id, region_id, year,
                 cultivated_area_ha, production_tonnes, rainfall_mm)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                farmer_id, crop_id, region_id, year,
                area, production, rainfall
            ))

            mydb.commit()
            message = "Crop details saved successfully!"

        else:
            message = ""

        mc.execute("SELECT crop_id, crop_name FROM crops ORDER BY crop_id")
        crops = mc.fetchall()

        mc.execute(
            "SELECT region_id, region_name FROM regions ORDER BY region_id"
        )
        regions = mc.fetchall()

        return render_template(
            "farmer_crop_details.html",
            crops=crops,
            regions=regions,
            message=message
        )

    except ValueError as e:
        if mydb:
            mydb.rollback()

        mc = mc if mc else None

        try:
            if mc:
                mc.execute("SELECT crop_id, crop_name FROM crops ORDER BY crop_id")
                crops = mc.fetchall()
                mc.execute(
                    "SELECT region_id, region_name FROM regions ORDER BY region_id"
                )
                regions = mc.fetchall()
            else:
                crops, regions = [], []
        except Exception:
            crops, regions = [], []

        return render_template(
            "farmer_crop_details.html",
            crops=crops,
            regions=regions,
            message=str(e)
        )

    except Exception:
        if mydb:
            mydb.rollback()

        app.logger.exception("Saving farmer crop details failed")

        return "Unable to save crop details. Check the PyCharm terminal for the error.", 500

    finally:
        if mc:
            mc.close()
        if mydb:
            mydb.close()




if __name__ == "__main__":
    app.run(debug=False)
