import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the satellite data
# @st.cache
def load_data():
    data = pd.read_excel('Satellite_Data.xlsx')
    return data


data = load_data()
st.set_page_config(page_title="Satellite Data Analysis", page_icon="📚", layout="wide")
# warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*PyplotGlobalUseWarning.*")
st.set_option('deprecation.showPyplotGlobalUse', False)
# Set the title and header
st.title("Satellite Data Analysis")
st.header("Explore Satellite Information")

# # 1. Satellite Count by Country
st.subheader("Satellite Count by Country")
satellite_count_by_country = data['Country of Operator/Owner'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=satellite_count_by_country.index[:10], y=satellite_count_by_country.values[:10])
plt.xlabel('Country')
plt.ylabel('Number of Satellites')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()

# 2. Orbit Class Distribution
# Filter the data to include only specific orbit classes
valid_orbit_classes = ['LEO', 'MEO', 'GEO', 'Elliptical']
filtered_data = data[data['Class of Orbit'].isin(valid_orbit_classes)]

# Create the pie chart with the filtered data
st.subheader("Orbit Class Distribution")
orbit_class_distribution = filtered_data['Class of Orbit'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(orbit_class_distribution, labels=orbit_class_distribution.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot()

# 3. Satellite Purpose
st.subheader("Satellite Purpose")
purpose_distribution = data['Purpose'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=purpose_distribution.values, y=purpose_distribution.index)
plt.xlabel('Number of Satellites')
plt.ylabel('Purpose')
plt.tight_layout()
st.pyplot()

# 6. Country vs. Satellite Altitude
st.subheader("Country vs. Satellite Altitude")
country_altitude = data.groupby('Country of Operator/Owner')['Apogee (km)'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=country_altitude.values[:10], y=country_altitude.index[:10])
plt.xlabel('Average Apogee Altitude (km)')
plt.ylabel('Country')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()

# 13. Yearly Satellite Launch Trends
# 13. Yearly Satellite Launch Trends
# 13. Yearly Satellite Launch Trends
# st.subheader("Yearly Satellite Launch Trends")

# Print the 'Date of Launch' column before conversion
# print("Before conversion:")
# print(data['Date of Launch'])
# print(type(data['Date of Launch'][0]))

# Convert the "Date of Launch" column to datetime format and handle errors
# 13. Yearly Satellite Launch Trends
st.subheader("Yearly Satellite Launch Trends")

# Extract the year from the existing "Date of Launch" column
# Convert the "Date of Launch" column to datetime format
data['Date of Launch'] = pd.to_datetime(data['Date of Launch'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Extract the year from the datetime objects and assign it to a new column "Year"
data['Year'] = data['Date of Launch'].dt.year

# Count the number of launches per year
yearly_launches = data['Year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x=yearly_launches.index, y=yearly_launches.values)
plt.xlabel('Year')
plt.ylabel('Number of Satellites Launched')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()

# 14. Satellite Name Word Cloud
# from wordcloud import WordCloud
# st.subheader("Satellite Name Word Cloud")
# satellite_names = " ".join(data['Name of Satellite, Alternate Names'])
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(satellite_names)
# plt.figure(figsize=(10, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# st.pyplot()

# 16. Satellite Altitude vs. Launch Mass
st.subheader("Satellite Altitude vs. Launch Mass")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Apogee (km)', y='Launch Mass (kg.)', alpha=0.5)
plt.xlabel('Apogee Altitude (km)')
plt.ylabel('Launch Mass (kg.)')
plt.tight_layout()
st.pyplot()

# Extract the year from the "Date of Launch" column
data['Year'] = data['Date of Launch'].dt.year

# Group data by year and calculate the mean launch mass for each year
launch_mass_trend = data.groupby('Year')['Launch Mass (kg.)'].mean()

# Create the launch mass vs. year trend plot
st.subheader("Satellite Launch Mass vs. Year Trend")
plt.figure(figsize=(10, 6))
sns.lineplot(x=launch_mass_trend.index, y=launch_mass_trend.values)
plt.xlabel('Year')
plt.ylabel('Mean Satellite Launch Mass (kg.)')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

