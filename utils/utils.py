import os

import betfairutil
from alive_progress import alive_it


def get_bet_names_from_event_folder(event_path):
    """
    This function iterates over all the files in a specified directory and extracts the event names from '.bz2' files
    which contain market books. It returns a dictionary mapping the file names to their respective event names.
    Note: this function is meant to be used on a folder that contains price files of one event (match), to extract the different
    types of bets (match odds, set betting, ...).

    Args:
        event_path (str): The path of the directory which contains the '.bz2' files.

    Returns:
        dict: A dictionary mapping file names to their respective event names.

    Example:

        event_path = 'path/to/your/event/32060431'
        event_names = get_event_names_in_folder(event_path)
        ## OUTPUT
        ## event_names = {'1.209205397.bz2': 'Set Betting',
                        '1.209205398.bz2': 'Set 1 - Correct Score',
                        '1.209205399.bz2': 'Tsitsipas To Win A Set?',
                        '1.209205400.bz2': 'Djokovic To Win A Set?',
                        '1.209205401.bz2': 'Handicap',
                        '1.209205438.bz2': 'Total Games',
                        '1.209205486.bz2': 'Number of Sets?',
                        '1.209205488.bz2': 'Match Odds'}
    """
    dir_names = {}
    for file in alive_it(os.listdir(event_path)):
        if ".bz2" in file:
            market_books = betfairutil.read_prices_file(os.path.join(event_path, file))
            dir_names[file] = market_books[0]['marketDefinition']["name"]

    return dir_names


def get_bet_names_for_each_event(events_folder):
    """
    This function recursively searches through a directory and its subdirectories for '.bz2' files. For each '.bz2' file,
    it extracts the market books and retrieves the 'event' and 'name' properties. It maps the events to a list of
    associated names (bets) and stores this in a dictionary.
    Note: this function is meant to be used on a folder that contains folders of events (matches) (like folder Jan/Day_number), to
    extract for each event all the different bets (match odds, set bettig, ...).

    Args:
        events_folder (str): The root directory containing the '.bz2' files.

    Returns:
        dict: A dictionary mapping events to a list of associated names (bets).

    Example:

        events_folder = 'path/to/your/events/Jan/1'
        bets_for_each_event = get_bets_for_each_event(events_folder)
        ## OUTPUT
        ## bets_for_each_event = {'A Isaacs @ E Khayrutdinova': ['Match Odds'],
                        'A Kalinina v A Bondar': ['Match Odds'],
                        'A Muller v Bra Holt': ['Match Odds'],
                        'A Potapova v L Noskova': ['Match Odds'],
                        'A Sinha @ T Cardona': ['Match Odds'],
                        'A Zhu @ V Bervid': ['Match Odds'],
                        'Ada Taylor v Mott': ['Match Odds'],

    """
    dict_names_and_events = {}
    for root, _, files in alive_it(list(os.walk(events_folder))):
        #print(root)
        for file in files:
            if ".bz2" in file:
                market_books = betfairutil.read_prices_file(os.path.join(root, file))
                event = market_books[0]['marketDefinition']['eventName']
                name = market_books[0]['marketDefinition']['name']

                if event in dict_names_and_events:
                    dict_names_and_events[event].append(name)
                else:
                    dict_names_and_events[event] = [name]

    return dict_names_and_events