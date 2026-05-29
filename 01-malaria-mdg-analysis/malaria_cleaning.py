"""
Global Malaria Data Cleaning Pipeline
Author: Joshua Thomas Babale
Purpose: Unpivot wide CSV with Region + year columns, get top 10 countries for 2019
Input: Global_Malaria_Case.csv with format: Region,1990,1991,...,2019
Output: malaria-data.xlsx with columns as Year, Country, Cases
"""

import pandas as pd

# 1. LOAD DATA
df = pd.read_csv('Global_Malaria_Case.csv')
print("Original shape:", df.shape)
print("First 5 columns:", df.columns.tolist()[:5])

# 2. STANDARDIZE COLUMN NAMES FOR PROCESSING
df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={'region': 'country'})

# 3. UNPIVOT: Convert year columns to rows for Excel/Power BI
year_columns = [col for col in df.columns if col.isdigit()]
df_long = pd.melt(
    df,
    id_vars=['country'],
    value_vars=year_columns,
    var_name='year',
    value_name='cases'
)

print("After unpivot:", df_long.shape)

# 4. CLEAN DATA TYPES
df_long['year'] = df_long['year'].astype(int)
df_long['cases'] = df_long['cases'].astype(str).str.replace(',', '')
df_long['cases'] = pd.to_numeric(df_long['cases'], errors='coerce').fillna(0).astype(int)

# 5. REMOVE AGGREGATE ROWS like 'World' or 'Africa' if they exist
aggregates = ['world', 'africa', 'americas', 'south-east asia', 'europe', 
              'eastern mediterranean', 'western pacific', 'global']
df_long = df_long[~df_long['country'].str.lower().isin(aggregates)]

# 6. CAPITALIZE FINAL COLUMN NAMES: Year, Country, Cases
df_long = df_long.rename(columns={
    'country': 'Country',
    'year': 'Year', 
    'cases': 'Cases'
})

# 7. TOP 10 COUNTRIES FOR 2019 ONLY
top_10_2019 = (
    df_long[df_long['Year'] == 2019]
    .sort_values('Cases', ascending=False)
    .head(10)[['Country', 'Year', 'Cases']]
)

print("\nTop 10 Countries in 2019:")
print(top_10_2019)

# 8. SAVE FILES
df_long.to_excel('malaria-data.xlsx', index=False)
top_10_2019.to_csv('malaria_top10_2019.csv', index=False)

print("\nFiles saved:")
print("- malaria-data.xlsx: Columns = Country, Year, Cases")
print("- malaria_top10_2019.csv: Top 10 for 2019")
