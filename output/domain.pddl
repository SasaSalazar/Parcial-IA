
(define (domain generated_domain)
  (:requirements :strips :typing)
  (:types agent object location target step)
  (:predicates
    (at ?a - agent ?l - location)
    (in ?o - object ?l - location)
    (has ?a - agent ?o - object)
    (neutralized ?t - target)
    (step-done-0)
    (step-done-1)
  )

  (:action repair-0
    :parameters (?a - agent ?o - object ?l - location 0 - step 1 - step)
    :precondition (step-done-0)
    :effect (step-done-1)
  )

)
