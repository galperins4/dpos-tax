import os
from configparser import ConfigParser
from datetime import datetime

from crypto.exceptions import ArkNetworkSettingsException

config_file = os.path.abspath('config.ini')

settings = ConfigParser()
settings.read(config_file)

network = {}


def use_network(network_name):
    """Select what network you want to use
    Args:
        network_name (str): name of a network, default ones are ARK's mainnet, kapu & persona
    """
    global network
    network = {
        'epoch': int(settings.get(network_name, 'epoch')),
        'database': settings.get(network_name, 'database')),
        'dbpassword': settings.get(network_name, 'dbpassword'),
    }


def get_network():
    """Get settings for a selected network
    Returns:
        dict: network settings
    """
    if not network:
        raise ArkNetworkSettingsException('Network has not been set')
    return network


def set_custom_network(epoch, database, dbpassword):
    """Set custom network
    Args:
        epoch (int): chains epoch time
        database (str): chains database
        database password (str): chains database password
    """
    section_name = 'custom'
    if section_name not in settings.sections():
        settings.add_section(section_name)
    settings.set(section_name, 'epoch', int(epoch))
    settings.set(section_name, 'database', str(database))
    settings.set(section_name, 'dbpassword', str(dbpassword)))