import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sn
#import statsmodels.api as sm

# Read in the Netflix CSV as a DataFrame
netflix_df = pd.read_csv('netflix_data.csv')
#print(netflix_df.shape)
#print(netflix_df.info())
#print(netflix_df.head(3))

# Subset the DataFrame for type "Movie"
netflix_subset = netflix_df[netflix_df["type"] == "Movie"]

# Select only the columns of interest
netflix_movies = netflix_subset[["title", "country", "genre", "release_year", "duration"]]

###Genre###
#Select columns of interest. Transform date column into datetype and extract year from dates and re-write cdate_added column to show just years.
movies_sel=netflix_subset.loc[:,('country','date_added','genre','duration')]
movies_sel.loc[:,('date_added')]=pd.to_datetime(movies_sel.loc[:,('date_added')])
movies_sel['year_added']=movies_sel['date_added'].values  #Ignore warning but read: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
movies_sel['year_added']=movies_sel['year_added'].dt.year

#Add different dfs selecting release_year and genre and genre separately
genre_year=movies_sel.loc[:,('genre','year_added','duration')]
movies_country_genre=movies_sel.loc[:,('genre','duration')]

#Group movies by genre and year added, and count genres movies added per year. 
m_genre_year=genre_year.groupby(["genre","duration"]).value_counts(ascending=True).reset_index(name='genreyear')
#print(m_genre_year)

#Count uncategorized movies and remove.
#Stats based on years when movies were added.
uncategorized_s=m_genre_year[m_genre_year['genre']=='Uncategorized']['genreyear'].sum()
uncategorized=m_genre_year[m_genre_year['genre']=='Uncategorized']
#print(len(uncategorized))

#Separate international movies into a different df and remove from main.
international_movies_g= genre_year[genre_year['genre']=='International Movies']
#print(international_movies_g.index)

genre_year=m_genre_year.drop(index=[74, 75, 76, 77, 78, 79,107,108,109,110,111,112,113]).reset_index(drop=True)
genre_year=genre_year.sort_values(by='year_added',ascending=True)

print(genre_year) #--> check n of rows is  down.

print(genre_year['genre'].unique()) # <-  distinct genres after cleaning

#Check categorical variable consistency.
genre_sum=genre_year['genre'].value_counts()
print(genre_sum)


#Remove 'Independent movies', 'International movies','Classic Movies' and 'Cult movies'
no_mov=['Classic Movies','Independent Movies', 'Cult Movies', 'Uncategorized']

for j in no_mov:
    if str(j) in genre_year[['genre']].values:
        print(j)
        k=genre_year[genre_year['genre'] == j].index
        print(k)
    else:
        continue

classic=[24, 25, 26, 27, 28, 29]

cult=[38, 39, 40, 41, 42]

independent=[70, 71, 72, 73]

uncategorized=[2328, 2314, 2317, 2337, 2327, 2308, 2335, 2324, 2312, 2333, 2348, 2306,
       2316, 2340, 2332, 2302, 2305, 2321, 2344, 2350, 2341, 2342, 2330, 2345,
       2346, 2331, 2322, 2325, 2326, 2347, 2311, 2303, 2309, 2307, 2313, 2339,
       2338, 2349, 2320, 2323, 2315, 2304, 2334, 2329, 2336, 2318, 2343, 2319,
       2310, 2351]

indeces=classic+cult+independent+uncategorized
gen_year=genre_year.drop(index=indeces).sort_values(by='duration',ascending=True)
print(gen_year.shape)


# Visualize missingness
msno.matrix(gen_year)
plt.show()

palette=sn.color_palette("colorblind",n_colors=18)
fig=sn.catplot(gen_year,x='genre',y='duration',palette=palette,hue='genre',legend =False,kind='bar')
fig.set(xlabel="Genre",ylabel="Duration (min)")
fig.set(title="Movie duration by genre")
fig.tick_params(labelsize=8)
plt.xticks(rotation=30)
plt.show()


#Check categorical variable consistency.

genre_sum=genre_year.groupby('genre')['genre'].count().reset_index(name='mcount')
genre_sum=genre_sum.sort_values(by='mcount',ascending=False)
print(genre_sum)


#filter out genres with fewer than 11 observations
genre_sum=genre_sum[genre_sum['mcount'] > 11].reset_index(drop=True)
print(genre_sum)


no_mov=['Classic Movies','Independent Movies', 'Cult Movies', 'Uncategorized']

for j in no_mov:
    if str(j) in genre_sum[['genre']].values:
        print(j)
        k=genre_sum[genre_sum['genre'] == j].index
        print(k)
    else:
        continue

gen_sum=genre_sum.drop(index=[8,9,11,14]).sort_values(by='mcount',ascending=True)

#Check resulting number of genres to specify palette n_colors next.
print(gen_sum['genre'].unique())


palette=sn.color_palette("colorblind",n_colors=11)
fig1=sn.catplot(gen_sum,x='genre',y='mcount',palette=palette,hue='genre',legend =False,kind='bar')
fig1.set(xlabel="Genre",ylabel="Sum")
fig1.set(title="Movie count by genre")
fig1.tick_params(labelsize=8)
plt.xticks(rotation=30)
plt.show()

print(gen_sum.describe())

#Further remove movies with fewer than 50 movies.
genre_tops=genre_sum[genre_sum['mcount'] > 50]
print(genre_tops)
print(genre_tops['genre'].unique())
print(genre_tops.describe())


palette=sn.color_palette("colorblind",n_colors=9)
fig2=sn.catplot(genre_tops,x='genre',y='mcount',palette=palette,hue='genre',legend =False,kind='bar')
fig2.set(xlabel="Genre",ylabel="Sum")
fig2.set(title="Movie count by genre")
fig2.tick_params(labelsize=8)
plt.xticks(rotation=30)
plt.show()