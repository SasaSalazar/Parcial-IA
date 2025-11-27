(define (problem generated-problem)
  (:domain generated_domain)
  
  (:objects 
    llave puerta robot - object
    home puerta - location)

  (:init
    (in llave home)
  )
  (:goal (and
    (has robot llave)
    (open puerta)
))
)
