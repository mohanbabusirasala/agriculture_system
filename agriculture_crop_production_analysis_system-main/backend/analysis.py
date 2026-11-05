import pandas as pd
import numpy as np

from backend import config


def get_connection():
    return config.connect()


def get_crop_data():
    conn = get_connection()
    try:
        query = """
            SELECT
                cr.record_id,
                c.crop_name,
                r.region_name,
                cr.year,
                cr.cultivated_area_ha,
                cr.production_tonnes,
                cr.rainfall_mm
            FROM crop_records cr
            JOIN crops c
                ON cr.crop_id = c.crop_id
            JOIN regions r
                ON cr.region_id = r.region_id
            ORDER BY cr.year, c.crop_name, r.region_name
        """
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [item[0] for item in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return df
    finally:
        conn.close()


def calculate_yield(df):
    df = df.copy()
    area = pd.to_numeric(df["cultivated_area_ha"], errors="coerce")
    production = pd.to_numeric(df["production_tonnes"], errors="coerce")
    valid = area.notna() & (area > 0) & production.notna() & (production >= 0)
    df["yield_tonnes_per_ha"] = np.nan
    df.loc[valid, "yield_tonnes_per_ha"] = production[valid] / area[valid]
    return df


def crop_wise_report(df):
    report = df.groupby("crop_name", as_index=False).agg(
        total_production_tonnes=("production_tonnes", "sum"),
        total_area_ha=("cultivated_area_ha", "sum"),
        record_count=("record_id", "count")
    )
    return report.sort_values("total_production_tonnes", ascending=False)


def region_wise_report(df):
    report = df.groupby("region_name", as_index=False).agg(
        total_production_tonnes=("production_tonnes", "sum"),
        total_area_ha=("cultivated_area_ha", "sum"),
        record_count=("record_id", "count")
    )
    return report.sort_values("total_production_tonnes", ascending=False)


def yearly_report(df):
    report = df.groupby("year", as_index=False).agg(
        total_production_tonnes=("production_tonnes", "sum"),
        total_area_ha=("cultivated_area_ha", "sum"),
        record_count=("record_id", "count")
    )
    report["yield_tonnes_per_ha"] = np.where(
        report["total_area_ha"] > 0,
        report["total_production_tonnes"] / report["total_area_ha"],
        np.nan
    )
    return report.sort_values("year")


def calculate_yearly_change(df):
    report = yearly_report(df).copy()
    report["production_change_tonnes"] = report["total_production_tonnes"].diff()
    previous = report["total_production_tonnes"].shift(1)
    report["percentage_change"] = np.where(
        previous.notna() & (previous != 0),
        (report["total_production_tonnes"] - previous) / previous * 100,
        np.nan
    )
    return report


def data_quality_report(df):
    area = pd.to_numeric(df["cultivated_area_ha"], errors="coerce")
    production = pd.to_numeric(df["production_tonnes"], errors="coerce")
    rainfall = pd.to_numeric(df["rainfall_mm"], errors="coerce")
    quality = {
        "Total records": len(df),
        "Missing crop names": int(df["crop_name"].isna().sum()),
        "Missing region names": int(df["region_name"].isna().sum()),
        "Missing years": int(df["year"].isna().sum()),
        "Missing cultivated area": int(area.isna().sum()),
        "Zero or negative area": int((area <= 0).sum()),
        "Missing production": int(production.isna().sum()),
        "Negative production": int((production < 0).sum()),
        "Missing rainfall": int(rainfall.isna().sum()),
        "Negative rainfall": int((rainfall < 0).sum()),
        "Duplicate crop-region-year records": int(df.duplicated(subset=["crop_name", "region_name", "year"], keep=False).sum()),
    }
    return pd.DataFrame(list(quality.items()), columns=["Check", "Count"])


if __name__ == "__main__":
    df = get_crop_data()
    print("\nALL CROP RECORDS")
    print(calculate_yield(df).to_string(index=False))
    print("\nCROP-WISE REPORT")
    print(crop_wise_report(df).to_string(index=False))
    print("\nREGION-WISE REPORT")
    print(region_wise_report(df).to_string(index=False))
    print("\nYEAR-WISE REPORT")
    print(yearly_report(df).to_string(index=False))
    print("\nYEARLY PRODUCTION CHANGES")
    print(calculate_yearly_change(df).to_string(index=False))
    print("\nDATA QUALITY REPORT")
    print(data_quality_report(df).to_string(index=False))
