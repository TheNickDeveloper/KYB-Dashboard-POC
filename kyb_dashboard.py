import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard class for KYB STP Automation metrics and visualizations.
class KYBDashboard:
    # Initialize the dashboard by loading data and calculating KPIs.
    def __init__(self, data_file=str, page_title=str, stage_order=str, color_map=str):
        self.data_file = data_file
        self.page_title = page_title
        self.stage_order = stage_order
        self.color_map = color_map

        self.loaded_df = self.load_data()
        self.kpis = self.calculate_kpis()

    def load_data(self) -> pd.DataFrame:
        try:
            df = pd.read_excel(self.data_file)
            df['Entry_Timestamp'] = pd.to_datetime(df['Entry_Timestamp'])
            df['Exit_Timestamp'] = pd.to_datetime(df['Exit_Timestamp'])
            df['Duration_Min'] = (df['Exit_Timestamp'] - df['Entry_Timestamp']).dt.total_seconds() / 60
            return df
        except FileNotFoundError:
            st.error(f"Data file '{self.data_file}' not found. Please ensure it exists in the directory.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()

    def calculate_kpis(self):
        if self.loaded_df.empty:
            return {}

        total_apps = self.loaded_df['Case_ID'].nunique()
        manual_cases = self.loaded_df[self.loaded_df['Processing_Mode'] == 'Manual']['Case_ID'].unique()
        stp_cases_count = total_apps - len(manual_cases)
        stp_rate = (stp_cases_count / total_apps) * 100 if total_apps > 0 else 0

        avg_auto_time = self.loaded_df[self.loaded_df['Processing_Mode'] == 'Automated']['Duration_Min'].mean()
        avg_manual_time = self.loaded_df[self.loaded_df['Processing_Mode'] == 'Manual']['Duration_Min'].mean()

        return {
            'total_apps': total_apps,
            'stp_rate': stp_rate,
            'avg_auto_time': avg_auto_time,
            'avg_manual_time': avg_manual_time
        }

    def create_funnel_chart(self):
        funnel_df = self.loaded_df.groupby(['Stage', 'Processing_Mode']).size().reset_index(name='Volume')
        fig = px.funnel(funnel_df, x='Volume', y='Stage', color='Processing_Mode',
                        category_orders={"Stage": self.stage_order},
                        color_discrete_map=self.color_map,
                        title="Where do cases drop out of Automation?")
        return fig

    def create_country_chart(self):
        """
        Create the STP rate by country chart.

        Returns:
            plotly.graph_objects.Figure: Bar chart figure.
        """
        country_mode = self.loaded_df.groupby(['Registration_Country', 'Processing_Mode']).size().unstack(fill_value=0)
        country_mode['STP_Rate'] = (country_mode['Automated'] / (country_mode['Automated'] + country_mode['Manual'])) * 100
        country_mode = country_mode.reset_index()
        fig = px.bar(country_mode, x='Registration_Country', y='STP_Rate',
                     title="Regional Infrastructure Readiness",
                     labels={'STP_Rate': 'STP %'},
                     color_discrete_sequence=['#636EFA'])
        return fig

    def create_exceptions_chart(self):
        """
        Create the top manual exception reasons pie chart.

        Returns:
            plotly.graph_objects.Figure: Pie chart figure.
        """
        exceptions = self.loaded_df[self.loaded_df['Exception_Reason'] != 'N/A']['Exception_Reason'].value_counts().reset_index()
        exceptions.columns = ['Reason', 'Count']
        fig = px.pie(exceptions, values='Count', names='Reason', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        return fig

    def create_risk_chart(self):
        """
        Create the risk tier vs processing mode bar chart.

        Returns:
            plotly.graph_objects.Figure: Bar chart figure.
        """
        risk_mode = self.loaded_df.groupby(['Risk_Tier', 'Processing_Mode']).size().reset_index(name='Count')
        fig = px.bar(risk_mode, x='Risk_Tier', y='Count', color='Processing_Mode',
                     barmode='group', title="Do High Risk tiers force Manual reviews?",
                     color_discrete_map=self.color_map)
        return fig

    def render(self):
        """
        Render the Streamlit dashboard UI.
        """
        st.set_page_config(page_title=self.page_title, layout="wide")

        st.title("📊 KYB Straight-Through Processing (STP) Dashboard")
        st.markdown("### Process: Doc Collection → Verification → Screening → Risk → Decision → Activation")

        # KPIs Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Applications", self.kpis.get('total_apps', 0))
        col2.metric("Overall STP Rate", f"{self.kpis.get('stp_rate', 0):.1f}%")
        col3.metric("Avg. Auto Time", f"{self.kpis.get('avg_auto_time', 0):.1f}m")
        col4.metric("Avg. Manual Time", f"{self.kpis.get('avg_manual_time', 0):.1f}m")

        st.divider()

        # Charts Row 1
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Automation Leakage Funnel")
            st.plotly_chart(self.create_funnel_chart(), use_container_width=True)

        with col_b:
            st.subheader("STP Rate by Country")
            st.plotly_chart(self.create_country_chart(), use_container_width=True)

        # Charts Row 2
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Top Manual Exception Reasons")
            st.plotly_chart(self.create_exceptions_chart(), use_container_width=True)

        with col_d:
            st.subheader("Risk Tier vs. Processing Mode")
            st.plotly_chart(self.create_risk_chart(), use_container_width=True)

        # Data Table
        with st.expander("View Full Audit Trail (Detailed Records)"):
            st.dataframe(self.loaded_df)