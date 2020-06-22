(define (problem SecuritySystemProblem) (:domain SecuritySystemDomain)
(:objects 
buzzer-obj - buzzer
bouglar - person
)

(:init
    (is-recognized bouglar)
)

(:goal (and
    (is-recognized bouglar)
    (is-on buzzer-obj)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
