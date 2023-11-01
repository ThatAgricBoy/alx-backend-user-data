#!/usr/bin/env python3
"""
redaction of a log message
"""

import re

def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in a log message.

    Args:
    fields (List[str]): List of strings representing fields to obfuscate.
    redaction (str): The string used for obfuscation.
    message (str): The log line message.
    separator (str): The character separating fields in the log message.

    Returns:
    str: The obfuscated log message.
    """
    pattern = re.compile(rf'(?<=^|{re.escape(separator)})([^{re.escape(separator)}]+)(?={re.escape(separator)}|$)')
    return re.sub(rf'(?<=^|{re.escape(separator)})({"|".join(fields)})(?={re.escape(separator)}|$)', redaction, message)

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))
