
(define (problem generated-problem)
  (:domain generated_domain)
  (:objects
    agente arreglar máquina tener destornillador robot - object
    home - location
  )
  (:init
    (at robot home)
  )
  (:goal (step-done-1))
)
