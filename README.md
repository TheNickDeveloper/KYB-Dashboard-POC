# 🛡 KYB STP Automation Analytics PoC

This Proof of Concept (PoC) project demonstrates an end-to-end analytical dashboard designed to monitor and optimize **Straight-Through Processing (STP)** within a corporate onboarding (KYB) workflow.

---

## 🪴 Application UIUX

![image](https://github.com/TheNickDeveloper/KYB-Dashboard-POC/blob/main/application_uiux.png)

---

## 🧷 Websit Page
[Visit KYB Straight-Through Processing (STP) Dashboard](https://kyb-dashboard-poc.streamlit.app/)

---

## 📑 Dataset Overview (Dummy Data)
The project utilizes a simulated dataset representing corporate application process logs. Each row represents a specific stage in the KYB lifecycle for a given application.

### Key Data Attributes:
* **Case Tracking**: Unique `Case_ID` for each corporate application.
* **Demographics**: Includes `Registration_Country` (e.g., Hong Kong, Singapore, BVI), `Entity_Type`, and `Industry_Sector`.
* **Workflow Stages**: Tracks progress through six critical stages:
    1. Document Collection
    2. Automated Verification
    3. Screening
    4. Risk Scoring
    5. Decision
    6. Activation
* **Processing Mode**: Categorizes each stage as either **Automated** (STP) or **Manual** (requires human intervention).
* **Efficiency Metrics**: Provides `Entry_Timestamp` and `Exit_Timestamp` to calculate processing duration.
* **Exception Logic**: Captures `Exception_Reason` (e.g., "Registry Mismatch", "Fuzzy Name Match") to highlight why cases drop out of the automated flow.

---

## 📊 KYB Dashboard Functions
The Streamlit-based dashboard translates raw process logs into actionable Management Information (MI) through several key views:

* **Real-time KPI Monitoring**: Tracks Total Volume, Overall STP Rate, and Average Processing Time (comparing Auto vs. Manual).
* **Automation Leakage Funnel**: Identifies exactly which stage has the highest "drop-off" rate to manual processing.
* **Geographical Efficiency**: Breaks down STP rates by jurisdiction to identify regional data quality issues.
* **Exception Analysis**: A deep dive into the most frequent manual triggers to prioritize system refinements.
* **Risk-Based Insights**: Correlates Risk Tiers with processing modes to ensure compliance standards are met.

---

## 🛠 Tech Stack

Built with a modern Python-based data stack for rapid prototyping:

* **Language**: [Python 3.9+](https://www.python.org/)
* **Web Framework**: [Streamlit](https://streamlit.io/)
* **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
* **Visualizations**: [Plotly Express](https://plotly.com/python/)
* **Excel Engine**: [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment.

### 2. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas plotly openpyxl
```

### 4. Run the Dashboard
Ensure KYB_Automation_Dummy_Data.xlsx is in the root directory:
```bash
streamlit run kyb_dashboard.py
```

### 5. View Dashboard
Open your browser to http://localhost:8501 to view the live STP analytics.

