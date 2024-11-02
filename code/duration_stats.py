import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sn
import statsmodels.api as sm

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv('netflix_data.csv')
#print(netflix_df.shape)
#print(netflix_df.info())
#print(netflix_df.head(3))

# Subset the DataFrame for type "Movie"
netflix_subset = netflix_df[netflix_df["type"] == "Movie"]

# Select only the columns of interest
netflix_movies = netflix_subset[["title", "country", "genre", "release_year", "duration"]]

###Duration###

# Filter for durations shorter than 60 minutes
short_movies = netflix_movies[netflix_movies.duration < 60]
#print(short_movies.info)


# Filter also for durations longer than 250 minutes to exclude outliers and movies released before 1960 (too few dataopint before that).
netflix_movies=netflix_movies[(netflix_movies['duration'] >= 60) & (netflix_movies['duration'] < 250 ) & (netflix_movies['release_year'] >= 1970)]
#print(netflix_movies.info)

#Filter out uncategorized movies.
uncategorized=netflix_movies[netflix_movies['genre'] == 'Uncategorized']
#print(uncategorized.index)

netflix_movies=netflix_movies.drop(index=[1318, 1320, 1570, 1709, 2177, 2178, 3253, 3736, 3737, 3738, 4187, 5576, 5577, 6735, 7170, 7171])

duration_year=netflix_movies[['genre','release_year','duration']]


#Check for null data.

#Where there years where no movies were released?
all_years=range(1970,2020)
years_movies=duration_year["release_year"].isin(all_years)
no_movies_y=years_movies[years_movies==False]

#print(years_movies.value_counts())

#print(len(no_movies_y.index))
drops=list(no_movies_y.index)

#Drop those rows and reset index.
duration_year=duration_year.drop(index=drops).reset_index(drop=True)

#Check.
print(duration_year.shape)

#Remove rows with other null elements
#print(duration_year.iloc[:,2].index)

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
#print(genres)

#Plot general distribution in a histogram.
palette=sn.color_palette("Spectral", as_cmap=True,n_colors=180)
fig=sn.histplot(duration_year,x='release_year',y='duration',palette=palette,hue='duration',legend =False,binwidth=1,discrete=(True, False))
fig.set(xlabel="Release year",ylabel="Duration (min)")
fig.set(title="Movie duration by year of release")
fig.tick_params(labelsize=7)
plt.show()

#Remove 'Independent movies', 'International movies','Classic Movies' and 'Cult movies'
no_mov=['International Movies','Classic Movies','Independent Movies', 'Cult Movies']

for j in no_mov:
    if str(j) in duration_year[['genre']].values:
        print(j)
        k=duration_year[duration_year['genre'] == j].index
        print(k)
    else:
        continue


classic=[ 114,  246,  247,  255,  310,  481,  487,  518,  640,  757,  851,  965,
       1263, 1265, 1322, 1444, 1465, 1482, 1661, 1678, 1682, 2022, 2104, 2121,
       2174, 2375, 2492, 2778, 2826, 2872, 2944, 2984, 2990, 3004, 3206, 3439,
       3441, 3514, 3526, 3687, 3736, 3854, 3861, 3895, 3943, 3959, 4428, 4465]

cult=[746, 818, 1051, 1271, 2278, 2748, 3508, 3657, 3829, 4083, 4542]

independent=[  10,  435,  525,  630,  688,  711,  720,  825,  977,  979, 1134, 1186,
       1333, 1451, 1751, 2134, 2402, 3653, 3734]

indeces=classic+cult+independent
dur_year=duration_year.drop(index=indeces)
print(dur_year.shape)

international=dur_year[dur_year['genre'] == 'International Movies'].index
dur_yea=dur_year.drop(index=international)
print(dur_yea.shape)

#Plot general distribution for clean df in a histogram. 
palette=sn.color_palette("Spectral", as_cmap=True,n_colors=180)
fig2=sn.histplot(dur_yea,x='release_year',y='duration',palette=palette,hue='duration',legend =False,binwidth=1,discrete=(True, False))
fig2.set(xlabel="Release year",ylabel="Duration (min)")
fig2.set(title="Movie duration by year of release")
fig2.tick_params(labelsize=7)
plt.show()

#Check remaining genres and amount of unique labels.
genres=dur_yea['genre'].value_counts()
print(genres)
print(len(dur_yea['genre'].unique()))

#Check period of time covered--> 50 years
data_year=dur_yea['release_year'].unique()
print(len(data_year))

#Plot scatter  with genre as hue.
palette=sn.color_palette("colorblind",n_colors=14)
fig3=sn.scatterplot(dur_yea,x='release_year',y='duration',palette=palette,hue='genre',legend =False)
fig3.set(xlabel="Release year",ylabel="Duration (min)")
fig3.set(title="Movie duration by year of release")
fig3.tick_params(labelsize=7)
plt.show()

print(dur_yea['duration'].describe())


#Plot data with a linear regression model, specifying estimator and including versions with locally weighted estimates (lowess).
fig4=sn.regplot(dur_yea,x='release_year',y='duration',color=(255/255, 138/255, 101/255,0.8),line_kws={'color':'royalblue'},scatter=True,lowess=True)
fig4.set(xlabel="Release year",ylabel="Duration (min)")
fig4.set(title="Movie duration by year of release")
fig4.tick_params(labelsize=7)
plt.show()


