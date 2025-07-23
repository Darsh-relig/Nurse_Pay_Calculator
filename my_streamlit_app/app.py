import streamlit as st
import pandas as pd
import io
import requests
import datetime

# --- Streamlit App Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="Nurse Pay Calculator", layout="centered")
GSA_API_KEY = "JQ2bFDT7uhsuRrPNybGx9zdrUvE9u9yjD7WoVSk0"
# --- Custom CSS for minimalistic design and color palette (inspired by reference UI) ---
st.markdown(
    """
    <style>
    /* Overall page background and general text */
    html, body {
        background-color: #f0f2f6; /* Very light gray background for the overall page */
        color: #000000; /* Changed to black for better visibility on light background */
        font-family: 'Inter', sans-serif; /* Using a clean, modern font */
    }

    /* Main container for the calculator card - white background, rounded corners, shadow 
    .main-calculator-card {
        background-color: #ffffff; /* Pure white background for the card */
        border-radius: 20px; /* More rounded corners like the image */
        padding: 40px; /* Increased padding */
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1); /* Softer, larger shadow */
        margin-top: 30px;
        margin-bottom: 30px;
        max-width: 800px; /* Constrain width for a more calculator-like feel */
        margin-left: auto;
        margin-right: auto;
    }*/

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50; /* Darker blue for headings */
        font-weight: 600; /* Slightly bolder headings */
        margin-bottom: 15px;
    }
    h1 {
        font-size: 2.2em; /* Slightly smaller main title to fit card */
        color: #4a4a4a;
        text-align: left; /* Align left like the image */
        margin-bottom: 25px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e0e0e0; /* Subtle separator */
    }
    h2 {
        font-size: 1.6em; /* Adjusted h2 size */
        border-bottom: none; /* Remove border from h2 */
        padding-bottom: 0;
        margin-bottom: 15px;
    }
    h3 {
        font-size: 1.2em; /* Adjusted h3 size */
        color: #555;
    }


    /* Buttons */
    .stButton > button {
        background-color: #4666ff; /* Blue from reference */
        color: white; /* Text color for buttons */
        border-radius: 8px; /* Rounded corners */
        border: none;
        padding: 14px 0; /* Adjusted padding */
        font-size: 1.1em;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 10px rgba(70, 102, 255, 0.15); /* Blue shadow */
        cursor: pointer;
        width: 100%; /* Make buttons full width in their column */
        margin-top: 20px; /* Space above buttons */
    }
    .stButton > button:hover {
        background-color: #2747c7; /* Darker blue on hover */
        transform: translateY(-2px); /* Slight lift effect */
        box-shadow: 0 6px 15px rgba(70, 102, 255, 0.25);
    }

    /* Text Inputs, Selectboxes, and Sliders */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div > div > div:first-child {
        border-radius: 8px;
        border: 1px solid #e0e0e0; /* Very light gray border */
        padding: 10px 15px;
        font-size: 1em;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.03); /* Very subtle inner shadow */
        background-color: #fcfcfc; /* Slightly off-white input background */
        color: #000000; /* Ensure input text is black */
    }
    /* Labels for inputs */
    .stTextInput > label, .stSelectbox > label, .stSlider > label {
        font-weight: 500;
        color: #555; /* Slightly softer label color */
        margin-bottom: 5px;
        font-size: 0.95em; /* Slightly smaller labels */
    }
    /* Slider container styling */
    .stSlider > div > div > div > div[data-baseweb="slider"] {
        border-radius: 8px; /* Match input border radius */
        border: 1px solid #e0e0e0; /* Match input border */
        background-color: #fcfcfc; /* Match input background */
        padding: 10px 15px; /* Add padding to slider container */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.03);
    }
    /* Slider track color */
    .stSlider > div > div > div > div > div[data-baseweb="slider"] > div:first-child > div:first-child {
        background-color: #e0e0e0 !important; /* Light gray track */
    }
    /* Slider fill color */
    .stSlider > div > div > div > div > div[data-baseweb="slider"] > div:first-child > div:last-child {
        background-color: #6a5acd !important; /* Purple fill for consistency with original design */
    }
    /* Slider thumb color */
    .stSlider > div > div > div > div > div[data-baseweb="slider"] > div:last-child {
        background-color: #6a5acd !important; /* Purple thumb */
        border: 2px solid #6a5acd !important;
    }
    /* Force slider value text to black */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-testid="stTickBar"] span,
    .stSlider [data-testid="stSliderValue"] {
        color: #000 !important;
    }
    .stSlider [data-testid="stSliderValue"] {
        background: #fff !important;
        border: 1px solid #e0e0e0 !important;
    }


    /* Metrics - redesigned to look like the image's "Loan amount" */
    .stMetric {
        background-color: transparent; /* No background for metrics */
        border-radius: 0; /* No border radius */
        padding: 0;
        margin-bottom: 20px; /* Space between metrics */
        box-shadow: none; /* No shadow */
        border: none; /* No border */
    }
    .stMetric > label {
        color: #666; /* Softer label color */
        font-weight: 500;
        font-size: 1em; /* Normal label size */
        margin-bottom: 5px;
    }
    .stMetric > div > div:first-child {
        color: #2c3e50; /* Darker blue for metric values */
        font-weight: 700;
        font-size: 2.5em; /* Significantly larger metric value font size */
        margin-top: 0; /* Remove top margin */
    }
    .stMetric > div > div:last-child { /* Help text for metrics */
        font-size: 0.85em;
        color: #888;
        margin-top: 5px;
    }

    /* Info, Warning, Error messages */
    .stAlert {
        border-radius: 8px;
        padding: 12px 18px;
        font-size: 1em;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .stAlert.info {
        background-color: #e6f7ff; /* Lighter blue */
        color: #0056b3;
        border-left: 5px solid #007bff;
    }
    .stAlert.warning {
        background-color: #fffbe6; /* Lighter yellow */
        color: #997a00;
        border-left: 5px solid #ffbf00;
    }
    .stAlert.error {
        background-color: #ffe6e6; /* Lighter red */
        color: #b30000;
        border-left: 5px solid #cc0000;
    }

    /* Horizontal Rule */
    hr {
        border-top: 1px solid #e0e0e0;
        margin-top: 25px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_annual_per_diem_from_gsa_api(zip_code, fiscal_year):
    """
    Fetches all monthly lodging and the M&IE rate for a given ZIP code and fiscal year
    from the GSA Per Diem API using the direct ZIP code endpoint.

    Args:
        zip_code (str): The ZIP code for which to fetch rates.
        fiscal_year (int): The GSA fiscal year (e.g., 2025 for FY2025).

    Returns:
        dict: A dictionary mapping month names (e.g., "January") to (lodging_rate, mie_rate) tuples,
              or None if fetching fails or no data is found.
    """
    
    # --- Using the direct ZIP code endpoint: /rates/zip/{zip}/year/{year} ---
    api_url = f"https://api.gsa.gov/travel/perdiem/v2/rates/zip/{zip_code}/year/{fiscal_year}"
    
    st.info(f"Attempting to fetch annual per diem data from GSA API for ZIP: {zip_code}, Fiscal Year: {fiscal_year}...")
    
    annual_rates = {} # To store {month_name: (lodging, mie)}

    try:
        # Changed header key from "api_key" to "X-API-KEY"
        response = requests.get(api_url, headers={"X-API-KEY": GSA_API_KEY})
        response.raise_for_status() # Raise an HTTPError for bad responses
        data = response.json()

        # --- Debugging: Display raw API response (Removed for cleaner UI, but can be re-added conditionally) ---
        # st.subheader("Raw API Response (for debugging)")
        # st.json(data)
        # --- End Debugging ---

        if data and 'rates' in data and data['rates']:
            found_rate_info_container = None
            # Ensure zip_code from input is stripped of whitespace
            clean_input_zip = str(zip_code).strip() 
            
            # Iterate through the top-level 'rates' array
            for item in data['rates']:
                # The actual per diem details are within 'item.get('rate')' which is a list
                if item.get('rate') and isinstance(item['rate'], list) and len(item['rate']) > 0:
                    # Get the first (and likely only) item from the 'rate' list
                    actual_per_diem_details = item['rate'][0]
                    
                    api_zip = actual_per_diem_details.get('zip')
                    # Ensure API zip is also stripped of whitespace for comparison
                    clean_api_zip = str(api_zip).strip() if api_zip is not None else None

                    # st.info(f"Comparing API zip '{clean_api_zip}' (type: {type(clean_api_zip)}) with input zip '{clean_input_zip}' (type: {type(clean_input_zip)})") # Removed for cleaner UI

                    if clean_api_zip == clean_input_zip:
                        found_rate_info_container = item # Store the container to access nested details
                        break
            
            if found_rate_info_container:
                # Get the actual per diem details from the nested 'rate' list
                actual_per_diem_details = found_rate_info_container['rate'][0]

                mie_rate = actual_per_diem_details.get('meals')
                
                if mie_rate is None:
                    st.warning(f"M&IE rate not found for ZIP {zip_code} in FY{fiscal_year}. Data might be incomplete.")
                    return None

                # Lodging rates are within 'months' array inside 'rate'
                if 'months' in actual_per_diem_details and 'month' in actual_per_diem_details['months']:
                    for month_detail in actual_per_diem_details['months']['month']:
                        month_long_name = month_detail.get('long') # Get the full month name
                        lodging_val = month_detail.get('value')
                        if month_long_name is not None and lodging_val is not None:
                            # Store by long month name as requested by user for dropdown
                            annual_rates[month_long_name] = (float(lodging_val), mie_rate)
                
                if annual_rates:
                    st.success(f"Successfully fetched annual per diem data for ZIP {zip_code}, FY{fiscal_year}.")
                    return annual_rates
                else:
                    st.warning(f"No monthly lodging rates found for ZIP {zip_code} in FY{fiscal_year}. Data might be incomplete or not available via this endpoint.")
                    return None
            else:
                st.warning(f"No specific rate info found for ZIP {zip_code} within the API response for FY{fiscal_year}. Response structure might be unexpected.")
                return None
        else:
            st.warning(f"No rates data found from GSA API for ZIP {zip_code} for FY{fiscal_year}. Response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching annual per diem rates from GSA API: {e}. This is likely due to an invalid or unauthorized API key. Please ensure your GSA_API_KEY is correct and has the necessary permissions.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred processing GSA API response: {e}")
        return None

# --- Main Application Layout ---
# Wrap the entire content in a div to create the card-like effect
st.markdown('<div class="main-calculator-card">', unsafe_allow_html=True)

st.title("💰 Nurse Pay Calculator")

# Removed the introductory markdown text for a cleaner look like the reference image

# Create two columns for input and output sections
# The reference image has inputs on the left, and results on the right, but a more compact layout.
# We will use columns for input fields, and then display results below them within the same card.

st.header("Input Your Details")

# Grouping inputs into columns for a more compact layout
col1, col2, col3 = st.columns(3)

with col1:
    zip_code_input = st.text_input("ZIP Code", "", help="e.g., 20032")

with col2:
    current_year = datetime.datetime.now().year
    years_to_offer = list(range(current_year - 2, current_year + 2))
    selected_fiscal_year = st.selectbox(
        "Fiscal Year",
        options=years_to_offer,
        index=years_to_offer.index(current_year + 1) if (current_year + 1) in years_to_offer else len(years_to_offer) - 1,
        help="GSA fiscal year (e.g., FY2025 runs from Oct 1, 2024 to Sep 30, 2025)"
    )

# Use session state to store fetched annual rates
if 'annual_per_diem_data' not in st.session_state:
    st.session_state.annual_per_diem_data = None
if 'selected_month_for_display' not in st.session_state:
    current_month_long_name = datetime.date(1900, datetime.datetime.now().month, 1).strftime('%B')
    st.session_state.selected_month_for_display = current_month_long_name

# Fetch Annual Per Diem Data button
if st.button("Fetch Annual Per Diem Data"):
    if zip_code_input:
        fetched_data = get_annual_per_diem_from_gsa_api(zip_code_input, selected_fiscal_year)
        st.session_state.annual_per_diem_data = fetched_data
        current_month_long_name = datetime.date(1900, datetime.datetime.now().month, 1).strftime('%B')
        if fetched_data and current_month_long_name in fetched_data:
            st.session_state.selected_month_for_display = current_month_long_name
        elif fetched_data:
            st.session_state.selected_month_for_display = sorted(fetched_data.keys())[0]
        else:
            st.session_state.selected_month_for_display = None
    else:
        st.warning("Please enter a ZIP Code to fetch per diem rates.")
        st.session_state.annual_per_diem_data = None
        st.session_state.selected_month_for_display = None

# Display month selection only if annual data is available
lodging_per_day = None
mie_per_day = None

if st.session_state.annual_per_diem_data:
    available_month_names = sorted(st.session_state.annual_per_diem_data.keys(), 
                                   key=lambda m: datetime.datetime.strptime(m, '%B').month)

    with col3: # Place month selector in the third column
        default_month_index = 0
        if st.session_state.selected_month_for_display and st.session_state.selected_month_for_display in available_month_names:
            default_month_index = available_month_names.index(st.session_state.selected_month_for_display)
        elif available_month_names:
            st.session_state.selected_month_for_display = available_month_names[0]
            default_month_index = 0
        else:
            st.session_state.selected_month_for_display = None
            default_month_index = 0

        selected_month_name = st.selectbox(
            "Month", # Changed label to just "Month"
            options=available_month_names if available_month_names else [],
            index=default_month_index,
            key="month_selector"
        )
        st.session_state.selected_month_for_display = selected_month_name

    if selected_month_name and selected_month_name in st.session_state.annual_per_diem_data:
        lodging_per_day, mie_per_day = st.session_state.annual_per_diem_data[selected_month_name]
        st.markdown(f"**Per Diem Rates for {selected_month_name}**: Lodging: ${lodging_per_day:,.2f}/day, M&IE: ${mie_per_day:,.2f}/day")
    else:
        st.warning(f"No per diem rates found for the selected month in the fetched annual data.")
        lodging_per_day = None
        mie_per_day = None
else:
    st.info("Enter a ZIP Code and Fiscal Year, then click 'Fetch Annual Per Diem Data' to retrieve rates.")

st.markdown("---") # Separator before other inputs

# Other inputs in a more compact layout
col4, col5, col6 = st.columns(3)
with col4:
    hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=70.0, format="%.2f")
with col5:
    weekly_hours = st.number_input("Weekly Hours", min_value=0.0, value=36.0, format="%.2f")
with col6:
    suggested_tax_percentage = st.slider("Suggested Tax %", min_value=0, max_value=50, value=25)

# Calculate Button
if st.button("Calculate Pay"):
    # Store calculation results in session state to display in output column
    if lodging_per_day is not None and mie_per_day is not None:
        # Formulas based on user's provided Excel sheet logic:
        excel_gross_weekly_pay = hourly_rate * weekly_hours 
        excel_per_diem_rate = (lodging_per_day + mie_per_day) * 7 

        if excel_per_diem_rate > excel_gross_weekly_pay:
            estimated_tax_deduction = 0.0
        else:
            taxable_base = excel_gross_weekly_pay - excel_per_diem_rate
            estimated_tax_deduction = taxable_base * (suggested_tax_percentage / 100)
        
        if excel_per_diem_rate > excel_gross_weekly_pay:
            take_home_pay = excel_gross_weekly_pay
        else:
            take_home_pay = excel_gross_weekly_pay - estimated_tax_deduction

        effective_hourly_rate = 0.0
        if weekly_hours > 0:
            effective_hourly_rate = take_home_pay / weekly_hours

        st.session_state.calculated_results = {
            "excel_gross_weekly_pay": excel_gross_weekly_pay,
            "excel_per_diem_rate": excel_per_diem_rate,
            "estimated_tax_deduction": estimated_tax_deduction,
            "take_home_pay": take_home_pay,
            "effective_hourly_rate": effective_hourly_rate,
            "hourly_rate": hourly_rate, # Store inputs for display
            "weekly_hours": weekly_hours,
            "suggested_tax_percentage": suggested_tax_percentage
        }
    else:
        st.warning("Please fetch annual per diem data and select a month before calculating pay.")
        st.session_state.calculated_results = None # Clear results if calculation fails

# Display results below the inputs, within the same card
if st.session_state.get('calculated_results'):
    results = st.session_state.calculated_results
    st.markdown("---") # Separator before results
    st.header("Results") # Changed title for results section

    # Display main calculated values using the metric style from the reference
    col_loan_amt, col_est_pm = st.columns(2)
    with col_loan_amt:
        st.markdown(f"""
        <div class='metric-label'>Gross Weekly $</div>
        <div class='metric-value'>${results['excel_gross_weekly_pay']:,.0f}</div>
        """, unsafe_allow_html=True)
    with col_est_pm:
        st.markdown(f"""
        <div class='metric-label'>Per-Diem Rate($)</div>
        <div class='metric-value'>${results['excel_per_diem_rate']:,.0f}</div>
        """, unsafe_allow_html=True)

    st.markdown("---") # Separator

    # Other metrics in a compact layout
    col_tax_ded, col_take_home, col_eff_hr = st.columns(3)
    with col_tax_ded:
        st.metric(label="Estimated Tax Deduction ($)", value=f"${results['estimated_tax_deduction']:,.2f}")
    with col_take_home:
        st.metric(label="Take-Home Pay ($)", value=f"**${results['take_home_pay']:,.2f}**")
    with col_eff_hr:
        st.metric(label="Effective Hourly Rate ($)", value=f"${results['effective_hourly_rate']:,.2f}")

    # Minimum Wage Metrics (can be placed below or integrated more compactly if desired)
    col_min_hr, col_min_wk = st.columns(2)
    with col_min_hr:
        minimum_wage_per_hour = 15.00
        st.metric(label="Minimum Wage per Hour", value=f"${minimum_wage_per_hour:,.2f}")
    with col_min_wk:
        weekly_minimum_wage = minimum_wage_per_hour * results['weekly_hours']
        st.metric(label="Weekly Minimum Wage", value=f"${weekly_minimum_wage:,.2f}")

    # Alert if Effective Hourly Rate is less than $15
    if results['effective_hourly_rate'] < 15 and results['weekly_hours'] > 0:
        st.warning(f"⚠️ Warning: The Effective Hourly Rate (${results['effective_hourly_rate']:,.2f}) is less than $15.00.")
    elif results['weekly_hours'] == 0:
        st.info("Effective Hourly Rate cannot be calculated as Weekly Hours are 0.")
else:
    st.info("Click 'Calculate Pay' to see the estimated weekly pay breakdown here.")


st.markdown("---")
st.info("Note: This is an estimation. Actual pay may vary based on specific tax situations, deductions, and company policies.")

# Close the main calculator card div
st.markdown('</div>', unsafe_allow_html=True)
