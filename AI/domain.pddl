;Header and description

(define (domain SecuritySystemDomain)

(:requirements :strips :fluents :typing :negative-preconditions)

(:types 
person system - object
buzzer light_bulb - actuator 
time
)

;(:constants )

(:predicates
(is-recognized ?p - person )
(is-on ?a - actuator)
(is-on-system ?s - system)
)

(:functions
    (time-passed ?v - time)
)


(:action turn-actuator-on
    :parameters (?p - person ?a - actuator)
    :precondition (and (is-recognized ?p) (not (is-on ?a) ) )
    :effect ( is-on ?a )
)

(:action turn-system-off
    :parameters (?v - time ?s - system)
    :precondition ( = (time-passed ?v) 10)
    :effect (not ( is-on-system ?s ))

)

)