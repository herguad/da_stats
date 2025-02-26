# Netflix Stats 
This project provides a more detailed analysis of hte Netflix db for movies up until 2020. It includes hypotheses about the possible reasons for the distribution of duration and release date for movies observed in the initial visualization of data and basic analyses can be found here, in a different project.

In the code folder, two files contain the code for the [duration](code\duration_stats.py) and [genre](code\genre_stats.py) stats, respectively and an img folder contains the different plots generated with the newly wrangled data, based on the cleaned, cropped and selected data following criteria aimed at proper hypothesis testing.


In both cases, the necesssary packages are imported, data is read into a df, which is immediately filtered to only display movie-related data. 

```python
import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns

netflix_df = pd.read_csv(r'pathway\netflix_data.csv')
```

Columns of interest are selected and filtering for specific duration and genre is done with the same criteria as shown in the initial visualization project (REF), i.e. to discard outliers and uncategorized or inexistent genres. Based on observations from the first project, the data is further filtered to only include rows for movies released between 1970 and 2020.

Next, null and NaN elements are filtered out in two short steps. First, via a simple nested loop, null elements are tracked along each column and rows containing null elements are dropped. Then, using `missingno` package, the cleaned df is further scanned for other NaNs.

<img src="imgs\na_values.png" alt="na_values">

After checking categorical variable consistency (for 'genre') a histogram is plotted to get a picture of the general distribution of 'duration' for different release years.

<img src="imgs\clean_dy.png" alt="clean_dy">

Rows for movies of genres 'independent', 'international', 'classic' and 'cult' movies were removed after identifying the specific indeces via a nested conditional in a for loop. The cleaned df was plotted in a new instagram using a gradient palette to better show data density for different years. 

When plotting genre as hue, the prevalence of certain genres over others become evident. Reference for genre has been omitted here since analysis for this variable will be taken up below.

<img src="imgs\dur_yea_gen_scatter.png" alt="genreashue">

## Variable correlation

Next step to assess possible correlation is first checking general stats with `.describe()`.
<p align="center">
<img src="imgs\describe_dur_year.png" alt="gral_stats_dur"> 
</p>

A regular scatterplot modelled with a linear regression shows the general trend in duration of movies over time with a blue line indicating a increasingly negative relation between the variables. Setting the estimator parameter in seaborn's regplot to np.mean displays the estimate more clearly in vertical (aggregated) lines.

<img src="imgs\dur_reg_scatter.png" alt="dur_reg_scatter"> 

<img src="imgs\dur_mean.png" alt="dur_reg_mean"> 

Further specifying the `lowess` parameter in the linear regression model to `True` shows the locally weighed (lowess) stats. The minimal variation of the curve up until the 'downward slope' observed between 2010 and 2020 confirms a steady decrease of duration in the previous decades which seems to have accelerated for the last one.

<img src="imgs\dur_mean_lowess.png" alt="dur_mean_lowess"> 

So movies DO seem to be getting shorter in time but mostly in the past decade (2010-2020). To get an actual coefficient confirming this trend, the `LabelEncoder()` function from the `sklearn.preprocessing` package allows for variable normalizing. To evaluate correlation between duration and release year of movies, we first normalize the duration variable and then use `SciPy` functions `.fit()` and `transform()` functions which will fit the model and then transform the data accordingly to properly estimate the correlation using `.corr()`. This yields the following coefficient:
<p align="center">
<img src="imgs\corr_dur_year.png" alt="dur_year_corr"> 
</p>

This means that even though the models plotted above based on the whole cleaned data showed a trend of decreasing duration over time, the actual coefficent implies virtually no correlation between the year of release and the duration of the movie as the coefficient is lower than 0.25. A plot for correlation between these two variables