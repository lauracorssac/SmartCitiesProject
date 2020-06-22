;Header and description

(define (domain SecuritySystemDomain)

(:requirements :strips :fluents :typing :negative-preconditions)

(:types 
person - object
buzzer light_bulb - actuator 
)

;(:constants )

(:predicates
(is-recognized ?p - person )
(is-on ?a - actuator)
)


(:action turn-actuator-on
    :parameters (?p - person ?a - actuator)
    :precondition (and (is-recognized ?p) (not (is-on ?a) ) )
    :effect ( is-on ?a )
)

)