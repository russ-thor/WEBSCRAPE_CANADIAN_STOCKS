#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Russ T
# Created: August 2021
# See READ_ME.doc in repository

# Imports
import os
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup as soup
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import ezgmail

# Data/variables
# To see nicely formatted HTML, use: https://beautifier.io/
today = datetime.date.today()
current_time = datetime.datetime.now().time()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.15'
                  '9 Safari/537.36'
}
yahoo_url = 'https://ca.finance.yahoo.com/quote/'

# ********** You need to select your stocks, create a figure title, and update lists ***********************************
figure_title = "Lumber Stock Price and Analyst Rating"
stock1 = 'IFP'
stock2 = 'CFP'
stock3 = 'WFG'
stocks_to_analyze = [stock1, stock2, stock3]
email_contact = 'russell.thorsteinsson@gmail.com'
# **********************************************************************************************************************


# With BeautifulSoup and requests, scrape current stock data from Yahoo for stock symbols. Write this data to a csv file


def get_stock_metrics(stock):

    # request stock url from Yahoo; format with BeautifulSoup
    req = requests.get(yahoo_url + stock + '.TO', headers=headers)
    print('processing:', stock, ', Authentication:', req.status_code)  # 200 means request successful
    page_soup = soup(req.text, 'html.parser')

    # stock metrics
    open_price = page_soup.find('td', {'class': "Ta(end) Fw(600) Lh(14px)"}).find_all('span')[0].text
    close_price = page_soup.find('div', {'class': "D(ib) Mend(20px)"}).find_all('span')[0].text
    one_year_target_price = (
        page_soup.find(
            'div',
            {
                'class': "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos"
                "(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0p"
                "x) smartphone_BdB smartphone_Bdc($seperatorColor)"
            },
        )
        .find('t' 'r', {'class': "Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorCol" "or) H(36px) Bdbw(0)!"})
        .find_all('span')[1]
        .text
    )
    day_change_percent = page_soup.find('div', {'class': "D(ib) Mend(20px)"}).find_all('span')[1].text
    PE_ratio = (
        page_soup.find(
            'div',
            {
                'class': "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos"
                "(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0p"
                "x) smartphone_BdB smartphone_Bdc($seperatorColor)"
                ""
            },
        )
        .find_all('td')[5]
        .text
    )

    # check if CSV exists (if not, write csv headers); append metrics to each stocks csv
    CSV_exists = os.path.exists(f'stock_{stock}.csv')
    with open(f'stock_{stock}.csv', 'a') as fileObj:

        if not CSV_exists:  # writes headers if csv was just created
            fileObj.write("Date,Time,Open_Price,Close_Price,One_Year_Target_Price,PE_Ratio,Day_Change\n")

        # Print the stock metrics that were scraped and write them to the csv
        print(
            str(today),
            '|',
            str(current_time),
            '|',
            open_price,
            '|',
            close_price,
            '|',
            one_year_target_price,
            '|',
            PE_ratio,
            '|',
            day_change_percent,
        )

        fileObj.write(
            str(today)
            + ","
            + str(current_time)
            + ","
            + open_price
            + ','
            + close_price
            + ','
            + one_year_target_price
            + ','
            + PE_ratio
            + ','
            + day_change_percent
            + "\n"
        )


# With Plotly, plot multiplot time series of stock metrics - save and email static + dynamic graphs


def plot_stock_metrics(stock_list):
    number_stocks = len(stock_list)

    # Make plotly subplot figure
    fig = make_subplots(
        rows=number_stocks,
        cols=1,
        subplot_titles=("X" * number_stocks),  # create temp subplot titles that are updated below
        shared_xaxes=True,
        vertical_spacing=0.07,
    )

    # Add scatter plot lines to each subplots (Open Price, Close Price, Analyst Rating)
    row_num = 0
    for i in stock_list:
        row_num += 1
        df = pd.read_csv(f'stock_{i}.csv')

        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Open_Price'], name=f'{i} Open Price', line=dict(color='#6d95d6')),
            row=row_num,
            col=1,
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Close_Price'], name=f'{i} Close Price', line=dict(color='#284575')),
            row=row_num,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df['Date'], y=df['One_Year_Target_Price'], name=f'{i} Analyst Target', line=dict(color='#e3b240')
            ),
            row=row_num,
            col=1,
        )

    # Add x-y axis labels and title to figure, save and email graphs
    fig.update_xaxes(title_text="Date", row=row_num, col=1)  # row_num sets label below last subplot
    fig.update_yaxes(title_text="Price (CDN)", row=int(row_num / 2), col=1)  # row_num sets label ~ halfway on y-axis
    fig.update_layout(
        height=600,
        width=600,
        title={'text': figure_title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
    )

    # Update temporary subplot titles with stock symbol
    for i, name in enumerate(stock_list):
        fig.layout.annotations[i].update(text=name)
        i += 1

    # Display final figure
    fig.show()

    # Save figures, email them to contact specified
    static_graph = 'stockGraphs\\' + f'Lumber_Stock_Prices_{str(datetime.date.today())}.png'
    dynamic_graph = 'stockGraphs\\' + f'Lumber_Stock_Prices_{str(datetime.date.today())}.html'
    fig.write_html(dynamic_graph)
    fig.write_image(static_graph)

    # Email static and dynamic files
    ezgmail.send(
        email_contact,
        f'Lumber Stocks {str(datetime.date.today())}',
        f'Here are the lumbbrer stock prices for {str(datetime.date.today())}',
        [static_graph, dynamic_graph],
    )


for i in stocks_to_analyze:
    get_stock_metrics(i)

plot_stock_metrics(stocks_to_analyze)
