#ENGR 315 - Final Project
#Los Angeles Crime Analysis
#Group 8 - Ryan Beach, Arslan Malik, Bodhi Theron

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

#absolute file path
file_path = "C:/Users/ryanb/OneDrive/Desktop/School/Engineering/ENGR 315/ENGR315-Project8/Crime_Data_from_2020_to_2024.csv"

#relative file path
#file_path = "Crime_Data_from_2020_to_2024.csv"
df = pd.read_csv(file_path)

#Cleaning:
df.columns = df.columns.str.strip() #cleans columns spaces
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'],format='%m/%d/%Y %I:%M:%S %p', errors='coerce')    #converts date column

df = df.dropna(subset=['DATE OCC']) #remove invalid dates

#extracts the year and month
df['YEAR'] = df['DATE OCC'].dt.year
df['MONTH'] = df['DATE OCC'].dt.month    

#removes 2024 data
df = df[df['YEAR'] < 2024]   #after analysis, determined that the data was incomplete for 2024

df = df.dropna(subset=['TIME OCC'])

df['TIME OCC'] = df['TIME OCC'].astype(int).astype(str).str.zfill(4)
df['HOUR'] = df['TIME OCC'].str[:2].astype(int)


#QUESTION 1: How has crime frequency changed over time?

print("\n QUESTION 1: CRIME OVER TIME ")

crimes_per_year = df.groupby('YEAR').size()
print("\nCrimes per Year:\n", crimes_per_year)  #Finds and prints total crimes per year  

#finds and prints growth rate
growth_rate = crimes_per_year.pct_change() * 100
print("\nYearly Growth Rate (%):\n", growth_rate)

#a moving average
rolling_avg = crimes_per_year.rolling(window=2).mean()

#sorts by crime type per year
crime_type_year = df.groupby(['YEAR', 'Crm Cd Desc']).size().unstack(fill_value=0)

#Plot for total crimes per year along with moving average
plt.figure()
crimes_per_year.plot(marker='o', label='Total Crimes')
rolling_avg.plot(label='2-Year Moving Avg')
plt.title("Crime Trend Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Crimes")
plt.legend()
plt.grid()
plt.show()

#Students T-Test (2020 vs 2023) to analysis the signifance between the different means
valid_dates = df.copy()
valid_dates['DATE'] = valid_dates['DATE OCC'].dt.date

daily_crimes = valid_dates.groupby(['YEAR', 'DATE']).size().reset_index(name='TOTAL CRIMES')

daily_crimes_2020 = daily_crimes.loc[daily_crimes['YEAR'] == 2020, 'TOTAL CRIMES']
daily_crimes_2023 = daily_crimes.loc[daily_crimes['YEAR'] == 2023, 'TOTAL CRIMES']

#metrics looking at overall average daily crimes vs standard deviation in 2020 vs 2023
print("\nAverage Daily Crimes (2020):", daily_crimes_2020.mean())
print("Average Daily Crimes (2023):", daily_crimes_2023.mean())

print("Standard Deviation (2020):", daily_crimes_2020.std())
print("Standard Deviation (2023):", daily_crimes_2023.std())



#look at the top crimes over time
top_crimes = df['Crm Cd Desc'].value_counts().head(5).index
filtered = df[df['Crm Cd Desc'].isin(top_crimes)]

crime_trends = filtered.groupby(['YEAR', 'Crm Cd Desc']).size().unstack()

print("\nTop Crime Types:\n", top_crimes)

crime_trends.plot()
plt.title("Crime Types Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Crimes")
plt.legend(title="Crime Type")
plt.show()

# QUESTION 2: How does crime vary by area?

print("\n QUESTION 2: CRIME BY AREA")

#total crimes per areea
crimes_by_area = df['AREA NAME'].value_counts()
print("\n Crime per Areas:\n", crimes_by_area)

#percent distribution
crime_percent = (crimes_by_area / crimes_by_area.sum()) * 100
print("\n Crime Percentage by Area (Top 10):\n", crime_percent.head(10))

#plot for the top 10 areas of crime count
plt.figure()
crimes_by_area.head(10).plot(kind='bar')
plt.title("Top 10 Areas by Crime Count")
plt.xlabel("Area")
plt.ylabel("Number of Crimes")
plt.xticks(rotation=45)
plt.show()


#QUESTION 3; How does the time of day influence crime?

print("\n QUESTION 3: TIME OF DAY")

df = df[df['TIME OCC'] != '1200'] #noticed a large spike at 12, came to conlusion entries without times entered as 1200


#finds the crimes per hour
crimes_per_hour = df.groupby('HOUR').size()
print("\nCrimes per Hour:\n", crimes_per_hour)

#used to find the peak crime hour
peak_hour = crimes_per_hour.idxmax()
print("\nPeak Crime Hour:", peak_hour)

#plots the crime at each hour of the day
plt.figure()
crimes_per_hour.plot(kind='bar')
plt.title("Crimes by Hour of Day")
plt.xlabel("Hour (0-23)")
plt.ylabel("Number of Crimes")
plt.xticks(rotation=0)
plt.show()


#Code used to confirm 2024 was incomplete
#print(df['DATE OCC'].max())
#df['MONTH'] = df['DATE OCC'].dt.month
#monthly_2024 = df[df['YEAR'] == 2024]['MONTH'].value_counts().sort_index()
#print(monthly_2024)
