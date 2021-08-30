# webscrape_canadian_stocks.py
- !/usr/bin/env python3
- -*- coding: utf-8 -*-
- Modules required: os, datetime, requests, pandas, bs4 (BeautifulSoup), plotly, ezgmail
- Author: Russ T
- Created: August 2021

# description 
This script was created to scrape Canadian stock metrics from https://ca.finance.yahoo.com/ (ticker must end with '.TO' - although you can easily this part of the script). Furthermore, a figure containing subplot graphs will be produced for each stock ticker and the static (jpg) and dynamic (html) results will be saved and emailed to the specificed contact(s) in the script. Ideally, you set up a scheduled task that runs the script Mon-Fri to continue the stock data collection - set this to run after market hours to ensure the close price is correct (there is no close price to scrape, just the current price which fluctuates during market hours). The figure/subplots will not be very insightful until data has been collected for at least a few days (limited data to start off).

# installation
- pip install bs4
- pip install plotly==5.2.1
- pip install ezgmail (setup credentials/tokens: https://pypi.org/project/EZGmail/)
- pip install pandas
- pip install plotly
- pip install plotly==5.2.1

# required inputs
Before running the scripts you must update (starting on line 28):
- the stock tickers you want to scrape
- the title of the figure that will be built with plotly
- the email contact you want the resulting graphs sent to.

# function descriptions
The get_stock_metrics function will:
- use the requests and bs4 modules to scrape the stock data for the list of symbols you input (open price, close price, analyst target rating, PE ration, daily change' (currently only plotting the open, close, and analyst rating)
- checks if an existing csv exists for each one of the stocks specified in your list. If not, it creates a csv and adds the appropriate stock metric headers
- appends the current days scraped metrics to the csv

The plot_stock_metrics function will:
- read in a pandas dataframe for each stock and create a figure from the dataframe with the plotly module
- iterate through each stock, and add scatter plot lines to each subplot for the open price, close price, and analyst rating
- create and save a static (jpg) figure and a dynamic (html) figure to your working directory
- using the ezgmail module, email the jpg and html link to the contact specified.

# example graph output (interactive html version is emailed)
![Lumber_Stock_Prices_2021-08-29](https://user-images.githubusercontent.com/87350911/131263806-aaaeb4b7-0eba-4448-bb4e-98cce8633daa.png)
