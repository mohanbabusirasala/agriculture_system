# Agriculture Crop Production Analysis System

A simple web application for analyzing crop production data and generating useful agricultural insights.

## About the Project
This project helps users view crop-related information, upload CSV data, analyze production trends, and generate reports for different regions and years.

## Features
- View crop and region details
- Upload crop data in CSV format
- Analyze crop production by year
- Check crop yield and rainfall data
- Generate reports and charts
- Manage farmer and crop records

## Technologies Used
- Python
- Flask
- HTML
- CSS
- Pandas
- NumPy
- MySQL
- Matplotlib

## Project Structure

```text
agriculture_crop_production_analysis_system-main/
├── app.py
├── requirements.txt
├── agriculture_db.sqlite3
├── backend/
│   ├── analysis.py
│   ├── charts.py
│   └── config.py
├── database/
├── static/
├── templates/
├── upload/
└── README.md
```

## How to Run
1. Clone the repository.
2. Open the project folder.
3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start the application:

```bash
python app.py
```

6. Open the browser and go to:

```text
http://127.0.0.1:5000/
```

## Purpose
The goal of this system is to help analyze agricultural crop production data and present useful information through reports and visualizations.

## Notes
- CSV files should contain crop, region, year, cultivated area, production, and rainfall data.
- Make sure the database configuration is set correctly before running the app.
