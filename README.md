# DA_stats
This project provides a more detailed analysis of hte netflix db for movies up until 2022. It includes hypotheses about the possible reasons for the distribution of duration and release date for movies observed in the initial visualization of data and basic analyses can be found here, in a different project.


In the code folder, two files contain the code for the duration and genre stats, respectively and an img folder contains the different plots generated with the newly wrangled data, based on the cleaned, cropped and selected data following criteria aimed at proper hypothesis testing.


In both cases, the necesssary packages are imported, data is read into a df, which is immediately filtered to only display movie-related data. Columns of interest are selected and filtering for specific duration and genre is done with the same criteria as shown in the initial visualization project (REF), i.e. to discard outliers and uncategorized or inexistent genres. Based on observations from the first project, the data is further filtered to only include rows for movies released between 1970 and 2020.

Next, null and NaN elements are filtered out in two short steps. First, via a simple nested loop, null elements are tracked along each column and rows containing null elements are dropped. Then, using ((missingno package)), the cleaned df is further scanned for other NaNs.

<img src="imgs\na_values.png" alt="na_values" width="377" align-items="center">

After checking categorical variable consistency (for 'genre') a histogram is plotted to get a picture of the general distribution of 'duration' for different release years.

<img src="imgs\clean_dy.png" alt="clean_dy">

Rows for movies of genres 'independent', 'international', 'classic' and 'cult' movies were removed after identifying the specific indeces via a nested conditional in a for loop. The cleaned df was plotted in a new instagram using a gradient palette to better show data density for different years. 

A scatterplot including genre as hue gives a clue to whether genres relate to duration

<img src="imgs\year_duration_hist.png" alt="yd_hist">

Variable correlation