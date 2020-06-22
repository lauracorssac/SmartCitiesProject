import requests
import sys
import os
import json

class Solver(object):

    def __init__(self):
        return

    def request(self, new_buzzer_status):

        print("request function help ")
        dir_name = os.path.dirname(os.getcwd())
        print(dir_name)
        with open( dir_name + "/AI/domain.pddl", 'r') as domain_file, open( dir_name + "/AI/problem.pddl", 'r') as problem_file:
            print("opened")
            problem_string = problem_file.read()
            domain_string = domain_file.read()

            print("domain", domain_string)
            print("problem", problem_string)
            
            json = {
                'domain': domain_string,
                'problem': problem_string
                }

            response = requests.post("http://solver.planning.domains/solve", json= json).json()
            print("made request")
            return response

        