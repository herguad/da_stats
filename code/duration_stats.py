import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sn

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv('netflix_data.csv')
#print(netflix_df.shape)
#print(netflix_df.info())
#print(netflix_df.head(3))

# Subset the DataFrame for type "Movie"
netflix_subset = netflix_df[netflix_df["type"] == "Movie"]

# Select only the columns of interest
netflix_movies = netflix_subset[["title", "country", "genre", "release_year", "duration"]]

# Filter for durations shorter than 60 minutes
short_movies = netflix_movies[netflix_movies.duration < 60]
#print(short_movies.info)

# Filter also for durations longer than 250 minutes to exclude outliers and movies released before 1960 (too few dataopint before that).
netflix_movies=netflix_movies[(netflix_movies['duration'] >= 60) & (netflix_movies['duration'] < 250 ) & (netflix_movies['release_year'] > 1960)]
print(netflix_movies.info)

#Filter out uncategorized movies.
uncategorized=netflix_movies[netflix_movies['genre'] == 'Uncategorized']
#print(uncategorized.index)

netflix_movies=netflix_movies.drop(index=[1318, 1320, 1570, 1709, 2177, 2178, 3253, 3736, 3737, 3738, 4187, 5576, 5577, 6735, 7170, 7171])

duration_year=netflix_movies[['genre','release_year','duration']]

#Check for null values.
#Where there years where no movies were released?
all_years=range(1960,2020)
years_movies=duration_year["release_year"].isin(all_years)
no_movies_y=years_movies[years_movies==False]

print(years_movies.value_counts()) #<-- 352
print(len(no_movies_y.index))

#Drop those rows and reset index.
drops=list(no_movies_y.index)
duration_year=duration_year.drop(index=drops).reset_index()

#Check.
print(duration_year.shape)

#Remove rows with other null elements
print(duration_year.iloc[:,2].index)

for i in range(0,2):
    for c in duration_year.iloc[:,i].index:
        if (duration_year.iloc[c,i] == '') is True:
            duration_year.drop(index=c)
        else:
            continue
        
print(len(duration_year))
print(duration_year.head())

# Visualize missingness
msno.matrix(duration_year)
plt.show()

#Check categorical variable consistency.
genres=duration_year['genre'].value_counts()
print(genres)

#Plot general distribution in a histogram.
palette=sn.color_palette("Spectral", as_cmap=True,n_colors=190)
fig=sn.histplot(duration_year,x='release_year',y='duration',palette=palette,hue='duration',legend =False,binwidth=1,discrete=(True, False))
fig.set(xlabel="Release year",ylabel="Duration (min)")
fig.set(title="Movie duration by year of release")
fig.tick_params(labelsize=7)
plt.show()

#Remove movies with ambiguous or vague names.
no_mov=['International Movies','Classic Movies','Independent Movies', 'Cult Movies']

#Identify indeces
for j in no_mov:
    if str(j) in duration_year[['genre']].values:
        print(j)
        k=duration_year[duration_year['genre'] == j].index
        print(k)
    else:
        continue
        


