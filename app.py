import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(page_title="Mira - GHG Calculator", layout="wide")

# Emission factors for different categories
EMISSION_FACTORS = {
    'livestock': {
        'Beef Cow': 99.0, 'Dairy Cow': 102.0, 'Buffalo': 107.0, 'Chicken': 6.0, 'Pigs': 21.0, 'Sheep': 15.0, 'Goats': 15.0, 'Camels': 84.0, 'Horses': 56.0
    },
    'crops': {
        'Wheat': 0.69, 'Barley': 0.54, 'Maize': 0.77, 'Oats': 0.64, 'Rye': 0.68, 'Rice': 1.50, 'Millet': 0.67, 'Sorghum': 0.61, 'Pasture': 0.15, 'Peas': 0.45,
        'Beans': 0.62, 'Soybeans': 0.62, 'Potatoes': 0.43, 'Feedbeet': 0.47, 'Sugarcane': 0.73, 'Peanuts': 0.80
    },
    'fertilizer': {
        'Urea': 1.87, 'Lime': 0.61, 'Gypsum': 0.10, 'Animal Manure': 0.20, 'Organic Compost': 0.20, 'Filter Cake': 0.25, 'Vinasse': 0.10
    },
    'fuel': {
        'Diesel Oil': 2.68, 'Gasoline': 2.31, 'Biodiesel': 1.83, 'Anhydrous Ethanol': 1.50, 'Hydrated Ethanol': 1.44, 'Natural Gas': 2.75
    },
    'electricity': {
        'Solar': 0.05, 'Wind': 0.03, 'Hydropower': 0.02
    }
}

def get_emission_factors():
    """Retrieve emission factors for all categories."""
    return EMISSION_FACTORS

def calculate_emissions(quantity, factor):
    """Calculate emissions based on quantity and emission factor."""
    return quantity * factor

def calculate_total_emissions(data):
    """Calculate total emissions for different categories."""
    factors = get_emission_factors()
    emissions = {
        category: sum(calculate_emissions(quantity, factors[category].get(item, 0))
                      for item, quantity in items.items())
        for category, items in data.items()
    }
    return emissions

def plot_comparison_chart(data):
    """Generate a comparison chart for traditional vs reduced emissions."""
    labels, traditional_values, reduced_values = [], [], []

    def add_emissions(type_dict, factor_dict):
        for item, quantity in type_dict.items():
            annual_emissions = calculate_emissions(quantity, factor_dict[item])
            reduced_emissions = annual_emissions * 0.8
            labels.append(item)
            traditional_values.append(annual_emissions)
            reduced_values.append(reduced_emissions)

    factors = get_emission_factors()
    for category in factors:
        add_emissions(data[category], factors[category])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=traditional_values, name='Traditional Farming', marker_color='pink'))
    fig.add_trace(go.Bar(x=labels, y=reduced_values, name='Reduced GHG', marker_color='purple'))

    fig.update_layout(
        xaxis_title='Farming',
        yaxis_title='Annual Emissions (kg CO2e)',
        barmode='group',
        legend=dict(
            orientation="h",
            entrywidth=100,
            yanchor="bottom",
            y=1.09,
            xanchor="right",
            x=1,
            tracegroupgap=10
        )
    )
    return fig

def plot_time_series_chart(predicted_emissions):
    """Generate a time series chart for predicted emissions over a decade."""
    years = list(range(2024, 2034))
    traditional_emissions = predicted_emissions['traditional']
    reduced_emissions = predicted_emissions['reduced']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=traditional_emissions, mode='lines+markers', name='Traditional Farming', marker_color='pink'))
    fig.add_trace(go.Scatter(x=years, y=reduced_emissions, mode='lines+markers', name='Reduced GHG', marker_color='purple'))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Emissions (kg CO2e)',
        legend=dict(
            orientation="h",
            entrywidth=100,
            yanchor="bottom",
            y=1.09,
            xanchor="right",
            x=1,
            tracegroupgap=10
        )
    )
    return fig

def plot_total_emissions_chart(total_emissions):
    """Generate a bar chart for total emissions by category."""
    fig = go.Figure(data=[go.Bar(x=list(total_emissions.keys()), y=list(total_emissions.values()))])
    fig.update_layout(
        title_text='Total Emissions by Category',
        xaxis_title='Category',
        yaxis_title='Total Emissions (kg CO2e)',
    )
    return fig

def predict_future_emissions(data):
    """Predict future emissions over a decade."""
    factors = get_emission_factors()
    base_emissions = calculate_total_emissions(data)

    years = list(range(2024, 2034))
    traditional_emissions = [base_emissions['livestock'] + base_emissions['crops'] + base_emissions['fertilizer'] +
                             base_emissions['fuel'] + base_emissions['electricity']]
    reduced_emissions = [e * 0.8 for e in traditional_emissions]
    
    for _ in range(1, len(years)):
        traditional_emissions.append(traditional_emissions[-1] * 1.05)
        reduced_emissions.append(reduced_emissions[-1] * 1.05)

    return {
        'traditional': traditional_emissions,
        'reduced': reduced_emissions
    }

def generate_recommendations(data):
    recommendations = []
    
    if 'livestock' in data and data['livestock']:
        recommendations.append("### Recommendations for Livestock")
        for animal, quantity in data['livestock'].items():
            if quantity > 0:
                recommendations.append(f"- Consider improving feed efficiency and manure management for {animal}. This can help reduce methane emissions.")
                
    if 'crops' in data and data['crops']:
        recommendations.append("### Recommendations for Crops")
        for crop, quantity in data['crops'].items():
            if quantity > 0:
                recommendations.append(f"- Optimize fertilizer use and adopt precision agriculture techniques for {crop} to minimize emissions.")
                
    if 'fertilizer' in data and data['fertilizer']:
        recommendations.append("### Recommendations for Fertilizers")
        for fertilizer, quantity in data['fertilizer'].items():
            if quantity > 0:
                recommendations.append(f"- Use fertilizers like Organic Compost or Filter Cake to reduce emissions compared to conventional options.")
                
    if 'fuel' in data and data['fuel']:
        recommendations.append("### Recommendations for Fuel")
        for fuel, quantity in data['fuel'].items():
            if quantity > 0:
                recommendations.append(f"- Switch to cleaner fuels like Biodiesel or reduce reliance on Diesel Oil to lower emissions.")
                
    if 'electricity' in data and data['electricity']:
        recommendations.append("### Recommendations for Electricity")
        for source, quantity in data['electricity'].items():
            if quantity > 0:
                recommendations.append(f"- Increase the use of renewable energy sources such as Solar or Wind to reduce emissions from electricity consumption.")
    
    return recommendations

def show_introduction():
    st.title("Food security & Sustainable Agriculture")
    st.image("assets/mira.png", use_column_width=True)
    st.write("""
    ### Climate Change and Emission Reduction

    Climate change is one of the most pressing issues of our time, driven largely by the increase in greenhouse gases (GHGs) in our atmosphere. These gases trap heat and contribute to global warming, which leads to a range of environmental impacts including more frequent extreme weather events, rising sea levels, and disruptions to ecosystems.

    Agriculture is a significant contributor to GHG emissions, particularly through activities such as livestock farming, crop production, fertilizer use, fuel consumption, and electricity generation. Reducing emissions in these areas is crucial for mitigating climate change and promoting sustainable practices.

    The Mira GHG Calculator helps you estimate your emissions from various agricultural activities and provides insights into how you can reduce your carbon footprint. By inputting your data, you can visualize your emissions, compare traditional and reduced emission scenarios, and receive actionable recommendations for minimizing your impact.

    Let's work together to make a positive difference for our planet.
    """)
    
    if st.button("Enter your Data"):
        st.session_state.page = "Enter your Data"
        st.rerun()

def show_input():
    st.title("Enter your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Livestock")
        livestock_quantities = {animal: st.number_input(f"{animal} Quantity (heads)", min_value=0, value=0, key=f"livestock_{animal}")
                                for animal in st.multiselect("Select Livestock Types", options=list(EMISSION_FACTORS['livestock'].keys()))}

        st.subheader("Crops")
        crop_quantities = {crop: st.number_input(f"{crop} Quantity (ha)", min_value=0, value=0, key=f"crops_{crop}")
                           for crop in st.multiselect("Select Crop Types", options=list(EMISSION_FACTORS['crops'].keys()))}

    with col2:
        st.subheader("Fertilizer")
        fertilizer_quantities = {fertilizer: st.number_input(f"{fertilizer} Quantity (kg)", min_value=0, value=0, key=f"fertilizer_{fertilizer}")
                                 for fertilizer in st.multiselect("Select Fertilizer Types", options=list(EMISSION_FACTORS['fertilizer'].keys()))}

        st.subheader("Fuel")
        fuel_quantities = {fuel: st.number_input(f"{fuel} Quantity (liters/m³)", min_value=0, value=0, key=f"fuel_{fuel}")
                           for fuel in st.multiselect("Select Fuel Types", options=list(EMISSION_FACTORS['fuel'].keys()))}

        st.subheader("Electricity")
        electricity_quantities = {source: st.number_input(f"{source} Quantity (kWh)", min_value=0, value=0, key=f"electricity_{source}")
                                  for source in st.multiselect("Select Electricity Sources", options=list(EMISSION_FACTORS['electricity'].keys()))}
    
    if st.button("Calculate Emissions"):
        data = {
            'livestock': livestock_quantities,
            'crops': crop_quantities,
            'fertilizer': fertilizer_quantities,
            'fuel': fuel_quantities,
            'electricity': electricity_quantities
        }
        
        st.session_state.data = data
        st.session_state.page = "Result"
        st.rerun()

def show_results():
    """Display the results of the emissions calculations and provide recommendations."""
    st.title("Results")
    
    if 'data' in st.session_state:
        data = st.session_state.data
        total_emissions = calculate_total_emissions(data)
        predicted_emissions = predict_future_emissions(data)
        recommendations = generate_recommendations(data)
        
        # Create a grid layout for the charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Total Emissions (kg CO2e):")
            st.plotly_chart(plot_total_emissions_chart(total_emissions), use_container_width=True)
        
        with col2:
            st.write("### Emissions Comparison:")
            st.plotly_chart(plot_comparison_chart(data), use_container_width=True)
        
        st.write("### Predicted Emissions Over the Next Decade:")
        st.plotly_chart(plot_time_series_chart(predicted_emissions), use_container_width=True)
        
        st.write("### Recommendations")
        for rec in recommendations:
            st.write(rec)
       
    else:
        st.error("No data available. Please enter your data first.")

def show_navigation_bar():
    """Display a navigation bar at the top of the app."""
    # Display logo at the top of the sidebar
    st.sidebar.image("assets/logo.png", use_column_width=True)
    
    # Title and page selection
    st.sidebar.title("GHG Calculator")
    pages = ["Home", "Enter your Data", "Result"]
    page = st.sidebar.radio("", pages, index=pages.index(st.session_state.page) if 'page' in st.session_state else 0)
    st.session_state.page = page

    # Instructions and Disclaimer
    st.sidebar.write("### Instructions")
    st.sidebar.write("""
    - Navigate between the pages using the sidebar.
    - On the "Enter your Data" page, input the relevant information.
    - On the "Result" page, view the emissions comparison and recommendations.
    """)
    
    st.sidebar.write("### Disclaimer")
    st.sidebar.write("""
    - The emission factors used are based on general data and may not reflect the exact conditions in your area.
    - This calculator provides estimates and should be used as a guide only.
    - For precise calculations and recommendations, please contact Mira consultants.
    """)

# Main logic
if 'page' not in st.session_state:
    st.session_state.page = "Home"

show_navigation_bar()

if st.session_state.page == "Home":
    show_introduction()
elif st.session_state.page == "Enter your Data":
    show_input()
elif st.session_state.page == "Result":
    show_results()
else:
    st.error("Unknown page.")
