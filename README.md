#  Bhutan Rainfall Explorer

<div align="center">

![Bhutan Rainfall Explorer](https://img.shields.io/badge/Bhutan-Rainfall%20Explorer-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-brightgreen?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**Explore, analyze, and visualize rainfall trends across the Land of the Thunder Dragon 🐉**

*An interactive data science dashboard for exploring rainfall patterns in Bhutan (2021–2025)*

[ Live Demo](#-quick-start) • [ Features](#-features) • [ Installation](#️-installation) • [ Documentation](#-documentation)

</div>

---

##  Overview

The **Bhutan Rainfall Explorer** is a comprehensive data visualization and analysis platform that provides insights into rainfall patterns across Bhutan's diverse geographical regions. Built with Python and Streamlit, this interactive dashboard combines historical data analysis with machine learning-powered forecasting to help researchers, meteorologists, and policymakers understand precipitation trends in the Himalayan kingdom.

###  Key Highlights

- **Interactive Data Exploration** - Dynamic filtering by regions and time periods
- **Advanced Visualizations** - Plotly-powered charts with hover interactions
- **Machine Learning Insights** - Clustering analysis of rainfall patterns
- **Predictive Forecasting** - Prophet-based time series forecasting
- **Beautiful UI/UX** - Animated welcome screen with Bhutan landscape background
- **Export Capabilities** - Download data and forecasts as CSV files

---

##  Features

###  **Welcome Experience**
- **Cinematic Introduction** - Full-screen Bhutan landscape with animated title
- **Floating Animations** - Thunder dragon emojis with smooth floating effects
- **Professional Glassmorphism** - Modern UI design with backdrop blur effects

###  **Historical Data Analysis**
- ** Monthly Trends** - Interactive time series visualization of rainfall patterns
- ** Distribution Analysis** - Histogram with marginal box plots for statistical insights
- ** Seasonal Patterns** - Monthly boxplots revealing seasonal variations
- ** Regional Comparisons** - Comparative analysis across multiple regions with error bars

###  **Forecasting & Predictions**
- **Time Series Forecasting** - Prophet-based predictions with confidence intervals
- **Monthly Breakdown** - Future rainfall predictions by month
- **Seasonal Analysis** - Forecast comparisons across seasons (Winter, Spring, Summer, Autumn)
- **Interactive Charts** - Plotly visualizations with hover details and zoom capabilities

###  **Machine Learning Insights**
- **Clustering Analysis** - Automated grouping of regions with similar rainfall patterns
- **Pattern Recognition** - Identification of high, moderate, and low rainfall zones
- **Statistical Summaries** - Comprehensive metrics and data tables
- **Adaptive Visualization** - Flexible charts that adapt to available data

###  **Interactive Controls**
- **Smart Filtering** - Multi-select regions with real-time data updates
- **Time Range Selection** - Slider-based year filtering (2021-2025)
- **Collapsible Sections** - Organized layout with expandable analysis sections
- **Responsive Design** - Mobile-friendly interface that works on all devices

---

##  Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Quick Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/bhutan-rainfall-explorer.git
   cd bhutan-rainfall-explorer
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in your terminal

### Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
seaborn>=0.12.0
matplotlib>=3.7.0
scikit-learn>=1.3.0
prophet>=1.1.4
base64
calendar
```

---

##  Project Structure

```
bhutan-rainfall-explorer/
├──  app.py                        
├──  bhutan_image.jpg               
├──  data/
│   ├── btn-rainfall-adm2-5ytd.csv    
│   └── cleaned_btn_rainfall.csv       
├──  notebooks/
│   ├── Bhutan_Rainfall_EDA.ipynb    
├──  outputs/
│   └── forecast.ipynb                 
│   ├── cluster_summary.csv            
│   ├── forecast.csv                   
│   └── monthly_region_clusters.csv 
├──  visuals/
│   ├── avg_rainfall_region_year_heatmap.png
│   ├── forecast_components_prophet.png
│   ├── monthly_avg_rainfall.png
│   ├── national_rainfall_decomposition.png
│   ├── rainfall_distribution_by_month.png
│   ├── rainfall_distribution_histogram.png
│   ├── rainfall_forecast_prophet.png
│   └── top10_rainiest_regions_yearly.png
├──  requirements.txt             
└──  README.md                       

---

##  Quick Start

### Option 1: Explore with Sample Data
1. Launch the application using the installation steps above
2. The welcome screen will display the beautiful Bhutan landscape
3. Click " Enter Dashboard" to access the main interface
4. Select regions from the sidebar to start exploring data
5. Use the " View Forecast" button for predictive analysis

### Option 2: Generate Your Own Analysis
1. **Run EDA Notebook:**
   ```bash
   jupyter notebook notebooks/Bhutan_Rainfall_EDA.ipynb
   ```
   - Execute all cells to generate clustering analysis
   - This creates `outputs/cluster_summary.csv`

2. **Generate Forecasts:**
   ```bash
   jupyter notebook notebooks/forecast.ipynb
   ```
   - Run the Prophet forecasting model
   - This creates `outputs/forecast.csv`

3. **Refresh Dashboard:**
   - Restart the Streamlit app to see new analysis results

---

##  Data Sources

### Dataset Information
- **Coverage**: Administrative Level 2 regions of Bhutan
- **Time Period**: 2021-2025 (5 years)
- **Granularity**: Daily rainfall measurements
- **Units**: Millimeters (mm)
- **Regions**: 20 administrative districts (dzongkhags)

### Data Processing
- **Cleaning**: Handled missing values and outliers
- **Feature Engineering**: Added month names, seasonal classifications
- **Aggregation**: Created monthly and seasonal summaries
- **Validation**: Statistical quality checks and consistency verification

---

##  Visualizations Gallery

###  Interactive Time Series
- **Monthly Trends**: Line charts with markers showing temporal patterns
- **Confidence Intervals**: Forecast predictions with uncertainty bands
- **Hover Details**: Interactive tooltips with precise values

###  Distribution Analysis
- **Histograms**: Frequency distributions with kernel density estimation
- **Box Plots**: Statistical summaries showing quartiles and outliers
- **Marginal Plots**: Combined histogram and box plot visualizations

###  Regional Comparisons
- **Bar Charts**: Comparative analysis with error bars
- **Color Coding**: Visual distinction between different rainfall levels
- **Interactive Legends**: Clickable legend items for data filtering

###  Forecasting Visuals
- **Prophet Decomposition**: Trend, seasonal, and residual components
- **Seasonal Analysis**: Quarterly and monthly forecast breakdowns
- **Uncertainty Visualization**: Confidence interval bands and statistics

---

##  Machine Learning Components

### Clustering Analysis
- **Algorithm**: K-Means clustering with optimal cluster selection
- **Features**: Monthly rainfall averages, seasonal patterns, variability metrics
- **Output**: Regional groupings based on similar precipitation patterns
- **Validation**: Silhouette analysis and within-cluster sum of squares

### Time Series Forecasting
- **Model**: Facebook Prophet with seasonal decomposition
- **Features**: Automatic trend detection, holiday effects, seasonal patterns
- **Validation**: Cross-validation with multiple forecast horizons
- **Uncertainty**: Confidence intervals and prediction bands

---

##  Use Cases

### 🌾 **Agricultural Planning**
- Identify optimal planting seasons based on rainfall patterns
- Plan irrigation schedules using forecast predictions
- Assess drought and flood risks for different regions

###  **Policy Making**
- Water resource management and allocation
- Climate change adaptation strategies
- Infrastructure planning for extreme weather events

###  **Research & Academia**
- Climate pattern analysis and documentation
- Comparative studies across Himalayan regions
- Educational tool for meteorology and data science

###  **Business Intelligence**
- Tourism industry weather planning
- Agricultural insurance risk assessment
- Renewable energy planning (hydroelectric potential)

---

##  Contributing

We welcome contributions from the community! Here's how you can help:

###  **Bug Reports**
- Use the [Issues](https://github.com/yourusername/bhutan-rainfall-explorer/issues) tab
- Provide detailed reproduction steps
- Include screenshots and error messages

###  **Feature Requests**
- Suggest new visualizations or analysis methods
- Propose UI/UX improvements
- Request additional data sources or regions

###  **Code Contributions**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

###  **Documentation**
- Improve README and code comments
- Add tutorials and usage examples
- Translate documentation to other languages

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Author

**Sangam Paudel**
-  Portfolio: [Your Portfolio Website]
-  LinkedIn: [Your LinkedIn Profile]
-  Email: [your.email@example.com]
-  Twitter: [@YourTwitterHandle]

---

##  Acknowledgments

- **Royal Government of Bhutan** - For providing rainfall data and supporting climate research
- **Streamlit Team** - For the amazing framework that makes data apps beautiful
- **Plotly Community** - For powerful interactive visualization capabilities
- **Facebook Prophet** - For robust time series forecasting algorithms
- **Python Data Science Community** - For the incredible ecosystem of tools and libraries

---

## 🔗 Related Projects

- [Climate Data Analysis Toolkit](https://github.com/example/climate-toolkit)
- [Himalayan Weather Patterns](https://github.com/example/himalayan-weather)
- [Streamlit Weather Dashboard](https://github.com/example/weather-dashboard)

---

##  Project Roadmap


###  **Future Enhancements**
- [ ] Satellite imagery integration
- [ ] Climate change impact analysis
- [ ] Cross-border precipitation comparisons
- [ ] Advanced statistical testing
- [ ] Custom alert systems

---

<div align="center">

### 🌄 Built with ❤️ for the Land of the Thunder Dragon 🐉

*Exploring Bhutan's climate patterns through the power of data science*

**[ Star this project](https://github.com/yourusername/bhutan-rainfall-explorer) if you found it helpful!**

</div>

---

*Last updated: June 2025*
