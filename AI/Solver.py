import requests

class Solver(object):

    def __init__(self):
        return

    def request(self, new_buzzer_status):

        json = {
            'domain': open("domain.pddl", 'r').read(),
            'problem': open("problem.pddl", "r").read()
        }

        return requests.post("http://solver.planning.domains/solve", json= json)

        