(define (problem SecuritySystemProblem) 
(:domain SecuritySystemDomain)
(:objects 
buzzer-obj - buzzer
light-obj - light_bulb
bouglar - person
program-obj - program
time-obj - time
)

(:init
    ;(is-on program-obj)
    (is-recognized bouglar)
   ; ( = (time-passed time-obj) 0)
    ;(not (is-on buzzer-obj))
    ;{initial_state}
)

; (:goal (and
;     (is-on program-obj)
;     (not (is-recognized bouglar))
;     (not (is-on buzzer-obj))
;     (not (is-on light-obj))
;     ( = (time-passed time-obj) 0)
; ))







(:goal (and
    (is-on buzzer-obj)
    (is-on light-obj)
    ;(is-on program-obj)
    ;(is-recognized bouglar)
    ;( < (time-passed time-obj) 30)
))
; (:goal (and
;     (not (is-on program-obj) )
;     (not (is-on buzzer-obj))
;     (not (is-on light-obj))
;     ( > (time-passed time-obj) 30)
;     (is-recognized bouglar)
; ))

)
;un-comment the following line if metric is needed
;(:metric minimize (???))