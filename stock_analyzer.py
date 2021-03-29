#!/usr/bin/env python3

import logging
import yfinance
import numpy as np
from matplotlib import pyplot as plt


def get_choice_path(menu):
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
    end_date = input('Enter start date (yyyy-mm-dd): ')
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
    logging.debug('Fetching info for stock {} from {} until {}'.format(symbol, start_date, end_date))
    data = yfinance.download(tickers=symbol, start=start_date, end=end_date, time_interval='daily')
    logging.debug(data)

    return data


def get_stats(arr):
    average = arr.mean()
    std_dev = arr.std()
    maximum = arr.max()
    minimum = arr.min()

    return (average, std_dev, maximum, minimum)


def display_closing_summary(data):
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

    print('Average: {}\nStandard Deviation: {}\nMaximum: {}\nMinimum: {}'.format(*stats))


def display_daily_yield_stats(data):
    """
    data - A pandas DataFrame as returned from yfinance.
           It contains the following columns: Open | High | Low | Close | Adj Close | Volume
    
    This function displays the following information about the daily yield:
        - Average
        - Standard deviation
        - Maximum
        - Minimum
    """
    daily_yield =  1 - data['Adj Close'].to_numpy() / data['Open'].to_numpy()
    logging.debug(daily_yield)
    stats = get_stats(daily_yield)
    print('Average: {}\nStandard Deviation: {}\nMaximum: {}\nMinimum: {}'.format(*stats))


def display_stock_stats(symbol, start_date, end_date):
    """
    Displays statistics about the given `symbol` in the time period that is selected by the user.
    """
    data = fetch_data(symbol, start_date, end_date)

    print('\nPrinting stats for: Symbol: {}. Range: {} - {}'.format(symbol, start_date, end_date))
    print('\nAdjusted Closing Rates:')
    display_closing_summary(data)
    print('\nDaily Yield:')
    display_daily_yield_stats(data)


def analyze_stock(symbol, start_date, end_date):
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

    return choice # todo: handle choices


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
