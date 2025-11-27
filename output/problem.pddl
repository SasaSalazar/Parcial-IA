(define (problem generated-problem)
  (:domain generated_domain)
  
  (:objects 
    cafe robot - object
    home - location)

  (:init
    (at robot home)
  )
  (:goal (done robot))
)
