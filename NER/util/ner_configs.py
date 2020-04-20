# This file holds user and application level configs
import logging

logging.basicConfig(format='%(asctime)s %(levelname)3s %(module)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


southwest_config = {
    'rapid_reward_number': '405696734'
}

person_config = {
    'name': 'Spencer K. Raymond',
    'username': 'sraymond',
    'home_address': '2004 C Street NE Washington DC',
    'employee_number': '100407',
    'employee_approver': 'Caleb DeGroote'
}

