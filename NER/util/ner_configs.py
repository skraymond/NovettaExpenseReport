# This file holds user and application level configs
import logging

logging.basicConfig(format='%(asctime)s %(levelname)3s %(module)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


southwest_config = {
    'rapid_reward_number': '123456789'
}

person_config = {
    'name': 'Test T. User',
    'username': 'tuser',
    'home_address': '123 Sesame Street',
    'employee_number': '444112',
    'employee_approver': 'Big Bird'
}

