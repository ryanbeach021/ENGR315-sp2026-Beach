# Los Angeles Crime Analysis

###         ENGR 315
### Ryan Beach, Bodhi Theron, Arslan Malik

## Table of Contents
- Title
- Table of Contents
- Project Context
    - Our Questions
- Methods/Metrics
- Code Explanation
- Results
    - Dataset Errors
- Conclusions

## Project/Dataset Context
For this final project, we were tasked with examining a dataset of our interest and to produce questions, metrics,
and then visual results to answer those questions. Our selected dataset was the [Crime Data from 2020 to 2024 in Los Angeles](https://catalog.data.gov/dataset/crime-data-from-2020-to-present?from_hint=eyJzb3J0IjoicG9wdWxhcml0eSJ9). We were interested in this dataset because we were curious how the COVID-19 pandemic may have affected overall crime rates.
Within our dataset, there was over 1 million entries with a variety of information including the type of crime, date, time of day,
location, area, and victim age. From this dataset we formulated the following questions. 


### Our Questions
1. How has the total and frequency of different types of crimes changed over time from 2020 to 2024?
2. How does the type of crime vary across different areas or neighborhoods in Los Angeles?
3. How does the time of day influence the frequency and type of crimes committed?

With these questions we were then able to create metrics and methods to filter and analyze this data.

## Metrics
1. Question 1
    1. Total crimes per year (2020–2023)
    2. 2-Year Moving Average
    3. Average Daily Crimes (mean)
    4. Standard Deviation
    5. T-Test comparing 2020 vs 2023
2. Question 2
    1. Total Crimes per Area
    2. Percentage Distribution
3. Question 3
    1. Number of Crimes per Hour
    2. Peak Crime Hour

## Code Explanation
The overall flow is Load Data -> clean Data -> Transform Data -> Analyze Patterns -> Visualize Results -> Perform Statistical Tests.

It starts by importing external Python libraries with lines. Pandas is used for reading the csv files, organizing the data tables, filtering, grouping, and cleaning the data. matplotlib is used for creating the plots, line graphs, and bar graphs. scripy.stats is used for the t-test function. 

    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import ttest_ind

Next the dataset is loaded using the following lines. The DataFrame allows us to look at the csv file and sort data within the columns and rows and analyize them indivually.

    file_path = "Crime_Data_from_2020_to_2024.csv"
    df = pd.read_csv(file_path)

After loading and reading the data, we need to clean the data. This is important because every entry might not be counted the same with small syntax errors including hidden spaces. Hence the line, df.columns = df.columns.str.strip(), which removes accidental spaces before or after column names. 

Some additional cleaning and formatting is done by converting the date column into datetime objects with a specified format, and removing invalid dates. 

The following lines are then used to create solo columns with only the year or month. This will then make grouping and analysis much easier. The next lines convert the time into the HHMM format and then extract just the first two digits to represent the hour. 

    df['YEAR'] = df['DATE OCC'].dt.year
    df['MONTH'] = df['DATE OCC'].dt.month
    df['TIME OCC'] = df['TIME OCC'].astype(int).astype(str).str.zfill(4)
    df['HOUR'] = df['TIME OCC'].str[:2].astype(int)

The .groupby function is then used to group variables into their sections, and then the size() functio takes the total amount of numbers within each group, creating size and answers to our total amount of crimes per year. This is repeated for other sections such as the amount of crimes in a certain area. 

With some formattable answers, we look to our matplotlib to create graphs. The following code formats things such as title, axis labels, a grid, and a legend to create a nice looking figure. 

    plt.figure()
    crimes_per_year.plot(marker='o', label='Total Crimes')
    rolling_avg.plot(label='2-Year Moving Avg')
    plt.title("Crime Trend Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Crimes")
    plt.legend()
    plt.grid()
    plt.show()
  
## Results
### Dataset Errors
After some intial analysis and produced graphs, we noticed some heavy outliers that lead us to believe there were some errors in the dataset. Firstly, the crime in 2024 greatly decreased. After some intial research we discovered that the Los Angeles Police Department transitioned to a new record system in March of 2024, and thus the 2024 data was incomplete. As a solution, we decided to just remove any of the 2024 data using the following line of code. 

    df = df[df['YEAR'] < 2024]

In additon, the graph of the crime per hour of the data showed a sinusodial wave trend but with a large spike in at noon. After looking at the dataset directly, it became apparent that any crime entry without a recorded time resulted in a default time of exactly 1200. With some filtering, we were able to smooth out the data to a closer expected value, allowing us to determine the actual peak data. 

## Conclusions
### Question Conclusions
1. There was a drop in crime during the COVID-19 pandemic, which appears as an increase in crime in the following years. This aligns with what we expected as the pandemic kept lots of people isolated and this was shown as a clear trend in our findings. As for specific types of crimes, there was no clear trend as each crime followed the general overall increase. 
2. The crime distribution in LA is similar to other cities where certain areas are more dangerous than others. Crime is spread out through LA, but certain areas have much higher levels of crime such as in Central LA and 77th Street. After some research, these trends matched the expected results as these areas are known for a high gang prevelance. 
3. Crime frequency follows an oscillating pattern with crime being highest around 6pm, and being lowest at 5am. This pattern makes sense as crime tends to increase during evening hours, and would be lowest during sleeping hours. However, we expected this data to be shifted slightly right with crime peaking closer to 9pm.

