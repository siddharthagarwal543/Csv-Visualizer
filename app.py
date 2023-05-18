import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page title and layout
st.set_page_config(
    page_title="Data Visualization App",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Set dark mode theme
st.markdown(
    """
    <style>
    body {
        color: #D3D3D3;
        background-color: #2B2B2B;
    }
    .stButton button {
        color: #2B2B2B !important;
        background-color: #D3D3D3 !important;
    }
    .stTextInput>div>div>input {
        color: #D3D3D3 !important;
        background-color: #2B2B2B !important;
    }
    .stSelectbox>div>div>div>div>select {
        color: #D3D3D3 !important;
        background-color: #2B2B2B !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add title and description
st.title("Data Visualization App")
st.write("Upload a CSV file and explore the data visualization.")

# Create a file uploader widget
file = st.file_uploader("Upload CSV file", type=["csv"])

# Check if a file is uploaded
if file is not None:
    # Read the CSV file data
    data = pd.read_csv(file)
    
    # Perform data preprocessing
    data['time'] = pd.to_datetime(data['time'])
    
    # Calculate device-wise efficiency and average RPM
    data['Efficiency'] = data['Total_rotations'] / (data['Total_rotations'] + data['Off_time'])
    avg_rpm = data['RPM'].mean()
    
    # Display the data in a table
    st.subheader("Data Table")
    st.dataframe(data)
    
    # Get the list of column names
    column_names = data.columns.tolist()
    
    # Select the x-axis and y-axis fields
    x_axis = st.selectbox("Select X-axis field", column_names)
    y_axis = st.selectbox("Select Y-axis field", column_names)
    
    # Select the type of graph to plot
    graph_type = st.selectbox("Select Graph Type", ["Line Plot", "Scatter Plot", "Bar Plot", "Area Plot", "Histogram"])
    
    # Perform additional data preprocessing based on the selected graph type
    if graph_type in ["Line Plot", "Scatter Plot", "Bar Plot", "Area Plot"]:
        data = data.dropna(subset=[x_axis, y_axis])
    
    # Visualize the data based on the selected graph type
    st.subheader("Data Visualization")
    st.write(f"Visualizing {y_axis} vs {x_axis}")
    
    with st.spinner("Generating visualization..."):
        if graph_type == "Line Plot":
            fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            fig.update_traces(mode='markers+lines')
            fig.update_layout(showlegend=False)
            fig.frames = [go.Frame(data=[go.Scatter(x=data[x_axis][:i+1], y=data[y_axis][:i+1], mode='markers')]) for i in range(len(data))]

        elif graph_type == "Scatter Plot":
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            fig.update_layout(showlegend=False)

        elif graph_type == "Bar Plot":
            fig = px.bar(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            fig.update_layout(showlegend=False)

        elif graph_type == "Area Plot":
            fig = px.area(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            fig.update_layout(showlegend=False)

        elif graph_type == "Histogram":
            fig = px.histogram(data, x=y_axis, title=f"{y_axis} Histogram")
            fig.update_layout(showlegend=False)
        
    st.plotly_chart(fig)
    
    # Conclusion based on data visualization
    st.subheader("Conclusion")
    
    if graph_type in ["Line Plot", "Scatter Plot"]:
        st.write(f"The {y_axis} tends to vary with {x_axis}.")
    elif graph_type == "Bar Plot":
        st.write(f"The {y_axis} shows different values for different {x_axis}.")
    elif graph_type == "Area Plot":
        st.write(f"The area under the curve represents the cumulative {y_axis} with respect to {x_axis}.")
    elif graph_type == "Histogram":
        st.write(f"The histogram shows the distribution of {y_axis} values.")

    # Display device-wise efficiency and average RPM
    st.subheader("Device-wise Efficiency")
    efficiency_fig = px.bar(data, x="Device_id", y="Efficiency", title="Device-wise Efficiency")
    efficiency_fig.update_layout(showlegend=False)
    st.plotly_chart(efficiency_fig)
    st.write(f"The device-wise efficiency visualization highlights variations in efficiency across devices.")
    
    st.subheader("Average RPM")
    st.write(f"The average RPM is: {avg_rpm}")
    st.write(f"The average RPM gives an idea of the overall rotational speed.")
