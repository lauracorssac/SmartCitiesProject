(define (problem PROBLEMAA)

(:domain DOMAINA)
(:objects 
	buzzerObj - buzzer
	lightObj - light
    bouglar - person
    algorithmObj - algorithm
    timeObj - time

)

(:init 
	;(is-recognized bouglar)
    (is-on algorithmObj)
    ;(is-on buzzerObj)
    ;(is-on lightObj)
    ;(has-waited timeObj)
)

; (:goal (and
;     (is-on lightObj)
;     (is-on buzzerObj)
;     (is-on algorithmObj)
;     (is-recognized bouglar)
;     ( = (time-passed timeObj) 0)
; ))

(:goal (and
    (not (is-on lightObj))
    (not (is-on buzzerObj))
    (not (is-on algorithmObj))
    (is-recognized bouglar)
    (has-waited timeObj)
))

)