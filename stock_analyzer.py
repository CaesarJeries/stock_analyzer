#!/usr/bin/env python3

import yfinance

# todo
def get_user_choice():
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


def main():
    companies = ['EBAY' , 'ecl', 'Eix', 'ew', 'ea']

    while True:
        choice = get_user_choice()
        print('User\'s choice: {}'.format(choice))

        company = 'ea' # todo: get user input
        if company not in companies:
            print('The selected company "{}" is not among the available stock symbols'.format(company))
            continue



if __name__ == '__main__':
    main()
