from datetime import datetime, timedelta


def is_action_recent(timestamp, days=0, minutes=0):
    """
    This method compares a timestamp to the actual date.
    :param timestamp: A string in the format "%Y-%m-%d %H:%M:%S".
    :param days: An integer indicating the number of days defining when an action is recent.
    :param minutes: An integer indicating the number of minutes defining when an action is recent.
    :return: True is the timestamp inserted is a date that happened recently, False otherwise.
    """
    t1 = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.now()

    difference = t2 - t1

    recent = difference < timedelta(days=days, minutes=minutes)
    return recent


def update_cursor_index(action, old_idx, step, size):
    """
    This method takes an index as an input, and returns an updated index which value depends on the other parameters.
    :param action: "none", "next" or "previous".
    :param old_idx: An integer representing the old index to modify.
    :param step: An integer representing the variation of the index.
    :param size: An integer representing the size of the element related to the index.
    :return: An integer representing the new index.
    """
    if action == "next":
        new_idx = old_idx + step if (old_idx + step) < size else 0
    elif action == "previous":
        new_idx = old_idx - step if (old_idx - step) > 0 else 0
    else:
        new_idx = old_idx
    return new_idx


def show_element(strings, idx_start, num_choices):
    # Get the indexes of the options to be shown to the user
    if idx_start >= len(strings):
        idx_start = 0
    idx_end = idx_start + num_choices

    strings = strings[idx_start:idx_end]

    # Format of display -> option n: text
    #                      option n+1: text
    num_1 = min(idx_start + num_choices, len(strings))
    num_2 = len(strings)
    text_response = f"{num_choices} of {num_2} items found are: \n"
    for i, string in enumerate(strings, start=1):
        text_response += f"{idx_start + i}: {string}. \n"

    return text_response
