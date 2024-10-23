import pandas as pd
import numpy as np
import scipy as sp

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
movies_sel=netflix_subset.loc[:,('country','date_added','genre')]
movies_sel.loc[:,('date_added')]=pd.to_datetime(movies_sel.loc[:,('date_added')])
movies_sel['year_added']=movies_sel['date_added'].values  #Ignore warning but read: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
movies_sel['year_added']=movies_sel['year_added'].dt.year

#Add different dfs selecting release_year and genre and genre separately
movies_genre_year=movies_sel.loc[:,('genre','year_added')]
movies_country_genre=movies_sel.loc[:,('country','genre')]

#Group movies by genre and year added, and count genres movies added per year. 
m_genre_year=movies_genre_year.groupby(["genre","year_added"]).value_counts(ascending=True).reset_index(name='movies_per_genreyear')
#print(m_genre_year)

#Count uncategorized movies and remove.
#Stats based on years when movies were added.
uncategorized_s=m_genre_year[m_genre_year['genre']=='Uncategorized']['movies_per_genreyear'].sum()
uncategorized=m_genre_year[m_genre_year['genre']=='Uncategorized']
#print(len(uncategorized))

#Separate international movies into a different df and remove from main.
international_movies_g= movies_genre_year[movies_genre_year['genre']=='International Movies']
#print(international_movies_g.index)

movies_genre_year=m_genre_year.drop(index=[74, 75, 76, 77, 78, 79,107,108,109,110,111,112,113]).reset_index(drop=True)

#print(movies_genre_year) #--> check n of rows is 13 down.

#print(movies_genre_year['genre'].unique()) # <- 18 distinct genres after cleaning

