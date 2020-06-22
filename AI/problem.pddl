(define (problem SecuritySystemProblem) (:domain SecuritySystemDomain)
(:objects 
buzzer-obj - buzzer
light-obj - light_bulb
bouglar - person
)

(:init
    (is-recognized bouglar)
)

(:goal (and
    (is-recognized bouglar)
    (is-on buzzer-obj)
    (is-on light-obj)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
