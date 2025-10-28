# Medical Device MDL Benchmark Dashboard

Interactive web dashboard for visualizing MAUDE data from 5 major medical device MDL cases.

## 📊 Cases Included

1. **Philips CPAP/BiPAP** (MDL 3014) - W.D. Pennsylvania - Filed: Oct 8, 2021
2. **Bard PowerPort** (MDL 3081) - D. Arizona - Filed: Aug 15, 2023
3. **Hernia Mesh (Bard/Davol)** (MDL 2846) - S.D. Ohio - Filed: Aug 2, 2018
4. **Exactech Joint Implants** (MDL 3044) - E.D. New York - Filed: Jun 14, 2022
5. **Allergan BIOCELL** (MDL 2921) - D. New Jersey - Filed: Dec 18, 2019

## 📈 Features

- **Case Overview**: Total cases, deaths, injuries, and malfunctions across all MDL cases
- **Monthly Trends**: Interactive line charts showing injury/death/malfunction trends over 6-month period before MDL filing
- **Event Distribution**: Pie charts showing breakdown of event types
- **Detailed Tables**: Month-by-month breakdown of events
- **Product Information**: Top product types and device classes for each case
- **Case Comparison**: Switch between different MDL cases to compare patterns

## 🚀 Quick Start

### Option 1: Using Python Server (Recommended)

```bash
cd /Users/praveen/Praveen
python3 scripts/start_dashboard.py
```

This will:
- Start a local web server on port 8080
- Automatically open your browser to http://localhost:8080

### Option 2: Direct File Open

Simply open `frontend/index.html` in your web browser.

## 📁 File Structure

```
Praveen/
├── frontend/
│   ├── index.html          # Main dashboard HTML
│   └── data/
│       └── benchmark_cases_data.json  # Processed case data
├── benchmark_cases/
│   ├── philips_cpap_mdl_3014.xlsx
│   ├── bard_powerport_mdl_3081.xlsx
│   ├── hernia_mesh_(bard_davol)_mdl_2846.xlsx
│   ├── exactech_joint_implants_mdl_3044.xlsx
│   ├── allergan_biocell_mdl_2921.xlsx
│   └── benchmark_cases_summary.xlsx
└── scripts/
    ├── fetch_5_mdl_benchmark_cases.py
    ├── process_benchmark_data_for_frontend.py
    └── start_dashboard.py
```

## 🔄 Updating Data

To refresh the dashboard with updated MAUDE data:

1. **Fetch new MAUDE data** (updates Excel files):
   ```bash
   python3 scripts/fetch_5_mdl_benchmark_cases.py
   ```

2. **Process data for frontend** (generates JSON):
   ```bash
   python3 scripts/process_benchmark_data_for_frontend.py
   ```

3. **Refresh browser** to see updated data

## 📊 Data Summary

Based on 6-month period BEFORE each MDL filing date:

| Case                    | MDL  | Deaths | Injuries | Malfunctions | Total Reports |
|------------------------|------|--------|----------|--------------|---------------|
| Philips CPAP/BiPAP     | 3014 | 44     | 1,066    | 3,121        | 4,232         |
| Bard PowerPort         | 3081 | 12     | 841      | 3,906        | 4,760         |
| Hernia Mesh (Bard)     | 2846 | 17     | 2,359    | 44           | 2,421         |
| Exactech Joints        | 3044 | 0      | 634      | 262          | 896           |
| Allergan BIOCELL       | 2921 | 9      | 189      | 13           | 213           |
| **TOTAL**              |      | **82** | **5,089**| **7,346**    | **12,522**    |

## 💡 Key Insights

- **Hernia Mesh** shows highest injury ratio (97% of reports are injuries)
- **Philips CPAP** has highest total volume (4,232 reports in 6 months)
- **Bard PowerPort** shows highest malfunction count (3,906)
- **Allergan BIOCELL** has smallest volume but highest death rate (4.2%)

## 🛠 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Charts**: Chart.js
- **Data Processing**: Python 3, Pandas
- **Data Source**: FDA MAUDE Database (via OpenFDA API)

## 📝 Notes

- All data represents the **6-month period BEFORE** the MDL filing date
- Event categorization based on FDA MAUDE event_type field
- Product information extracted from generic_name and device_class fields
- Data last updated: Check "Generated" date in dashboard footer

## 🔗 Data Source

FDA MAUDE Database: https://open.fda.gov/data/maude/
