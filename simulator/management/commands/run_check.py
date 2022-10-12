from django.core.management.base import BaseCommand
from simulator.connectors.requester import CaseRequests
"""
Дергает запущенный локально бэкенд, который обращается к локальной заглушке
"""


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('cases', nargs='*', type=int, default=[])
        parser.add_argument('--debug', nargs='?', const=True, default=False)

    def handle(self, *args, **options):
        cases = options['cases']
        debug = options['debug']
        if debug:
            print("---> DEBUG MODE")
            print(">> CASE: ", cases)
        CaseRequests(debug=debug).run_tests(cases)
