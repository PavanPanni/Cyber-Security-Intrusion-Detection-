import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder
import plotly.express as px

# Function to preprocess data
def preprocess_data(data, model):
    session_ids = data['session_id']
    data = data.drop(['attack_detected', 'session_id'], axis=1, errors='ignore')
    
    categorical_cols = ['protocol_type', 'encryption_used', 'browser_type']
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_data = encoder.fit_transform(data[categorical_cols])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))
    data = pd.concat([data.drop(categorical_cols, axis=1), encoded_df], axis=1)

    model_features = model.feature_names_in_
    for feature in model_features:
        if feature not in data.columns:
            data[feature] = 0

    return data[model_features], session_ids

# Function to determine reasons for attack detection
def get_alert_reason(row):
    reasons = []
    if 'network_packet_size' in row and row['network_packet_size'] > 1000:
        reasons.append("Large network packet size")
    if 'failed_logins' in row and row['failed_logins'] > 3:
        reasons.append("Multiple failed login attempts")
    if 'ip_reputation_score' in row and row['ip_reputation_score'] < 20:
        reasons.append("Low IP reputation score")
    if 'unusual_time_access' in row and row['unusual_time_access'] == 1:
        reasons.append("Access at unusual time")
    
    return ", ".join(reasons) if reasons else "No suspicious activity detected"

# Main app logic
def main():
    st.title("🔒 Cybersecurity Intrusion Detection App")

    # Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["📂 CSV Prediction", "🚨 Real-time Alerts", "📊 Data Visualization"])

    # Tab 1 - CSV Prediction
    with tab1:
        uploaded_file = st.file_uploader("Upload CSV file for prediction", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.write("Uploaded Data Preview:")
            st.write(data.head())

            model = joblib.load("model.pkl")
            processed_data, session_ids = preprocess_data(data, model)
            predictions = model.predict(processed_data)

            result_df = pd.DataFrame({'session_id': session_ids, 'attack_detected': predictions})
            st.write("Prediction Results:")
            st.write(result_df)
    
    # Tab 2 - Real-time Alerts
    with tab2:
        st.subheader("🚨 Real-time Alerts")
        if uploaded_file is not None:
            alert_data = pd.DataFrame({'session_id': session_ids, 'attack_detected': predictions})
            alert_data['reason'] = processed_data.apply(get_alert_reason, axis=1)
            
            for index, row in alert_data.iterrows():
                if row['attack_detected'] == 1:
                    st.write(f"Session {row['session_id']}: ⚠ Intrusion Detected - {row['reason']}")
                else:
                    st.write(f"Session {row['session_id']}: ✅ Safe Session")
        else:
            st.warning("Please upload a CSV file in the Prediction tab to see real-time alerts.")

    # Tab 3 - Data Visualization
    with tab3:
        st.subheader("📊 Data Visualization")
        if uploaded_file is not None:
            pie_chart = pd.DataFrame({'Status': ['Detected Attacks', 'Safe Sessions'], 'Count': [sum(predictions), len(predictions) - sum(predictions)]})
            fig = px.pie(pie_chart, values='Count', names='Status', title='Intrusion Detection Overview', color_discrete_map={'Detected Attacks': '#d32f2f', 'Safe Sessions': '#4CAF50'})
            st.plotly_chart(fig)
        else:
            st.warning("Please upload a CSV file in the Prediction tab to visualize data.")

if __name__ == "__main__":
    main()
