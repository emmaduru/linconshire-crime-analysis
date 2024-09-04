import pandas as pd
import string

raw_crime_df = pd.read_csv("2024-03-lincolnshire-street.csv")

# Get select columns
crime_df = raw_crime_df[["Longitude", "Latitude", "Location", "LSOA name", "Crime type"]]
# Format location column
crime_df["Location"] = crime_df["Location"].apply(lambda x: string.capwords(x.replace("On or near ", "")))
# Format City column
crime_df["City"] = crime_df["LSOA name"].apply(lambda x: " ".join(x.split(" ")[:-1]))
    

# Get number of total crimes per city
city_s = crime_df["City"].value_counts()
city_df = pd.DataFrame({"City": city_s.index, "All Crimes": city_s.values})

# Number of crimes by type
city_and_type_s = crime_df[["City", "Crime type"]].value_counts()
type_df = pd.DataFrame(city_and_type_s).reset_index()
type_df = type_df.pivot(index="City", columns='Crime type', values="count")

# Fill null values
type_df = type_df.fillna(0)

# Convert all columns except city to integers
type_df = type_df.astype(int)
type_df = type_df.reset_index()

# Join the pivotted table with the city_df DataFrame
all_crime_df = pd.merge(city_df, type_df, how="inner", on="City")

cities = list(all_crime_df["City"])

crimes = list(all_crime_df.columns)[1:]