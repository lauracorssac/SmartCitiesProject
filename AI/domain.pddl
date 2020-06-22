;Header and description

(define (domain SecuritySystemDomain)

(:requirements :strips :fluents :typing :negative-preconditions)

(:types 
person buzzer
)

;(:constants )

(:predicates
(is-recognized ?p - person )
(is-on ?b - buzzer)
)


(:action turn-buzzer-on
    :parameters (?p - person ?b - buzzer)
    :precondition (and (is-recognized ?p) (not (is-on ?b) ) )
    :effect ( is-on ?b )
)
)