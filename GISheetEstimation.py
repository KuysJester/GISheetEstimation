import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from fpdf import FPDF
import time

# Dummy credentials
USER_CREDENTIALS = {
    "Engineering": "Ducting"
}    
# Constants
gi_sheet_max_length = 2.44  # Max Length
gi_sheet_width = 1.22  # Fixed Width

# Set up the page configuration
st.set_page_config(page_title="GI Sheet Estimator", layout="wide")

def login_screen():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFCC00;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;

            /* WalterMart logo as a faint full-page background */
            background-image: url('https://cdn.prod.website-files.com/640ea4106aa3032db2a6cefb/648957c0bed2d0bbb669af38_64588d254fceb101ad84ab07_Waltermart%2520Supermarket%252C%2520Incorporated.png');
            background-repeat: no-repeat;
            background-position: center center;
            background-size: 0%; /* Adjust size as you want */
            opacity: 1; /* keep page fully visible */
            position: relative;
        }
        /* Overlay to reduce logo brightness and increase transparency */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: url('https://cdn.prod.website-files.com/640ea4106aa3032db2a6cefb/648957c0bed2d0bbb669af38_64588d254fceb101ad84ab07_Waltermart%2520Supermarket%252C%2520Incorporated.png');
            background-repeat: no-repeat;
            background-position: center center;
            background-size: 90%;
            opacity: 0.2;  /* Very faint watermark */
            pointer-events: none; /* Allows clicks through */
            z-index: 0;
        }

        /* Added: center the login container */
        .login-container > div {
            width: 100%;
            padding: 2rem 2.5rem 3rem 2.5rem;
            border-radius: 12px;
            opacity: 0.0;
            background-color: #ffffff;
            box-shadow: 0 8px 20px rgba(0, 51, 160, 0.25);
            border: 0px solid #0033A0;
            text-align: center;
        }

        .login-title {
            color: #0033A0;
            font-weight: 500;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            letter-spacing: 0.05em;
            line-height: 1.2;
            white-space: wrap;
            text-align: center;
            width: 100%;
        }
        .login-container input[type="text"], .login-container input[type="password"] {
            width: 100%;
            height: 2.8rem;
            margin-bottom: 1.5rem;
            padding: 0.5rem 0.75rem;
            border: 2px solid #0033A0;
            border-radius: 6px;
            font-size: 1rem;
            background-color: #fff;
            color: #0033A0;
            font-weight: 600;
        }
        .stButton > button {
            width: 100%;
            background-color: #0033A0;
            color: #FFCC00;
            font-weight: 700;
            padding: 0.7rem 0;
            font-size: 1.1rem;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #002070;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="login-container"><div>', unsafe_allow_html=True)

        st.markdown(
            """
            <h1 class="login-title">WM GI SHEET ESTIMATOR LOGIN</h1>
            """,
            unsafe_allow_html=True,
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["logged_in"] = True
            else:
                st.error("Invalid username or password")

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.stop()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_screen()
else:
    st.success("Welcome Engineer!")
    
def tooltip_html(text):
    return f'''
    <style>
    .tooltip {{
      position: relative;
      display: inline-block;
      cursor: help;
      color: #0033A0;
      font-weight: 600;
      font-size: 16px;
      line-height: 1;
      user-select: none;
      margin-left: 2px;
      vertical-align: middle;
    }}
    .tooltip .tooltiptext {{
      visibility: hidden;
      width: 240px;
      background-color: #FFCC00;
      color: #000000;
      text-align: left;
      border-radius: 8px;
      padding: 14px 18px;
      position: absolute;
      z-index: 1000;
      bottom: 140%;
      left: 50%;
      transform: translateX(-50%) scale(0.8);
      opacity: 0;
      transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
      box-shadow: 0 6px 14px rgba(255, 204, 0, 0.6);
      font-size: 14px;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.4;
      pointer-events: none;
      white-space: normal;
      border: 2px solid #0033A0;
    }}
    .tooltip:hover .tooltiptext, .tooltip:focus-within .tooltiptext {{
      visibility: visible;
      opacity: 1;
      pointer-events: auto;
      transform: translateX(-50%) scale(1);
    }}
    .tooltip .tooltiptext::after {{
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      margin-left: -9px;
      border-width: 9px;
      border-style: solid;
      border-color: #FFCC00 transparent transparent transparent;
    }}
    </style>
    <span class="tooltip" tabindex="0" aria-label="info">ⓘ
      <span class="tooltiptext">{text}</span>
    </span>
    '''

def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_screen()

# **Custom CSS for Styling**
st.markdown(
    """
    <style>
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFCC00;
        }
        /* Title */
        h1 {
            color: #003366;
            text-align: center;
        }
        /* Tabs */
        div.stTabs [role="tablist"] button {
            background-color: #003366 !important;
            color: white !important;
            border-radius: 10px !important;
            margin: 2px !important;
        }
        /* Results Cards */
        .result-card {
            background-color: #F4F4F4;
            padding: 10px;
            border-radius: 10px;
            margin: 10px;
            text-align: center;
        }
        .result-card h3 {
            color: #003366;
        }
        /* Buttons */
        .stButton>button {
            background-color: #003366 !important;
            color: white !important;
            border-radius: 5px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **Title**
st.markdown('<h1>🔹 Duct Visualization from GI Sheet 🔹</h1>', unsafe_allow_html=True)

# Sidebar with Inputs
with st.sidebar:
    # Display the logo
    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 1rem;">
            <img src="https://images.squarespace-cdn.com/content/v1/634e3b955d467878d2b0b482/1696438869697-P9QZ872Q97T9UDE4G8CO/Wally_Cover.gif" alt="Wally GIF" style="max-width:100%; height:auto;" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("⚙️ Input Dimensions")

    width = st.number_input("Enter Width (m):", min_value=0.0, format="%.2f", help="Duct width in meters")
    depth = st.number_input("Enter Depth (m):", min_value=0.0, format="%.2f", help="Duct depth in meters")
    length = st.number_input("Enter Length of Duct (m):", min_value=0.0, format="%.2f", help="Total duct length in meters")
    cost_per_sheet = st.number_input("Enter Cost per GI Sheet (PHP):", min_value=0.0, format="%.2f", help="Cost of one GI sheet")

    visualize_button = st.button("🚀 Visualize Duct")

    if st.button("Logout"):
        st.session_state.logged_in = False
        
# **Multi-Sheet Optimization Algorithm**
main_formula_value = 0.1 + (width * 2) + (depth * 2)
sheet_value = np.ceil(length / 1.22)

if main_formula_value > gi_sheet_max_length:
    number_of_sheets = int(sheet_value * 2)
else:
    number_of_sheets = int(sheet_value)

optimized_sheets = np.ceil(main_formula_value / gi_sheet_max_length)
waste_percentage = ((optimized_sheets * gi_sheet_max_length) - main_formula_value) / (optimized_sheets * gi_sheet_max_length) * 100

# **Tabs for Better UI**
tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "🎨 Visualization", "📜 Computation", "📁 Data"])

# **Results Tab**
with tab1:
    st.markdown('<div class="result-card"><h3>📏 Calculation Results</h3></div>', unsafe_allow_html=True)
    st.write(f"✅ **Total Duct Length Required:** {main_formula_value:.2f} m")
    st.write(f"📄 **Sheets Needed:** {sheet_value:.2f} sheets")
    st.write(f"📦 **Optimized Sheets Used:** {optimized_sheets:.0f}")
    
    # **Progress bar for Waste Percentage**
    st.progress(int(waste_percentage))
    st.write(f"🔄 **Material Waste:** {waste_percentage:.2f}%")
     # Doughnut Pie Chart for single sheet usage
    st.markdown("<h3 style='text-align: center;'>Sheet Usage</h3>", unsafe_allow_html=True)

    # Define usage based on the main formula value
    if main_formula_value < gi_sheet_max_length:
        usage = gi_sheet_max_length - main_formula_value
    else:
        usage = gi_sheet_max_length - (0.1 + width + depth)

    remaining = gi_sheet_max_length - usage

    # Pie chart values
    sizes = [usage, remaining]
    labels = ['Loss', 'Used']

    # Create doughnut chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'], wedgeprops=dict(width=0.3))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)

    # Create a DataFrame for tabular representation
    data = {
        'Description': ['Loss Length (m)', 'Used Length (m)'],
        'Value (m)': [usage, remaining]
    }
    df = pd.DataFrame(data)

    # Display the DataFrame in the app
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)  # Close the background div


# **Visualization Tab**
with tab2:
    st.subheader("📐 2D Visualization")
    
    if visualize_button:
        fig, ax = plt.subplots(figsize=(10, 5))

        # We only want to visualize a maximum of 2 sheets
        sheets_to_show = min(number_of_sheets, 2)

        # Calculate the dynamic x-axis limit based on the number of sheets (max 2) and their lengths
        total_length = sheets_to_show * gi_sheet_max_length + (sheets_to_show - 1) * 0.56  # Spacing between sheets

        # Draw rectangles based on the main formula value
        if main_formula_value <= gi_sheet_max_length:
            # Draw a single GI sheet with 5 lines
            positions = [0, 0.1, 0.1 + width, 0.1 + width + depth, 0.1 + width + depth + width, 0.1 + width + depth + width + depth]

            # Display the lines for the single rectangle outside the rectangle
            ax.axvline(x=positions[1], color='purple', linestyle='--', label='Clearance')
            ax.axvline(x=positions[2], color='red', linestyle='--', label=f'Width: {width:.2f} m', linewidth=2)
            ax.axvline(x=positions[3], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m', linewidth=2)
            ax.axvline(x=positions[4], color='red', linestyle='--', label=f'Width: {width:.2f} m', linewidth=2)
            ax.axvline(x=positions[5], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m', linewidth=2)

            # Draw rectangle
            ax.fill_betweenx([0, gi_sheet_width], 0, gi_sheet_max_length, color='green', alpha=0.3)

        else:
            # Fixed positions for two GI sheets with 3 lines each
            for sheet_index in range(2):
                current_position = sheet_index * (gi_sheet_max_length + 0.56)  # Fixed spacing for each sheet
                positions = [current_position + 0.1, 
                             current_position + 0.1 + width, 
                             current_position + 0.1 + width + depth]

                # Display the lines for each sheet
                ax.axvline(x=positions[0], color='purple', linestyle='--', label=f'Clearance (Sheet {sheet_index + 1})')
                ax.axvline(x=positions[1], color='red', linestyle='--', label=f'Width: {width:.2f} m (Sheet {sheet_index + 1})')
                ax.axvline(x=positions[2], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m (Sheet {sheet_index + 1})')

                # Draw rectangle
                ax.fill_betweenx([0, gi_sheet_width], current_position, current_position + gi_sheet_max_length, color='green', alpha=0.3)

        # Show plot
        st.pyplot(fig)

     # Initialize figure
fig = go.Figure()

# **Tab 3: Computation**
with tab3:
    # Display the computation results
    st.markdown("<h3 style='text-align: center;'>📊 Computation</h3>", unsafe_allow_html=True)

    # Show calculation details
    st.write(f"✅ **Total Duct Length Required:** {main_formula_value:.2f} meters")
    st.write(f"📏 **Sheets Needed:** {sheet_value:.2f} sheets")
    st.write(f"📦 **Optimized Sheets Used:** {optimized_sheets:.0f} sheets")
    st.write(f"🔄 **Material Waste:** {waste_percentage:.2f}%")
    
    # Progress bar for material waste
    st.progress(int(waste_percentage))


# **Tab 4: Data Storage & Display**
with tab4:
    # **Styled Header**
    st.markdown(
        """
        <div style="background-color: #FFCC00; padding: 15px; border-radius: 5px; text-align: center;">
            <h2 style="color: black; margin: 0;">📊 Stored Data & Results</h2>
        </div>
        """, unsafe_allow_html=True
    )

    # **Collapsible Section: Computation Results**
    with st.expander("📌 Computation Results", expanded=True):
        st.markdown("<h4 style='text-align: center; color: black;'>Calculation Summary</h4>", unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:18px;'><b>Total Length Required:</b> {main_formula_value} m</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px;'><b>Sheets Needed:</b> {sheet_value} sheets</p>", unsafe_allow_html=True)

        if main_formula_value > gi_sheet_max_length:
            st.markdown(f"<p style='font-size:18px;'><b>Total Sheets Used:</b> {number_of_sheets} sheets (2 Sheets)</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:18px;'><b>Total Sheets Used:</b> {number_of_sheets} sheets (1 Sheet)</p>", unsafe_allow_html=True)

    # **Data Storage Section**
    if 'saved_data' not in st.session_state:
        st.session_state.saved_data = []

    col1, col2 = st.columns([2, 1])  # Layout balance for buttons and table

    with col1:

        # **Save Button Styled**
        if st.button("💾 Save Computation", help="Save current computation results"):
            if len(st.session_state.saved_data) < 20:
                # Placeholder values
                sheet_weight = 10.00  
                total_cost = cost_per_sheet * number_of_sheets  

                # Append data with 2 decimal places for specific fields and no decimal for Sheets Needed and Total Sheets Used
                st.session_state.saved_data.append({
                    'Width (m)': round(width, 2),
                    'Depth (m)': round(depth, 2),
                    'Length (m)': round(length, 2),
                    'Total Length (m)': round(main_formula_value, 2),
                    'Sheets Needed': int(sheet_value),  # Ensure whole number (no decimal)
                    'Total Sheets Used': int(number_of_sheets),  # Ensure whole number (no decimal)
                    'Weight (kg)': round(sheet_weight, 2),
                    'Total Cost (PHP)': round(total_cost, 2)
                })
                st.success("✅ Data saved successfully!")
            else:
                st.warning("⚠️ Maximum of 20 entries reached.")
                

       # **Display Saved Data**
    st.write("### 📁 Stored Computation Data")
    df_saved = pd.DataFrame(st.session_state.saved_data)

    if not df_saved.empty:
        # Ensure all numeric values have only 2 decimal places for the relevant columns
        numeric_columns = ['Width (m)', 'Depth (m)', 'Length (m)', 'Total Length (m)', 
                           'Weight (kg)', 'Total Cost (PHP)',]
        for col in numeric_columns:
            df_saved[col] = pd.to_numeric(df_saved[col], errors='coerce')

        # **Display Data with Correct Formatting**
        st.dataframe(df_saved.style.format({
            'Width (m)': '{:.2f}', 
            'Depth (m)': '{:.2f}',
            'Length (m)': '{:.2f}',
            'Total Length (m)': '{:.2f}',
            'Weight (kg)': '{:.2f}',
            'Total Cost (PHP)': '{:.2f}',
            
        }))

        # **Display Total Sheets Used**
        total_sheets_used = df_saved['Total Sheets Used'].sum()
        st.markdown(f"<h4 style='text-align: center; color: black;'>🛠 Overall Total Sheets Used: {total_sheets_used}</h4>", unsafe_allow_html=True)

        # **Download CSV Button**
        csv = df_saved.to_csv(index=False, float_format="%.2f").encode('utf-8')
        st.download_button("📥 Download CSV", csv, "saved_data.csv", "text/csv", key="download-csv")

        # **Generate & Download PDF**
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "GI Sheet Ducting Estimation Report", ln=True, align='C')

        # **Table Headers**
        for col in df_saved.columns:
            pdf.cell(50, 10, col, 1, 0, 'C')
        pdf.ln()

        # **Table Data**
        for row in df_saved.values:
            for item in row:
                if isinstance(item, (int, float)):  
                    # Ensure 2 decimal places for relevant fields
                    pdf.cell(50, 10, f"{item:.2f}", 1, 0, 'C')  # Ensure 2 decimal places
                else:
                    pdf.cell(50, 10, str(item), 1, 0, 'C')  # Keep text unchanged
            pdf.ln()

        pdf.output("report.pdf")
        with open("report.pdf", "rb") as file:
            st.download_button("📥 Download PDF Report", file, "duct_report.pdf", "application/pdf")

    
# Add rectangle representing the GI sheet
fig.add_shape(
    type="rect",
    x0=0, y0=0,
    x1=2.44, y1=1.22,
    line=dict(color="blue"),
    fillcolor="lightblue"
)

if __name__ == "__main__":
    main()
