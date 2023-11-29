# 10-sqlalchelmy-challenge

Yay! I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decide to do a climate analysis about the area.

With this climate analysis I have utilized Python and SQLAlchemy to do a basic climate analysis and data exploration of my climate database.  Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib.

Two analysis's were created, precipitation and station.  Each query utilized the previous 12 months of data, then converted the results to a dataframe.  In a few cases the station and measurement tables needed to be joined for queries.  With this dataframe I was able to them create a plot to show a visualization of the results.  

Next, when the initial analysis was completed, I designed a Flask API based on the queries developed.  The Flask API's consist of a starting homepage listing all of the available API's in JSON format. The API's are as follows; precipitation, stations, temperature observations (tobs), start (allows you to pick any single date for min, max and avg results), start/end (allows you to choose a range of dates for min, max, and avg results).

