import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(page_title="Bhutan Rainfall Explorer", layout="wide")

# Function to encode image as base64
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

# Session state
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

# ---------- FULL SCREEN BHUTAN IMAGE PAGE ----------
if not st.session_state.show_dashboard:
    # Get base64 encoded image
    bhutan_image_b64 = get_base64_image("bhutan_image.jpg")
    
    if bhutan_image_b64:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('data:image/jpeg;base64,{bhutan_image_b64}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}
            .stButton > button {{
                background: rgba(255, 255, 255, 0.2) !important;
                color: white !important;
                border: 2px solid rgba(255, 255, 255, 0.5) !important;
                border-radius: 15px !important;
                padding: 0.75rem 2rem !important;
                font-size: 1.1rem !important;
                font-weight: bold !important;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
                backdrop-filter: blur(10px) !important;
                transition: all 0.3s ease !important;
                margin: 0 auto !important;
                display: block !important;
                position: fixed !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                z-index: 10 !important;
            }}
            .stButton > button:hover {{
                background: rgba(255, 255, 255, 0.4) !important;
                border-color: rgba(255, 255, 255, 0.8) !important;
                transform: translate(-50%, -50%) translateY(-2px) !important;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # Fallback if image is not found
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .center-box {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(255, 255, 255, 0.9);
                padding: 3rem 4rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                z-index: 10;
            }
            .center-box h1 {
                color: #2c3e50;
                margin-bottom: 1rem;
                font-size: 2.5rem;
            }
            .center-box p {
                color: #34495e;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            </style>
            <div class="center-box">
                <h1> Bhutan Rainfall Explorer</h1>
                <p>Explore, analyze, and visualize rainfall trends across Bhutan (2021–2025).</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if st.button(" Enter Dashboard", key="enter_dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()
    
    st.stop()

# ---------- DASHBOARD ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_btn_rainfall.csv", parse_dates=["date"])
    df["month_name"] = df["date"].dt.month_name()
    return df

df = load_data()

# Sidebar
st.sidebar.header(" Filter Options")
st.sidebar.markdown("*Select regions and year range to explore rainfall data*")

regions = st.sidebar.multiselect(
    "Select Regions", 
    df["ADM2_PCODE"].unique(),
    default=[],  # Start with no regions selected
    help="Choose one or more regions to analyze rainfall patterns"
)

year_range = st.sidebar.slider(
    "Year Range", 
    int(df["year"].min()), 
    int(df["year"].max()), 
    (2021, 2025),
    help="Select the time period for analysis"
)

# Add some helpful info in sidebar
if len(regions) == 0:
    st.sidebar.info(" Select regions above to start exploring data")
else:
    st.sidebar.success(f" {len(regions)} region(s) selected")
    
st.sidebar.markdown("---")
st.sidebar.markdown("###  Quick Stats")
st.sidebar.metric("Total Regions Available", len(df["ADM2_PCODE"].unique()))
st.sidebar.metric("Data Time Span", f"{df['year'].min()}-{df['year'].max()}")
st.sidebar.metric("Total Records", f"{len(df):,}")

# Forecast Analysis in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔮 Forecast Analysis")
show_forecast = st.sidebar.button(" View Rainfall Forecast", help="Access detailed rainfall predictions and analysis")

if show_forecast:
    # Store in session state to persist the view
    st.session_state.show_forecast = True

# Reset forecast view option
if st.sidebar.button(" Close Forecast"):
    st.session_state.show_forecast = False

# Forecast section - independent of region selection
if hasattr(st.session_state, 'show_forecast') and st.session_state.show_forecast:
    st.markdown("---")
    st.subheader(" Rainfall Forecast Analysis")
    st.markdown("*Access comprehensive rainfall predictions and analysis from the sidebar*")
    
    try:
        # Try to load forecast data
        forecast_df = pd.read_csv("outputs/forecast.csv", parse_dates=["ds"])
        
        st.markdown("###  Future Rainfall Predictions")
        st.markdown("*This forecast uses Prophet time series modeling to predict future rainfall patterns.*")
        
        # Display forecast metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate forecast period
        forecast_start = forecast_df['ds'].min()
        forecast_end = forecast_df['ds'].max()
        forecast_days = (forecast_end - forecast_start).days
        
        with col1:
            st.metric(" Forecast Period", f"{forecast_days} days")
        with col2:
            avg_forecast = forecast_df['yhat'].mean()
            st.metric(" Avg Predicted Rainfall", f"{avg_forecast:.1f} mm")
        with col3:
            max_forecast = forecast_df['yhat'].max()
            st.metric(" Peak Forecast", f"{max_forecast:.1f} mm")
        with col4:
            min_forecast = forecast_df['yhat'].min()
            st.metric(" Lowest Forecast", f"{min_forecast:.1f} mm")
        
        st.markdown("---")
        
        # Main forecast visualization
        st.markdown("###  Forecast Visualization")
        
        # Create forecast plot with confidence intervals
        fig_forecast = go.Figure()
        
        # Add forecast line
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='#2E86AB', width=3),
            hovertemplate='<b>Date:</b> %{x}<br><b>Forecast:</b> %{y:.1f} mm<extra></extra>'
        ))
        
        # Add confidence intervals if available
        if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
            # Upper bound
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat_upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Lower bound with fill
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat_lower'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(46, 134, 171, 0.2)',
                name='Confidence Interval',
                hovertemplate='<b>Date:</b> %{x}<br><b>Lower:</b> %{y:.1f} mm<extra></extra>'
            ))
        
        # Add actual data if available (historical part)
        if 'y' in forecast_df.columns:
            actual_data = forecast_df[forecast_df['y'].notna()]
            if len(actual_data) > 0:
                fig_forecast.add_trace(go.Scatter(
                    x=actual_data['ds'],
                    y=actual_data['y'],
                    mode='markers+lines',
                    name='Historical Data',
                    line=dict(color='#A23B72', width=2),
                    marker=dict(size=6, color='#A23B72'),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Actual:</b> %{y:.1f} mm<extra></extra>'
                ))
        
        fig_forecast.update_layout(
            title='Rainfall Forecast with Confidence Intervals',
            title_font_size=16,
            title_x=0.5,
            xaxis_title='Date',
            yaxis_title='Rainfall (mm)',
            hovermode='x unified',
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Monthly forecast breakdown
        st.markdown("### 📅 Monthly Forecast Breakdown")
        
        # Create monthly aggregation
        forecast_df['month'] = forecast_df['ds'].dt.month
        forecast_df['month_name'] = forecast_df['ds'].dt.month_name()
        monthly_forecast = forecast_df.groupby(['month', 'month_name'])['yhat'].mean().reset_index()
        
        # Create monthly forecast bar chart
        fig_monthly = px.bar(
            monthly_forecast, 
            x='month_name', 
            y='yhat',
            title='Average Monthly Forecast',
            labels={'yhat': 'Predicted Rainfall (mm)', 'month_name': 'Month'},
            color='yhat',
            color_continuous_scale='Blues',
            template="plotly_white"
        )
        
        fig_monthly.update_traces(
            texttemplate='%{y:.1f}',
            textposition='outside',
            marker_line_color="#2E86AB",
            marker_line_width=1.5
        )
        
        fig_monthly.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Seasonal analysis
        st.markdown("###  Seasonal Forecast Analysis")
        
        # Define seasons
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Autumn'
        
        forecast_df['season'] = forecast_df['month'].apply(get_season)
        seasonal_forecast = forecast_df.groupby('season')['yhat'].agg(['mean', 'std']).reset_index()
        seasonal_forecast.columns = ['Season', 'Average_Rainfall', 'Std_Deviation']
        
        # Create seasonal comparison
        fig_seasonal = px.bar(
            seasonal_forecast, 
            x='Season', 
            y='Average_Rainfall',
            title='Seasonal Rainfall Forecast',
            labels={'Average_Rainfall': 'Average Rainfall (mm)'},
            color='Average_Rainfall',
            color_continuous_scale='Viridis',
            template="plotly_white"
        )
        
        fig_seasonal.update_traces(
            error_y=dict(type='data', array=seasonal_forecast['Std_Deviation'], visible=True),
            texttemplate='%{y:.1f}',
            textposition='outside',
            marker_line_color="#2E86AB",
            marker_line_width=1.5
        )
        
        fig_seasonal.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Data table
        st.markdown("###  Forecast Data Table")
        
        # Show recent forecast data
        display_forecast = forecast_df[['ds', 'yhat']].copy()
        display_forecast.columns = ['Date', 'Predicted_Rainfall_mm']
        display_forecast['Predicted_Rainfall_mm'] = display_forecast['Predicted_Rainfall_mm'].round(2)
        
        # Add confidence intervals if available
        if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
            display_forecast['Lower_Bound'] = forecast_df['yhat_lower'].round(2)
            display_forecast['Upper_Bound'] = forecast_df['yhat_upper'].round(2)
        
        st.dataframe(display_forecast.tail(30), use_container_width=True, height=300)
        
        # Download option
        csv = display_forecast.to_csv(index=False)
        st.download_button(
            label=" Download Forecast Data",
            data=csv,
            file_name="bhutan_rainfall_forecast.csv",
            mime="text/csv"
        )
        
    except FileNotFoundError:
        st.info("🔮 **Forecast data not available yet**")
        st.markdown("""
        **To generate forecast data:**
        1.  Open the forecast notebook (`notebooks/forecast.ipynb`)
        2.  Run the Prophet forecasting model
        3.  This will generate `outputs/forecast.csv`
        4.  Refresh this dashboard to see the forecast
        """)
        
        # Show preview of what forecast would look like
        st.markdown("**Preview of forecast features:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ** Visualizations:**
            - Time series forecast with confidence intervals
            - Monthly breakdown predictions
            - Seasonal analysis
            - Interactive Plotly charts
            """)
        
        with col2:
            st.markdown("""
            ** Metrics:**
            - Forecast period duration
            - Average predicted rainfall
            - Peak and minimum forecasts
            - Seasonal comparisons
            """)
    
    except Exception as e:
        st.error(f" **Error loading forecast data:** {str(e)}")
        st.markdown("Please check if the forecast analysis has been run successfully.")
        st.markdown("**Debug info:**")
        st.code(f"Error details: {type(e).__name__}: {str(e)}")
    
    # Stop here if forecast is shown - don't show the main dashboard
    st.stop()

filtered_df = df[
    df["ADM2_PCODE"].isin(regions) &
    df["year"].between(year_range[0], year_range[1])
]

# Dashboard content
# Check if regions are selected
if len(regions) == 0:
    # Show full-screen Bhutan image when no regions are selected
    bhutan_image_b64 = get_base64_image("bhutan_image.jpg")
    
    if bhutan_image_b64:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url('data:image/jpeg;base64,{bhutan_image_b64}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
                min-height: 100vh;
            }}
            .main-content {{
                background: transparent !important;
            }}
            
            /* Animated title styles */
            .animated-title {{
                position: fixed;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                z-index: 10;
            }}
            
            .animated-title h1 {{
                color: #ffffff;
                font-size: 4rem;
                font-weight: bold;
                text-shadow: 3px 3px 8px rgba(0,0,0,0.9);
                letter-spacing: 2px;
                margin: 0;
                animation: fadeInScale 2s ease-in-out, glow 3s ease-in-out infinite alternate;
            }}
            
            .animated-title .subtitle {{
                color: #FFD700;
                font-size: 1.8rem;
                font-style: italic;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
                margin-top: 1rem;
                animation: fadeInUp 2s ease-in-out 0.5s both;
            }}
            
            /* Animations */
            @keyframes fadeInScale {{
                0% {{
                    opacity: 0;
                    transform: scale(0.8);
                }}
                100% {{
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
            
            @keyframes fadeInUp {{
                0% {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                100% {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes glow {{
                0% {{
                    text-shadow: 3px 3px 8px rgba(0,0,0,0.9), 0 0 10px rgba(255,255,255,0.3);
                }}
                100% {{
                    text-shadow: 3px 3px 8px rgba(0,0,0,0.9), 0 0 20px rgba(255,255,255,0.6), 0 0 30px rgba(255,215,0,0.4);
                }}
            }}
            
            /* Floating animation for dragon emoji */
            .dragon-float {{
                animation: float 4s ease-in-out infinite;
                display: inline-block;
            }}
            
            @keyframes float {{
                0%, 100% {{
                    transform: translateY(0px);
                }}
                50% {{
                    transform: translateY(-10px);
                }}
            }}
            </style>
            <div class="animated-title">
                <h1> Bhutan Rainfall Explorer</h1>
                <div class="subtitle">
                    <span class="dragon-float">🐉</span> The Land of the Thunder Dragon <span class="dragon-float">🐉</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.info(" **Please select regions from the sidebar to start exploring rainfall data**")
        st.markdown("""
        ###  Features Available:
        -  **Monthly rainfall trends** over time
        -  **Rainfall distribution** analysis  
        -  **Seasonal patterns** by month
        -  **Regional comparisons** across selected areas
        -  **Machine learning clusters** (when available)
        """)
    
    st.stop()

# Show dashboard title only when regions are selected
st.title(" Bhutan Rainfall Dashboard")

# Show selected regions info
st.markdown(f"Showing **{len(regions)}** regions from **{year_range[0]}–{year_range[1]}**")

# Filter data
filtered_df = df[
    df["ADM2_PCODE"].isin(regions) &
    df["year"].between(year_range[0], year_range[1])
]

# Check if filtered data is empty
if len(filtered_df) == 0:
    st.warning(" No data available for the selected regions and year range. Please adjust your selections.")
    st.stop()

# Monthly trend
st.subheader(" Monthly Average Rainfall")
monthly_avg = filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["rfh"].mean().reset_index()
monthly_avg["date"] = monthly_avg["date"].dt.to_timestamp()

# Create interactive Plotly line chart
fig1 = px.line(monthly_avg, x="date", y="rfh", 
               title="Monthly Average Rainfall Trends",
               labels={"rfh": "Rainfall (mm)", "date": "Date"},
               template="plotly_white")

fig1.update_traces(
    line=dict(color="#2E86AB", width=3),
    mode="lines+markers",
    marker=dict(size=8, color="#A23B72", line=dict(width=2, color="white"))
)

fig1.update_layout(
    title_font_size=16,
    title_x=0.5,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    hovermode='x unified',
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig1, use_container_width=True)

# Histogram
st.subheader(" Rainfall Distribution")

# Create interactive Plotly histogram
fig2 = px.histogram(filtered_df, x="rfh", nbins=30,
                    title="Rainfall Distribution Across Selected Regions",
                    labels={"rfh": "Rainfall (mm)", "count": "Frequency"},
                    template="plotly_white",
                    marginal="box")  # Add box plot on top

fig2.update_traces(
    marker_color="#4ECDC4",
    marker_line_color="#2E86AB",
    marker_line_width=1.5,
    opacity=0.7
)

fig2.update_layout(
    title_font_size=16,
    title_x=0.5,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True)

# Boxplot
st.subheader(" Rainfall by Month")

# Create interactive Plotly box plot
fig3 = px.box(filtered_df, x="month_name", y="rfh",
              title="Monthly Rainfall Distribution Patterns",
              labels={"rfh": "Rainfall (mm)", "month_name": "Month"},
              template="plotly_white",
              category_orders={"month_name": list(calendar.month_name)[1:]})

fig3.update_traces(
    marker_color="#FF6B6B",
    line_color="#2E86AB",
    fillcolor="rgba(255, 107, 107, 0.3)",
    marker_size=4
)

fig3.update_layout(
    title_font_size=16,
    title_x=0.5,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    xaxis_tickangle=45,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig3, use_container_width=True)

# Regional Comparison
st.subheader(" Regional Rainfall Comparison")
if len(regions) > 1:
    # Create regional comparison chart
    regional_avg = filtered_df.groupby('ADM2_PCODE')['rfh'].agg(['mean', 'std']).reset_index()
    regional_avg.columns = ['Region', 'Average_Rainfall', 'Std_Deviation']
    
    # Create interactive bar chart with error bars
    fig4 = px.bar(regional_avg, x='Region', y='Average_Rainfall',
                  title="Average Rainfall by Region (with Standard Deviation)",
                  labels={"Average_Rainfall": "Average Rainfall (mm)", "Region": "Region Code"},
                  template="plotly_white",
                  color='Average_Rainfall',
                  color_continuous_scale="Blues")
    
    # Add error bars
    fig4.update_traces(
        error_y=dict(type='data', array=regional_avg['Std_Deviation'], visible=True),
        marker_line_color="#2E86AB",
        marker_line_width=1.5,
        texttemplate='%{y:.1f}',
        textposition='outside'
    )
    
    fig4.update_layout(
        title_font_size=16,
        title_x=0.5,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        xaxis_tickangle=45,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Select multiple regions to see regional comparison")

# Forecast section - independent of region selection
if hasattr(st.session_state, 'show_forecast') and st.session_state.show_forecast:
    st.markdown("---")
    st.subheader("🔮 Rainfall Forecast Analysis")
    st.markdown("*Access comprehensive rainfall predictions and analysis from the sidebar*")
    
    try:
        # Try to load forecast data
        forecast_df = pd.read_csv("outputs/forecast.csv", parse_dates=["ds"])
        
        st.markdown("###  Future Rainfall Predictions")
        st.markdown("*This forecast uses Prophet time series modeling to predict future rainfall patterns.*")
        
        # Display forecast metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate forecast period
        forecast_start = forecast_df['ds'].min()
        forecast_end = forecast_df['ds'].max()
        forecast_days = (forecast_end - forecast_start).days
        
        with col1:
            st.metric(" Forecast Period", f"{forecast_days} days")
        with col2:
            avg_forecast = forecast_df['yhat'].mean()
            st.metric(" Avg Predicted Rainfall", f"{avg_forecast:.1f} mm")
        with col3:
            max_forecast = forecast_df['yhat'].max()
            st.metric(" Peak Forecast", f"{max_forecast:.1f} mm")
        with col4:
            min_forecast = forecast_df['yhat'].min()
            st.metric(" Lowest Forecast", f"{min_forecast:.1f} mm")
        
        st.markdown("---")
        
        # Main forecast visualization
        st.markdown("###  Forecast Visualization")
        
        # Create forecast plot with confidence intervals
        fig_forecast = go.Figure()
        
        # Add forecast line
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='#2E86AB', width=3),
            hovertemplate='<b>Date:</b> %{x}<br><b>Forecast:</b> %{y:.1f} mm<extra></extra>'
        ))
        
        # Add confidence intervals if available
        if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
            # Upper bound
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat_upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Lower bound with fill
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat_lower'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(46, 134, 171, 0.2)',
                name='Confidence Interval',
                hovertemplate='<b>Date:</b> %{x}<br><b>Lower:</b> %{y:.1f} mm<extra></extra>'
            ))
        
        # Add actual data if available (historical part)
        if 'y' in forecast_df.columns:
            actual_data = forecast_df[forecast_df['y'].notna()]
            if len(actual_data) > 0:
                fig_forecast.add_trace(go.Scatter(
                    x=actual_data['ds'],
                    y=actual_data['y'],
                    mode='markers+lines',
                    name='Historical Data',
                    line=dict(color='#A23B72', width=2),
                    marker=dict(size=6, color='#A23B72'),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Actual:</b> %{y:.1f} mm<extra></extra>'
                ))
        
        fig_forecast.update_layout(
            title='Rainfall Forecast with Confidence Intervals',
            title_font_size=16,
            title_x=0.5,
            xaxis_title='Date',
            yaxis_title='Rainfall (mm)',
            hovermode='x unified',
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Monthly forecast breakdown
        st.markdown("### 📅 Monthly Forecast Breakdown")
        
        # Create monthly aggregation
        forecast_df['month'] = forecast_df['ds'].dt.month
        forecast_df['month_name'] = forecast_df['ds'].dt.month_name()
        monthly_forecast = forecast_df.groupby(['month', 'month_name'])['yhat'].mean().reset_index()
        
        # Create monthly forecast bar chart
        fig_monthly = px.bar(
            monthly_forecast, 
            x='month_name', 
            y='yhat',
            title='Average Monthly Forecast',
            labels={'yhat': 'Predicted Rainfall (mm)', 'month_name': 'Month'},
            color='yhat',
            color_continuous_scale='Blues',
            template="plotly_white"
        )
        
        fig_monthly.update_traces(
            texttemplate='%{y:.1f}',
            textposition='outside',
            marker_line_color="#2E86AB",
            marker_line_width=1.5
        )
        
        fig_monthly.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Seasonal analysis
        st.markdown("### 🌤️ Seasonal Forecast Analysis")
        
        # Define seasons
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Autumn'
        
        forecast_df['season'] = forecast_df['month'].apply(get_season)
        seasonal_forecast = forecast_df.groupby('season')['yhat'].agg(['mean', 'std']).reset_index()
        seasonal_forecast.columns = ['Season', 'Average_Rainfall', 'Std_Deviation']
        
        # Create seasonal comparison
        fig_seasonal = px.bar(
            seasonal_forecast, 
            x='Season', 
            y='Average_Rainfall',
            title='Seasonal Rainfall Forecast',
            labels={'Average_Rainfall': 'Average Rainfall (mm)'},
            color='Average_Rainfall',
            color_continuous_scale='Viridis',
            template="plotly_white"
        )
        
        fig_seasonal.update_traces(
            error_y=dict(type='data', array=seasonal_forecast['Std_Deviation'], visible=True),
            texttemplate='%{y:.1f}',
            textposition='outside',
            marker_line_color="#2E86AB",
            marker_line_width=1.5
        )
        
        fig_seasonal.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Data table
        st.markdown("### 📋 Forecast Data Table")
        
        # Show recent forecast data
        display_forecast = forecast_df[['ds', 'yhat']].copy()
        display_forecast.columns = ['Date', 'Predicted_Rainfall_mm']
        display_forecast['Predicted_Rainfall_mm'] = display_forecast['Predicted_Rainfall_mm'].round(2)
        
        # Add confidence intervals if available
        if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
            display_forecast['Lower_Bound'] = forecast_df['yhat_lower'].round(2)
            display_forecast['Upper_Bound'] = forecast_df['yhat_upper'].round(2)
        
        st.dataframe(display_forecast.tail(30), use_container_width=True, height=300)
        
        # Download option
        csv = display_forecast.to_csv(index=False)
        st.download_button(
            label="📥 Download Forecast Data",
            data=csv,
            file_name="bhutan_rainfall_forecast.csv",
            mime="text/csv"
        )
        
    except FileNotFoundError:
        st.info("🔮 **Forecast data not available yet**")
        st.markdown("""
        **To generate forecast data:**
        1. 📔 Open the forecast notebook (`notebooks/forecast.ipynb`)
        2. ▶️ Run the Prophet forecasting model
        3. 💾 This will generate `outputs/forecast.csv`
        4. 🔄 Refresh this dashboard to see the forecast
        """)
        
        # Show preview of what forecast would look like
        st.markdown("**Preview of forecast features:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📊 Visualizations:**
            - Time series forecast with confidence intervals
            - Monthly breakdown predictions
            - Seasonal analysis
            - Interactive Plotly charts
            """)
        
        with col2:
            st.markdown("""
            **📈 Metrics:**
            - Forecast period duration
            - Average predicted rainfall
            - Peak and minimum forecasts
            - Seasonal comparisons
            """)
    
    except Exception as e:
        st.error(f"❌ **Error loading forecast data:** {str(e)}")
        st.markdown("Please check if the forecast analysis has been run successfully.")
        st.markdown("**Debug info:**")
        st.code(f"Error details: {type(e).__name__}: {str(e)}")

# Cluster summary
st.subheader(" Cluster Analysis")
with st.expander(" View Cluster Summary", expanded=False):
    try:
        cluster_df = pd.read_csv("outputs/cluster_summary.csv", index_col=0)
        
        # Add some styling and information
        st.markdown("###  Rainfall Pattern Clusters")
        st.markdown("*This analysis groups regions with similar rainfall patterns using machine learning clustering.*")
        
        # Check what columns are available
        st.write("**Available columns:**", list(cluster_df.columns))
        
        # Display metrics in columns - make it flexible based on available columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(" Total Clusters", len(cluster_df))
        
        with col2:
            # Try different possible column names for average rainfall
            avg_rainfall_col = None
            for col in ['avg_rainfall', 'mean_rainfall', 'average_rainfall', 'rfh_mean', 'mean']:
                if col in cluster_df.columns:
                    avg_rainfall_col = col
                    break
            
            if avg_rainfall_col:
                st.metric(" Avg Rainfall (mm)", f"{cluster_df[avg_rainfall_col].mean():.1f}")
            else:
                st.metric(" Avg Rainfall", "N/A")
        
        with col3:
            # Try different possible column names for count
            count_col = None
            for col in ['count', 'size', 'n_regions', 'regions']:
                if col in cluster_df.columns:
                    count_col = col
                    break
            
            if count_col:
                st.metric("Regions Analyzed", int(cluster_df[count_col].sum()))
            else:
                st.metric(" Total Rows", len(cluster_df))
        
        st.markdown("---")
        
        # Style the dataframe
        st.markdown("###  Detailed Cluster Information")
        
        # Format the dataframe for better display
        display_df = cluster_df.copy()
        
        # Round numeric columns
        for col in display_df.columns:
            if display_df[col].dtype in ['float64', 'float32']:
                display_df[col] = display_df[col].round(2)
        
        # Display with basic styling (remove column_config that might cause issues)
        st.dataframe(display_df, use_container_width=True)
        
        # Add visualization if possible
        if len(cluster_df) > 1:
            st.markdown("###  Cluster Visualization")
              # Find a suitable column for plotting
            plot_col = None
            numeric_cols = cluster_df.select_dtypes(include=['float64', 'int64', 'float32', 'int32']).columns
            
            # First try specific rainfall column names
            for col in ['avg_rainfall', 'mean_rainfall', 'average_rainfall', 'rfh_mean', 'mean']:
                if col in cluster_df.columns:
                    plot_col = col
                    break
            
            # If no specific column found, use the first numeric column
            if plot_col is None and len(numeric_cols) > 0:
                plot_col = numeric_cols[0]
            
            if plot_col:
                # Create interactive Plotly bar chart
                fig_cluster = px.bar(
                    x=cluster_df.index,
                    y=cluster_df[plot_col],
                    title=f'{plot_col.replace("_", " ").title()} by Cluster',
                    labels={"x": "Cluster", "y": f'{plot_col.replace("_", " ").title()}'},
                    template="plotly_white",
                    color=cluster_df[plot_col],
                    color_continuous_scale="viridis"
                )
                
                fig_cluster.update_traces(
                    marker_line_color="#2E86AB",
                    marker_line_width=2,
                    texttemplate='%{y:.1f}',
                    textposition='outside'
                )
                
                fig_cluster.update_layout(
                    title_font_size=16,
                    title_x=0.5,
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    showlegend=False
                )
                
                st.plotly_chart(fig_cluster, use_container_width=True)
            else:
                st.info(" No numeric columns available for visualization. The cluster data appears to contain only categorical information.")
        
    except FileNotFoundError:
        st.info("🔬 **Cluster analysis not available yet**")
        st.markdown("""
        **To generate cluster analysis:**
        1.  Open the EDA notebook (`notebooks/Bhutan_Rainfall_EDA.ipynb`)
        2.  Run the clustering analysis section
        3.  This will generate `outputs/cluster_summary.csv`
        4.  Refresh this dashboard to see the results
        """)
        
        # Show a sample of what it would look like
        st.markdown("**Preview of cluster analysis format:**")
        sample_data = {
            'Cluster': ['High Rainfall', 'Moderate Rainfall', 'Low Rainfall'],
            'Avg Rainfall (mm)': [150.5, 89.2, 45.8],
            'Regions Count': [12, 18, 8],
            'Pattern': ['Monsoon-heavy', 'Seasonal', 'Arid']
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
    
    except Exception as e:
        st.error(f" **Error loading cluster data:** {str(e)}")
        st.markdown("Please check if the cluster analysis has been run successfully.")
        st.markdown("**Debug info:**")
        st.code(f"Error details: {type(e).__name__}: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built by **Sangam Paudel** · Project: Bhutan Rainfall Explorer")
