import requests
import sys
import os
import json

class Solver(object):

    def __init__(self):
        return

    def request(self, new_person_status, time_measured):

        print("request function help ")
        dir_name = os.path.dirname(os.getcwd())
        print(dir_name)
        with open( dir_name + "/AI/domain.pddl", 'r') as domain_file, open( dir_name + "/AI/problem.pddl", 'r') as problem_file:
            print("opened")

            domain_string = domain_file.read()
            initial_state_stirng = ""
            if new_person_status == 1.0:
                initial_state_stirng += "(is-recognized bouglar)"
                initial_state_stirng += "\n"
            
            initial_state_stirng += "( = (time-passed time-obj) %d)" % time_measured 
            problem_string = problem_file.read().format(initial_state= initial_state_stirng)
            print("problem", problem_string)
            
            json = {
                'domain': domain_string,
                'problem': problem_string
                }

            response = requests.post("http://solver.planning.domains/solve", json= json).json()
            print("made request")
            return response
        