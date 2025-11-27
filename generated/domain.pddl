(define (domain generated_domain)
  (:requirements :strips :typing)
  (:types agent object location target)
  (:predicates
    (at ?a - agent ?l - location)
    (in ?o - object ?l - location)
    (has ?a - agent ?o - object)
    (prepared ?o - object)
    (heated ?o - object)
    (open ?p - object)
    (closed ?p - object)
    (charged ?o - object)
    (clean ?o - object)
    (neutralized ?t - target)
  )

  (:action open
    :parameters (?a - agent ?p - object)
    :precondition ()
    :effect (open ?p)
  )

  (:action pick
    :parameters (?a - agent ?o - object ?l - location)
    :precondition (and (at ?a ?l) (in ?o ?l))
    :effect (and (not (in ?o ?l)) (has ?a ?o))
  )
)
