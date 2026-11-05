import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from backend.analysis import (
    get_crop_data,
    yearly_report,
    crop_wise_report,
    calculate_yield
)
# Save graphs inside the project's static folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
# Graph 1: Year-wise production
def create_production_chart():
    df = get_crop_data()
    yearly = yearly_report(df)
    plt.figure(figsize=(8, 5))
    plt.bar(
        yearly["year"].astype(str),
        yearly["total_production_tonnes"]
    )
    plt.title("Year-wise Crop Production")
    plt.xlabel("Year")
    plt.ylabel("Production (tonnes)")
    plt.tight_layout()
    plt.savefig(
        os.path.join(STATIC_DIR, "production_chart.png")
    )
    plt.close()
# Graph 2: Crop-wise production
def create_crop_chart():
    df = get_crop_data()
    report = crop_wise_report(df)
    plt.figure(figsize=(8, 5))
    plt.bar(
        report["crop_name"],
        report["total_production_tonnes"]
    )
    plt.title("Crop-wise Production Comparison")
    plt.xlabel("Crop")
    plt.ylabel("Production (tonnes)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(
        os.path.join(STATIC_DIR, "crop_chart.png")
    )
    plt.close()
# Graph 3: Year-wise yield
def create_yield_chart():
    df = calculate_yield(get_crop_data())
    yearly = df.groupby("year", as_index=False).agg(
        total_area=("cultivated_area_ha", "sum"),
        total_production=("production_tonnes", "sum")
    )
    yearly = yearly[yearly["total_area"] > 0].copy()
    yearly["yield"] = (
        yearly["total_production"] / yearly["total_area"]
    )
    plt.figure(figsize=(8, 5))
    plt.plot(
        yearly["year"],
        yearly["yield"],
        marker="o"
    )
    plt.title("Year-wise Crop Yield")
    plt.xlabel("Year")
    plt.ylabel("Production per hectare (tonnes/ha)")
    plt.tight_layout()
    plt.savefig(
        os.path.join(STATIC_DIR, "yield_chart.png")
    )
    plt.close()
# Run all three graphs
if __name__ == "__main__":
    create_production_chart()
    create_crop_chart()
    create_yield_chart()
    print("All three graphs created successfully.")
    print("Check the project's static folder.")
