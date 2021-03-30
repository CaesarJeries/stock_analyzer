#!/usr/bin/env python3

import logging
import yfinance
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import statsmodels.api as sm



# define the back-end for matplotlib
matplotlib.use('GTK3Agg')



def get_choice_path(menu):
    """
    Prompts the user to make a choice out of the given `menu`.
    The structure of menu is as follows:
        {
            <choice-label>: {
                'msg': the message to display to the user
                'sub': (optional) a sub-menu. It follows the same structure rules
            },
            ...
        }
    
    @return - the choice path, i.e, the series of choices the user made until a concrete operation
              was reached.
    """
    menu_itr = menu
    choice_path = ''
    while True: 
        for key in menu_itr:
            print('{}. {}\n'.format(key, menu_itr[key]['msg']))
        
        choice = input()
        if choice not in menu_itr:
            print('Invalid option. Choose again: {}'.format('/'.join(menu_itr.keys())))
            continue
        
        choice_path += choice

        if 'sub' in menu_itr[choice]:
            menu_itr = menu_itr[choice]['sub']
        else:
            return choice_path


def get_user_choice():
    """
    Displays the menu, and prompts the user to enter their choice.

    @return - the user's "choice path": the series of choices the user made
              until an operation is chosen to be performed.
    """
    menu = {
        'a': {
            'msg': 'Display stock data',
            'sub': {
                'a': {
                    'msg': 'Display available stock symbols'
                },
                'b': {
                    'msg': 'Display statistics of a specific stock'
                }
            }
        },
        'b': {
            'msg': 'Exit'
        }
    }

    return get_choice_path(menu)


def get_user_input():
    """
    Prompts the user to enter a stock name, a start and end dates.
    It then parses the input, and returns three strings:
        - The name of the selected stock
        - The start date of the desired time period
        - The end date of the desired time period
    
    Note: The dates are in the following format: yyyy-mm-dd
    """
    stock = input('Enter desired stock: ')
    start_date = input('Enter start date (yyyy-mm-dd): ')
    end_date = input('Enter end date (yyyy-mm-dd): ')
    return stock, start_date, end_date


def display_available_stocks(companies):
    """
    Displays the list of companies that the user can choose from
    to read statistics about their stocks during a selected time period.

    @return - this function does not return a value
    """
    print('Available stocks:')
    print('\n'.join(companies))


def fetch_data(symbol, start_date, end_date):
    """
    Downloads and returns a dataframe that represents the history of the given
    stock `symbol` in the date range defined by `start_date` - `end_date` (inclusive)
    """
    logging.debug('Fetching info for stock {} from {} until {}'.format(symbol, start_date, end_date))
    
    interval = 'daily'
    if start_date == end_date:
        logging.debug('Using hourly interval')
        interval = 'hourly'
    
    data = yfinance.download(tickers=symbol, start=start_date, end=end_date, time_interval=interval)
    logging.debug(data)

    return data


def get_stats(arr):
    """
    Calculates and returns the following stats for the given numpy-like array `arr`:
        - Average
        - Standard deviation
        - Maximum
        - Minimum
    
    @return - a tuple containing the metrics above, in the specified order (left-to-right)
    """
    average = arr.mean()
    std_dev = arr.std()
    maximum = arr.max()
    minimum = arr.min()

    return (average, std_dev, maximum, minimum)


def display_closing_summary(data, symbol):
    """
    data - A pandas DataFrame as returned from yfinance.
           It contains the following columns: Open | High | Low | Close | Adj Close | Volume
    
    This function displays the following information about the adjusted closing rate:
        - Average
        - Standard deviation
        - Maximum
        - Minimum
    """
    adjusted_closing_rates = data['Adj Close'].to_numpy()
    stats = get_stats(adjusted_closing_rates)

    print('{}: Statistics of the stock\'s closing rate:'.format(symbol))
    print('Average: {}\nStandard Deviation: {}\nMaximum: {}\nMinimum: {}'.format(*stats))


def display_daily_yield_stats(data, symbol):
    """
    data - A pandas DataFrame as returned from yfinance.
           It contains the following columns: Open | High | Low | Close | Adj Close | Volume
    
    This function displays the following information about the daily yield:
        - Average
        - Standard deviation
        - Maximum
        - Minimum
    """
    daily_yields =  data['Adj Close'].pct_change()[1:]
    logging.debug(daily_yields)
    stats = get_stats(daily_yields)

    print('{}: Statistics of the stock\'s daily yields:'.format(symbol))
    print('Average: {}\nStandard Deviation: {}\nMaximum: {}\nMinimum: {}'.format(*stats))


def calculate_sharpe_metric(data, symbol):
    """
    Calculates and displays Sharpe metric according to the following formula:
        S = r / d
        Where r is the average of daily returns, and d is the standard deviation of the daily returns
    
    @return - S, the Sharpe metric 
    """
    daily_yields =  data['Adj Close'].pct_change()[1:]
    average, std_dev, _, _ = get_stats(daily_yields)
    s = average / std_dev

    print('{}: Sharpe metric: {}'.format(symbol, s))
    return s


def plot_exchange_rates(data, symbol):
    """
    Plots the opening and the adjusted closing rates of the given stock.
    The stock rates are represented in the dataframe `data` (as returned from yfinance.download)
    """
    logging.debug('Plotting exchange rate for {}'.format(symbol))
    plt.figure(figsize=(15, 10))
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    plt.plot(data['Adj Close'], linewidth=2, color='blue', label='Adjusted Closing Rates')
    plt.plot(data['Open'], linewidth=2, color='silver', label='Opening Rates')
    plt.xlabel('Date', fontsize=13)
    plt.legend()
    plt.title('The exchange rates for {}'.format(symbol))
    plt.show()


def plot_daily_yields(data, symbol):
    """
    Plots the daily yields (returns) of the given stock.
    The stock rates are represented in the dataframe `data` (as returned from yfinance.download)
    """
    logging.debug('Plotting daily yields for {}'.format(symbol))
    plt.figure(figsize=(15, 10))
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)

    yields = data['Adj Close'].pct_change()[1:]
    plt.plot(yields, linewidth=2, color='black')
    
    plt.xlabel('Date', fontsize=13)
    plt.ylabel('Daily Yields', fontsize=13)
    plt.title('Daily yields of {}'.format(symbol))
    plt.show()


def plot_exchange_rates_hist(data, symbol):
    """
    Plots a histogram of the closing adjusted closing rates of the given stock.
    The stock rates are represented in the dataframe `data` (as returned from yfinance.download)
    """
    logging.debug('Plotting a histogram of exchange rates of {}'.format(symbol))
    plt.figure(figsize=(15, 10))
    plt.title('A histogram of exchange rates of {}'.format(symbol))
    plt.hist(data['Adj Close'])
    plt.show()


def plot_daily_yields_hist(data, symbol):
    """
    Plots a histogram of the daily returns (yields) of the given stock.
    The stock rates are represented in the dataframe `data` (as returned from yfinance.download)
    """
    logging.debug('Plotting a histogram of daily yields of {}'.format(symbol))
    plt.figure(figsize=(15, 10))
    plt.title('A histogram of the daily yields of {}'.format(symbol))
    yields = data['Adj Close'].pct_change()[1:]
    plt.hist(yields)
    plt.show()


def calculate_alpha_beta(data, symbol, start_date, end_date):
    """
    Calculates Jensen's alpha and beta coefficients.
    The regression is done against the S&P500 stock in the date range `start_date` - `end_date` (inclusive)

    @return - a tuple: (alpha, beta)
    """
    logging.debug('Calculating alpha of {}'.format(symbol))

    benchmark_data = fetch_data('SPY', start_date, end_date)
    benchmark_returns = benchmark_data['Adj Close'].pct_change()

    X = benchmark_returns[1:]
    X = sm.add_constant(X)
    
    Y = data['Adj Close'].pct_change()[1:]
    
    model = sm.OLS(Y, X).fit()
    coeff = model.params

    logging.debug('α = {}, β = {}'.format(*coeff))

    return coeff


def analyze_stock(symbol, start_date, end_date):
    """
    Displays a list of available analysis options, and prompts the user for a choice.
    On choice, the corresponding analysis is run and results are displayed to the user.
    This function does not return a value.
    """
    menu = {
        'a': {
            'msg': 'Display statistics of the adjusted closing rate (Average / Standard Deviation / Maximum / Minimum)'
        },
        'b': {
            'msg': 'Display statistics of the daily yield of the adjusted closing rate (Average / Standard Deviation / Maximum / Minimum)'
        },
        'c': {
            'msg': 'Calculate the Sharpe metric'
        },
        'd': {
            'msg': 'Plot a graph of the stock\'s exchange rates'
        },
        'e': {
            'msg': 'Plot a graph of the daily yields' 
        },
        'f': {
            'msg': 'Plot a histogram of the stock\'s exchange rates'
        },
        'g': {
            'msg': 'Plot a histogram of the daily yields' 
        },
        'h': {
            'msg': 'End analysis' 
        },
        'i': {
            'msg': 'Calculate α' 
        },
        'j': {
            'msg': 'Calculate β'
        }
    }

    choice = get_choice_path(menu)
    
    handlers = {
        'a': display_closing_summary,
        'b': display_daily_yield_stats,
        'c': calculate_sharpe_metric,
        'd': plot_exchange_rates,
        'e': plot_daily_yields,
        'f': plot_exchange_rates_hist,
        'g': plot_daily_yields_hist
    }

    data = fetch_data(symbol, start_date, end_date)
    if choice in handlers:
        handlers[choice](data, symbol)
    elif choice == 'i' or choice == 'j':
        alpha, beta = calculate_alpha_beta(data, symbol, start_date, end_date)

        if (choice == 'i'):
            print('The alpha of {} is {}'.format(symbol, alpha))
        else:
            print('The beta of {} is {}'.format(symbol, beta))


def main():
    symbols = ['EBAY' , 'ecl', 'Eix', 'ew', 'ea']

    while True:
        choice = get_user_choice()
        logging.debug('User\'s choice: {}'.format(choice))

        if choice == 'b':
            break
        elif choice == 'aa':
            display_available_stocks(symbols)
        elif choice == 'ab':
            symbol, start_date, end_date = get_user_input()
            if symbol not in symbols:
                print('The selected company "{}" is not among the available stock symbols'.format(symbol))
                continue
            analyze_stock(symbol, start_date, end_date)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(funcName)s:%(lineno)d] %(message)s')
    main()
