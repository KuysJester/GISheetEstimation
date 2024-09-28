import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
gi_sheet_max_length = 2.44  # Max Length
gi_sheet_width = 1.22  # Fixed Width

# Set up the page configuration
st.set_page_config(page_title="GI Sheet Estimator", layout="wide")
st.markdown('<h1 style="text-align: center;">Duct Visualization from GI Sheet</h1>', unsafe_allow_html=True)

# Sidebar section with input fields
with st.sidebar:
    # Header and Logo
    st.header("Input Dimensions")
    
    # Input fields
    width = st.number_input("Enter Width (m):", min_value=0.0, format="%.2f")  # No maximum limit on width
    depth = st.number_input("Enter Depth (m):", min_value=0.0, format="%.2f")
    length = st.number_input("Enter Length of Duct (m):", min_value=0.0, format="%.2f")

    # Visualize Duct button placed after all input fields
    visualize_button = st.sidebar.button("Visualize Duct")

    # Add spacer to push the footer down
    st.write("")  # Adds space
    st.write("")  # You can add more blank lines if needed for spacing

    # Footer with the logo at the top
    st.markdown('<div class="footer">WalterMart Duct Visualization Tool © 2024</div>', unsafe_allow_html=True)

# Calculate total length required to fold the duct using the main formula
main_formula_value = 0.1 + (width * 2) + (depth * 2)

# Determine the number of sheets needed based on the length
sheet_value = np.ceil(length / 1.22)  # Round up the sheet value

# Multiply the number of sheets by sheet_value if main formula > 2.44
if main_formula_value > gi_sheet_max_length:
    number_of_sheets = int(sheet_value * 2)  # Multiply by 2 if main formula exceeds 2.44 meters
else:
    number_of_sheets = int(sheet_value)

# Columns with adjusted space and background colors
left_column, middle_column, right_column = st.columns([3, 6, 3])  # Adjusting space: 3:5:3 ratio

# Set background color for left column
with left_column:
    st.markdown('<div style="background-color: #FFCC00; padding: 10px; border-radius: 5px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Usage</h2>", unsafe_allow_html=True)
    
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

# Set background color for middle column
with middle_column:
    st.markdown('<div style="background-color: #FFCC00; padding: 10px; border-radius: 5px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>2D Display</h2>", unsafe_allow_html=True)
    
    # Visualize the duct based on the main formula value, with a maximum of 2 sheets shown
    if visualize_button:  # Use the button click event here
        with st.container():
            st.markdown('<div class="plot-section">', unsafe_allow_html=True)
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
                plt.axvline(x=positions[1], color='purple', linestyle='--', label='Clearance')
                plt.axvline(x=positions[2], color='red', linestyle='--', label=f'Width: {width:.2f} m', linewidth=2)
                plt.axvline(x=positions[3], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m', linewidth=2)
                plt.axvline(x=positions[4], color='red', linestyle='--', label=f'Width: {width:.2f} m', linewidth=2)
                plt.axvline(x=positions[5], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m', linewidth=2)

                # Draw rectangle
                plt.fill_betweenx([0, gi_sheet_width], 0, gi_sheet_max_length, color='green', alpha=0.3)

            else:
                # Fixed positions for two GI sheets with 3 lines each
                for sheet_index in range(2):
                    current_position = sheet_index * (gi_sheet_max_length + 0.56)  # Fixed spacing for each sheet
                    positions = [current_position + 0.1, 
                                 current_position + 0.1 + width, 
                                 current_position + 0.1 + width + depth]

                    # Display the lines for each sheet
                    plt.axvline(x=positions[0], color='purple', linestyle='--', label='Clearance (sheet {})'.format(sheet_index + 1))
                    plt.axvline(x=positions[1], color='red', linestyle='--', label=f'Width: {width:.2f} m (sheet {sheet_index + 1})')
                    plt.axvline(x=positions[2], color='blue', linestyle='--', label=f'Depth: {depth:.2f} m (sheet {sheet_index + 1})')

                    # Draw rectangle
                    plt.fill_betweenx([0, gi_sheet_width], current_position, current_position + gi_sheet_max_length, color='green', alpha=0.3)

            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)  # Close the plot-section div

    st.markdown('</div>', unsafe_allow_html=True)  # Close the background div

# Set background color for right column
with right_column:
    st.markdown('<div style="background-color: #FFCC00; padding: 10px; border-radius: 5px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Result</h2>", unsafe_allow_html=True)
    # Display calculation results in collapsible sections
    with st.expander("Calculated Results", expanded=True):
        st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

        # Calculations    
        st.markdown(f'<div class="result-item"> <strong>Calculated total length required to fold the duct: {main_formula_value:.2f} meters </strong></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-item"> <strong>Sheets needed based on the length of duct: {sheet_value:.2f} sheets</strong></div>', unsafe_allow_html=True)
        if main_formula_value > gi_sheet_max_length:
            st.markdown(f'<div class="result-item"> <strong>Total sheets needed (2): {number_of_sheets} sheets </strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-item"> <strong>Total sheets needed (1): {number_of_sheets} sheets </strong></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the background div
