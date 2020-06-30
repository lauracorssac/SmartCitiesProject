;Header and description

(define (domain DOMAINA)

;remove requirements that are not needed
(:requirements :strips :fluents :typing :conditional-effects :negative-preconditions :equality)

(:types
    person time - object
    buzzer light - actuator
    algorithm - component
    actuator - component
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (is-on ?c - component)
    (is-recognized ?p - person)
    (has-waited ?time - time)
)


;define actions here

(:action turn-component-on
    :parameters (?c - component ?p - person ?t - time)
    :precondition (and (not (is-on ?c)) (is-recognized ?p) (not (has-waited ?t)) )
    :effect (and (is-on ?c))
)

(:action turn-algorithm-off
    :parameters (?alg - algorithm ?time - time ?light - light ?buzz - buzzer)
    :precondition (and (is-on ?alg) (has-waited ?time) (not (is-on ?light)) (not (is-on ?buzz) ) )
    :effect (and (not (is-on ?alg)))
)

(:action turn-actuator-off
    :parameters (?act - actuator ?time - time)
    :precondition (and (is-on ?act) (has-waited ?time) )
    :effect (and (not (is-on ?act)))
)

(:action wait-for-while
    :parameters ( ?person - person ?buzz - buzzer ?light - light ?time - time)
    :precondition (and
       (not (has-waited ?time))
       (is-recognized ?person)
       (is-on ?buzz)
       (is-on ?light)
    )
    :effect (and 
    (has-waited ?time)
    )
)


(:action wait-for-person
    :parameters (?person - person)
    :precondition (and (not (is-recognized ?person)))
    :effect (and (is-recognized ?person))
)




)