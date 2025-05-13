# covid_analysis.py

# 📦 Importing required libraries
import pandas as pd  # For data loading and manipulation
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For enhanced plot styling
import os  # To check if the file exists
from datetime import datetime  # To work with date objects

# 📂 Step 1: Load the CSV dataset
try:
    # Replace 'owid-covid-data.csv' with your actual dataset path if needed
    file_path = 'owid-covid-data.csv'

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError("Dataset file not found!")

    # Read the CSV file
    df = pd.read_csv(file_path)
    print("✅ Dataset loaded successfully!")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    exit()

# 👁️ Step 2: Explore the dataset
print("\n🔍 First 5 rows of data:")
print(df.head())

print("\n📊 Dataset info:")
print(df.info())

print("\n🧼 Checking for missing values:")
print(df.isnull().sum())

# 🧹 Step 3: Data Cleaning
# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter for a few countries of interest
countries = ['Kenya', 'India', 'United States']
df = df[df['location'].isin(countries)]

# Fill missing numeric values with 0 for simplicity (you can improve this)
df.fillna(0, inplace=True)

# 📈 Step 4: Basic Analysis
print("\n📈 Descriptive statistics:")
print(df.describe())

# 💡 Calculating death rate
df['death_rate'] = df['total_deaths'] / df['total_cases']
df['death_rate'].fillna(0, inplace=True)  # Replace NaN with 0

# 📊 Step 5: Visualization Setup
sns.set(style="darkgrid")
plt.figure(figsize=(12, 6))

# 🔹 Line chart: Total cases over time
for country in countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('📈 Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()

# 🔹 Bar chart: Average total deaths per country
avg_deaths = df.groupby('location')['total_deaths'].max()
avg_deaths.plot(kind='bar', color='orange', title='☠️ Max Total Deaths per Country')
plt.ylabel('Deaths')
plt.tight_layout()
plt.show()

# 🔹 Histogram: Distribution of new cases
plt.hist(df['new_cases'], bins=50, color='purple')
plt.title('📊 Distribution of New COVID-19 Cases')
plt.xlabel('New Cases')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 🔹 Scatter plot: Total cases vs Total deaths
plt.scatter(df['total_cases'], df['total_deaths'], alpha=0.5, c='red')
plt.title('🔬 Total Cases vs Total Deaths')
plt.xlabel('Total Cases')
plt.ylabel('Total Deaths')
plt.tight_layout()
plt.show()

# 💉 Step 6: Vaccination Analysis
plt.figure(figsize=(12, 6))
for country in countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title('💉 COVID-19 Vaccination Progress Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()

# 📝 Step 7: Summary Insights (printed to console)
print("\n📌 Summary Insights:")
for country in countries:
    latest = df[df['location'] == country].sort_values(by='date').iloc[-1]
    print(f"\n📍 {country} as of {latest['date'].date()}:")
    print(f"  Total Cases: {int(latest['total_cases'])}")
    print(f"  Total Deaths: {int(latest['total_deaths'])}")
    print(f"  Death Rate: {latest['death_rate']:.2%}")
    print(f"  Total Vaccinations: {int(latest['total_vaccinations'])}")

