#!/usr/bin/env python3

import yfinance




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

    menu_itr = menu
    choice_path = ''
    while True: 
        for key in menu_itr:
            print('{}. {}\n'.format(key, menu_itr[key]['msg']))
        
        choice = input()
        if choice not in menu_itr:
            print('Invalid option. Choose again.')
            continue
        
        choice_path += choice

        if 'sub' in menu_itr[choice]:
            menu_itr = menu_itr[choice]['sub']
        else:
            return choice_path


def get_user_input():
    """
    Prompts the user to enter a stock name, a start and end dates.
    It then parses the input, and returns three strings:
        - The name of the selected stock
        - The start date of the desired time period
        - The end date of the desired time period
    
    Note: The dates are in the following format: dd/mm/yyyy
    """
    return None, None, None # todo


def display_available_stocks(companies):
    """
    Displays the list of companies that the user can choose from
    to read statistics about their stocks during a selected time period.

    @return - this function does not return a value
    """
    print('Available stocks:')
    for c in companies:
        print(c)


def display_stock_stats(company, start_date, end_date):
    """
    Displays statistics about the given `company` in the time period that is selected by the user.
    """
    pass


def main():
    companies = ['EBAY' , 'ecl', 'Eix', 'ew', 'ea']

    while True:
        choice = get_user_choice()
        print('User\'s choice: {}'.format(choice)) # todo: remove before submission

        if choice == 'b':
            break
        elif choice == 'aa':
            display_available_stocks(companies)
        elif choice == 'ab':
            company, start_date, end_date = get_user_input()
            if company not in companies:
                print('The selected company "{}" is not among the available stock symbols'.format(company))
                continue
            display_stock_stats(company, start_date, end_date)


if __name__ == '__main__':
    main()
