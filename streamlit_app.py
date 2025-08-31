import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Car Price Prediction Model",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    /* Fix selectbox text visibility and rounded corners */
    .stSelectbox > div > div {
        background-color: white;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stSelectbox > div > div > div {
        color: #000000 !important;
        border-radius: 10px !important;
    }
    /* Ensure selected text is visible */
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
        border-radius: 10px !important;
    }
    /* Fix placeholder text color */
    .stSelectbox > div > div > div > div > div {
        color: #666666 !important;
    }
    /* Number input styling */
    .stNumberInput > div > div > div > div {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stNumberInput > div > div > div > div > div {
        border-radius: 10px !important;
    }
    /* Button styling */
    .stButton {
        width: 100% !important;
        max-width: none !important;
    }
    .stButton > button {
        width: 100% !important;
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 10px !important;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2);
        max-width: none !important;
        min-width: 100% !important;
        display: block !important;
    }
    .stButton > button:hover {
        background-color: #c82333;
        border-radius: 10px !important;
        box-shadow: 0 6px 8px rgba(220, 53, 69, 0.3);
        transform: translateY(-1px);
    }
    /* Additional selectbox fixes */
    .stSelectbox [data-baseweb="select"] {
        background-color: white;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        color: #000000 !important;
        border-radius: 10px !important;
    }
    /* Focus states for better UX */
    .stSelectbox > div > div:focus-within {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 2px rgba(26, 119, 180, 0.2) !important;
    }
    .stNumberInput > div > div > div > div:focus-within {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 2px rgba(26, 119, 180, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model_and_data():
    """Load the trained model and data with caching"""
    try:
        model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
        df = pd.read_csv('Cleaned_car_data.csv')
        return model, df
    except Exception as e:
        st.error(f"❌ Error loading model or data: {e}")
        return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Car Price Prediction Model</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict the price of your car based on its features</p>', unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #666; margin-bottom: 2rem;'>Made with ❤️ By Shazim Javed</div>", unsafe_allow_html=True)
    # Load model and data
    model, df = load_model_and_data()
    
    if model is None or df is None:
        st.error("Failed to load the model. Please check if the model file exists.")
        return
    
    # Center the form using columns
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("### 📋 Enter Car Details")
        
        # Get unique values for dropdowns
        companies = sorted(df['company'].unique())
        years = sorted(df['year'].unique(), reverse=True)
        fuel_types = sorted(df['fuel_type'].unique())
        
        # Company selection
        selected_company = st.selectbox(
            "Select Company:",
            companies,
            index=None,
            placeholder="Choose a company..."
        )
        
        # Car model selection (dependent on company)
        if selected_company:
            company_models = sorted(df[df['company'] == selected_company]['name'].unique())
            selected_model = st.selectbox(
                "Select Model:",
                company_models,
                index=None,
                placeholder="Choose a model..."
            )
        else:
            selected_model = None
        
        # Year selection
        selected_year = st.selectbox(
            "Select Year:",
            years,
            index=None,
            placeholder="Choose year..."
        )
        
        # Fuel type selection
        selected_fuel_type = st.selectbox(
            "Select Fuel Type:",
            fuel_types,
            index=None,
            placeholder="Choose fuel type..."
        )
        
        # Kilometers driven
        kms_driven = st.number_input(
            "Kilometers Driven:",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000,
            help="Enter the total kilometers the car has been driven"
        )
        
        # Predict button
        if st.button("🚀 Predict Price", type="primary", key="predict_button" ,use_container_width=True):
            if all([selected_company, selected_model, selected_year, selected_fuel_type]):
                try:
                    # Make prediction
                    prediction_input = pd.DataFrame({
                        'name': [selected_model],
                        'company': [selected_company],
                        'year': [selected_year],
                        'kms_driven': [kms_driven],
                        'fuel_type': [selected_fuel_type]
                    })
                    
                    predicted_price = model.predict(prediction_input)[0]
                    predicted_price_multiplied = predicted_price * 3.5
                    predicted_price_rounded = round(predicted_price_multiplied, 2)
                    
                    # Store prediction in session state
                    st.session_state.prediction = predicted_price_rounded
                    st.session_state.car_info = {
                        'company': selected_company,
                        'model': selected_model,
                        'year': selected_year,
                        'fuel_type': selected_fuel_type,
                        'kms_driven': kms_driven
                    }
                    st.session_state.show_prediction = True
                            
                except Exception as e:
                    st.error(f"❌ Error making prediction: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all the required fields!")
        
        # Display prediction result
        if st.session_state.get('show_prediction', False):
            st.success(f"💰 **Estimated Price:** Rs. {st.session_state.prediction:,.0f}")
            
            # Show car details
            car_info = st.session_state.car_info
            st.info(f"""
            **Car Details:**
            - **Company:** {car_info['company']}
            - **Model:** {car_info['model']}
            - **Year:** {car_info['year']}
            - **Fuel Type:** {car_info['fuel_type']}
            - **Kilometers Driven:** {car_info['kms_driven']:,} km
            """)
        else:
            st.info("Click the button above to get the Estimated Price")

if __name__ == "__main__":
    main()
