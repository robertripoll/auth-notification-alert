"""
This module contains the AuditD parser class.

The AuditD parser class is a concrete implementation of the Parser abstract base class.
It uses the AuditdEventParser class from the auditd_tools module to parse the input
line and extract the user and IP address.
"""

# pylint: disable=W4901
from parser.base import Login, Parser
from auditd_tools.event_parser import AuditdEventParser


# pylint: disable=R0903
class AuditD(Parser):
    """
    A concrete implementation of the Parser abstract base class.

    It uses the AuditdEventParser class from the auditd_tools module to parse the
    input line and extract the user and IP address.

    Attributes:
        parser (AuditdEventParser): An instance of the AuditdEventParser class used
            to parse the input line.

    Methods:
        parse (str) -> Login | None: This method takes a line of input and returns
            a Login object if a login event is found, otherwise it returns None.
    """

    def __init__(self):
        self.parser = AuditdEventParser()

    def parse(self, line: str) -> Login | None:
        for event in self.parser.parseline(line):
            if event['action'] != 'logged-in':
                continue

            for record in event['records']:
                if record['res'] != 'success':
                    continue

                if record['addr'] == '':
                    continue

                user = record['id']
                ip = record['addr']

                return Login(user, ip)

        return None
