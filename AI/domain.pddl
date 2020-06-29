;Header and description

(define (domain SecuritySystemDomain)

(:requirements :strips :fluents :typing :negative-preconditions)

(:types 
person time - object
buzzer light_bulb program - system_component
)

;(:constants )

(:predicates
(is-recognized ?p - person )
(is-on ?s - system_component)
)

(:functions
    (time-passed ?v - time)
)

(:action turn-system-component-on
    :parameters (?person - person ?sc - system_component)
    :precondition (is-recognized ?person)
    :effect ( is-on ?sc )
)





(:action turn-system-component-off
    :parameters (?time - time ?sc - system_component )
    :precondition (and ( > (time-passed ?time) 30) (is-on ?sc) )
    :effect (not ( is-on ?sc ))
)

)