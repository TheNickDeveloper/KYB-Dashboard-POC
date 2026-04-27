from kyb_dashboard import KYBDashboard

if __name__ == "__main__":
    # --- CONFIGURATION ---
    DATA_FILE = "dataset/KYB_Automation_Dummy_Data.xlsx"
    PAGE_TITLE = "KYB STP Automation Dashboard"
    STAGE_ORDER = ["Document Collection", "Automated Verification", "Screening", "Risk Scoring", "Decision", "Activation"]
    COLOR_MAP = {"Automated": "#00CC96", "Manual": "#EF553B"}
    
    dashboard = KYBDashboard(DATA_FILE, PAGE_TITLE, STAGE_ORDER, COLOR_MAP)
    dashboard.render()