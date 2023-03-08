#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import os

# function to take a list of tickers and prepare a 5-year portfolio of price data
def port_prep(ticker_lst):
    # find dates for import: 5 years of price data
    today = datetime.today().strftime("%Y-%m-%d")
    five = (datetime.today() - relativedelta(years=5)).strftime("%Y-%m-%d")

    # remove any blank ticker positions at end of list
    while ticker_lst[-1] == "":
        ticker_lst.pop()

    # create class to convert string to object location name
    class classthing:
        def __init__(self, name):
            self.name = name

    # dictionary to hold ticker and pd.series object location name
    dct = {name: classthing(name) for name in ticker_lst}

    # get price data for tickers in list using yfinance where pd.series are memory location names
    for stk in ticker_lst:
        dct[stk] = yf.download(stk, start=five, end=today)["Adj Close"]

    # combine the four stocks into a single dataframe
    # axis =1 to show that the concatenation is to be done on columns not rows
    port = pd.concat([dct[x] for x in ticker_lst], axis=1)
    # ticker names to portfolio
    port.columns = ticker_lst

    return port


# function behind button displaying performance percentages
def chart_perf(ticker_lst):
    # prepare 5-year portfolio from ticker list
    port = port_prep(ticker_lst)

    ## RETURN GRAPHING SECTION
    # dataframe based on the stock prices to compute the daily returns.
    port_returns = port.pct_change(1).dropna()

    # now combining all four into one step
    cumul_return2 = 100 * ((1 + port_returns).cumprod() - 1)

    # display chart
    fig = plt.figure(figsize=(12, 6))
    plt.plot(cumul_return2)
    plt.ylabel("Returns")
    plt.xlabel("Date")
    plt.title("Individual Percent Returns")
    plt.legend(cumul_return2.columns)
    plt.show()


# function behind button to run monte carlo simulation - couldn't resist the name
def mc_hammer(ticker_lst):
    # remove any previous result set
    os.remove("mc.pickle")

    # prepare 5-year portfolio from ticker list
    port = port_prep(ticker_lst)

    # get the number of stocks in portfolio
    N = len(port.columns)

    # calculate the variables just to make this readable
    log_rets = np.log(port / port.shift(1))
    log_rets_cov = log_rets.cov()

    # function to generate random portfolio weights
    def gen_weights(N):
        weights = np.random.random(N)
        return weights / np.sum(weights)

    # function to calculate annualized portfolio return given weighting
    def calculate_returns(weights, log_rets):
        # annualize return
        return np.sum(log_rets.mean() * weights) * 252

    # function to calculate annual portfolio volatility given weighting
    def calculate_volatility(weights, log_rets_cov):
        annualized_cov = np.dot(log_rets.cov() * 252, weights)
        vol = np.dot(weights.transpose(), annualized_cov)
        return np.sqrt(vol)

    """
        # Monte Carlo Simulation
    """
    # lists to hold the results from the monte carlo simulation
    mc_weights = []
    mc_portfolio_returns = []
    mc_portfolio_vol = []

    # note that the number of stocks in the portfolio makes the length of
    # the simulation grow exponentially in complexity
    for sim in range(6000):

        weights = gen_weights(N)
        mc_weights.append(weights)
        sim_returns = calculate_returns(weights, log_rets)
        mc_portfolio_returns.append(sim_returns)
        sim_volatility = calculate_volatility(weights, log_rets_cov)
        mc_portfolio_vol.append(sim_volatility)

    # assume zero risk-free rate to calculate Sharpe ratio
    mc_sharpe_ratios = np.array(mc_portfolio_returns / np.array(mc_portfolio_vol))

    port_list = list(port.columns)

    # assemble dataframe of results
    df_weights = pd.DataFrame(np.row_stack(mc_weights))
    df_weights.columns = port_list

    df_portfolio_returns = pd.DataFrame(np.row_stack(mc_portfolio_returns))
    df_portfolio_returns.columns = ["Return"]

    df_portfolio_vol = pd.DataFrame(np.row_stack(mc_portfolio_vol))
    df_portfolio_vol.columns = ["Volatility"]

    df_portfolio_sharpe = pd.DataFrame(np.row_stack(mc_sharpe_ratios))
    df_portfolio_sharpe.columns = ["Sharpe"]

    df_portfolio_mc = pd.concat(
        [df_weights, df_portfolio_returns, df_portfolio_vol, df_portfolio_sharpe],
        axis=1,
    )

    # sort dataframe descending by Sharpe ratio
    mc_final = df_portfolio_mc.sort_values("Sharpe", ascending=False)

    mc_final.to_pickle("mc.pickle")


# function to read pickle from mc and display results in chart
def view_mc():
    mc_final = pd.read_pickle("mc.pickle")
    mc_portfolio_vol = mc_final["Volatility"].tolist()
    mc_portfolio_returns = mc_final["Return"].tolist()
    mc_sharpe_ratios = mc_final["Sharpe"].tolist()

    fig = plt.figure(figsize=(12, 6))
    plt.scatter(mc_portfolio_vol, mc_portfolio_returns, c=mc_sharpe_ratios)
    plt.colorbar(label="Sharpe Ratio")
    plt.xlabel("Volatility")
    plt.ylabel("Returns")
    plt.title("MC Simulation Results")
    plt.show()


# function to read pickle and return top 10
def view_tbl():
    mc_final = pd.read_pickle("mc.pickle")
    # df = mc_final.head(10)
    return mc_final.head(10)


# export top 10 to excel
def xls_export():
    mc_final = pd.read_pickle("mc.pickle")
    mc_final.to_excel("MCSimResults.xlsx")
