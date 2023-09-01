import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Skyroot Comparative Analysis", page_icon="📚", layout="wide")
# warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*PyplotGlobalUseWarning.*")
st.set_option('deprecation.showPyplotGlobalUse', False)


# Load the dataset
# @st.cache
def load_data():
    data = pd.read_csv('Space_Corrected.csv')  # Replace with the actual path
    return data


data = load_data()


# Convert 'Datum' column to datetime format with custom format
def custom_datetime_parser(datum_str):
    try:
        return pd.to_datetime(datum_str, format='%a %b %d, %Y %H:%M UTC')
    except ValueError:
        return pd.to_datetime(datum_str, format='%a %b %d, %Y')


data['Datum'] = data['Datum'].apply(custom_datetime_parser)

# Extract year from the 'Datum' column and add it as a new column
data['Year'] = data['Datum'].dt.year

# App title
st.title('Space Launch Analysis')

# Sidebar filters
st.sidebar.header('Filters')
min_year = data['Year'].min()
max_year = data['Year'].max()
years = st.sidebar.slider('Select Year Range', min_year, max_year, (min_year, max_year))

# Apply filters
filtered_data = data[(data['Year'] >= years[0]) & (data['Year'] <= years[1])]

# Data Analysis
# st.header('Data Analysis')

# Display the total number of launches
st.subheader('Total Number of Launches: {}'.format(len(filtered_data)))

success_rate = round(len(filtered_data[filtered_data['Status Mission'] == 'Success']) / len(filtered_data) * 100,2)
# Display launch success rate
st.subheader('Launch Success Rate: {} %'.format(success_rate))

# st.write(f'{success_rate:.2f}%')

st.header('Space Launch Data From  1957')
# st.set_page_config(page_title="Space Launch Analysis")
st.dataframe(filtered_data.iloc[:, 2:])
# Data Visualization
# st.header('Data Visualization')

# Launches by Company (using Matplotlib)
st.subheader('Launches by Company')
launches_by_company = filtered_data['Company Name'].value_counts()
plt.figure(figsize=(12, 10))
sns.barplot(x=launches_by_company.values, y=launches_by_company.index)
plt.xlabel('Number of Launches')
plt.ylabel('Company Name')

# Rotate y-labels for better readability
plt.yticks(rotation=0, ha="right")

# plt.tight_layout()  # Adjust layout
st.pyplot()

# Launch Status (using Matplotlib)
st.subheader('Launch Status')
launch_status = filtered_data['Status Mission'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(launch_status, labels=launch_status.index, autopct='%1.1f%%', startangle=140)
plt.title('Launch Status')
st.pyplot()
# Disable the specific warning
# st.header('Launch Locations on Map')

# Create a geocoder instance
st.header('Country/Location of Launch')
launches_by_country = filtered_data['Location'].apply(lambda x: x.split(', ')[-1]).value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=launches_by_country.index, y=launches_by_country.values)
plt.xlabel('Country')
plt.ylabel('Number of Launches')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()

# Load the additional dataset
rockets_data = pd.read_csv('all-rockets-from-1957.csv')  # Replace with the actual path

# Convert payload to LEO and GTO values to kilograms
rockets_data['Payload to LEO (kg)'] = rockets_data['Payload to LEO'] * 1000
rockets_data['Payload to GTO (kg)'] = rockets_data['Payload to GTO'] * 1000
import re


# ... (previous code)
def extract_price(price_str):
    try:
        # Use regular expression to extract numeric part and convert to float
        numeric_part = re.search(r'(\d+\.\d+)', price_str).group(1)
        return float(numeric_part)
    except:
        return None
    # Rockets vs. Price


st.header('Launch Vehicle Data')
# st.set_page_config(page_title="Space Launch Analysis")
st.dataframe(rockets_data.iloc[:, 1:])

rockets_data['Price'] = rockets_data['Price'].apply(extract_price)

st.header('Rockets vs. Price [Million USD]')
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=rockets_data.dropna(subset=['Price']), x='Sr', y='Price')
plt.xlabel('Rocket Serial Number From Data')
plt.ylabel('Price in Million USD')
# plt.xticks(rotation=45, ha="right")
x_labels = [label if i % 4 == 0 else '' for i, label in enumerate(ax.get_xticklabels())]
ax.set_xticklabels(x_labels)
plt.tight_layout()
st.pyplot()

# Rockets vs. Payload to LEO
st.header('Rockets vs. Payload to LEO (Kg)')
plt.figure(figsize=(10, 6))
ax2 = sns.barplot(data=rockets_data, x='Sr', y='Payload to LEO (kg)')
plt.xlabel('Rocket Serial Number From Data')
plt.ylabel('Payload to LEO (kg)')
# plt.xticks(rotation=45, ha="right")
x_labels = [label if i % 20 == 0 else '' for i, label in enumerate(ax2.get_xticklabels())]
ax2.set_xticklabels(x_labels)
plt.tight_layout()
st.pyplot()

# Rockets vs. Payload to GTO
st.header('Rockets vs. Payload to GTO (Kg)')
plt.figure(figsize=(10, 6))
ax3 =sns.barplot(data=rockets_data, x='Sr', y='Payload to GTO (kg)')
plt.xlabel('Rocket Serial Number From Data')
plt.ylabel('Payload to GTO (kg)')
# plt.xticks(rotation=45, ha="right")
x_labels = [label if i % 20 == 0 else '' for i, label in enumerate(ax3.get_xticklabels())]
ax3.set_xticklabels(x_labels)
plt.tight_layout()
st.pyplot()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
