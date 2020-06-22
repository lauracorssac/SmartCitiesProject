(define (problem SecuritySystemProblem) (:domain SecuritySystemDomain)
(:objects 
buzzer-obj - buzzer
light-obj - light_bulb
bouglar - person
system-obj - system
time-obj - time
)

(:init
    ;(is-on-system system-obj)
    ;( = (time-passed time-obj) 10)
    {initial_state}
)

(:goal (and
    (is-recognized bouglar)
    (is-on buzzer-obj)
    (is-on light-obj)
))

(:goal (and
    (not (is-on-system system-obj))
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
