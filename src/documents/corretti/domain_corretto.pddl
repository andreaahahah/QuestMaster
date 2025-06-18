(define (domain arlen-quest)
  (:requirements :strips :typing)

  (:types
    luogo oggetto personaggio
  )

  (:predicates
    (in ?p - personaggio ?l - luogo) 
    (collezionato ?p - personaggio ?o - oggetto) 
    (accessibile ?from - luogo ?to - luogo) 
    (bloccato ?l - luogo) 
    (usa ?o - oggetto ?l - luogo)
  )

  (:action muovi
    :parameters (?p - personaggio ?from - luogo ?to - luogo)
    :precondition (and (in ?p ?from) (accessibile ?from ?to) (not (bloccato ?to)))
    :effect (and (not (in ?p ?from)) (in ?p ?to))
  )

  (:action raccogli
    :parameters (?p - personaggio ?o - oggetto ?l - luogo)
    :precondition (and (in ?p ?l))
    :effect (collezionato ?p ?o)
  )

  (:action usa-ogg
    :parameters (?p - personaggio ?o - oggetto ?l - luogo)
    :precondition (and (in ?p ?l) (collezionato ?p ?o) (usa ?o ?l))
    :effect (not (bloccato ?l))
  )

  (:action supera-cancello
    :parameters (?p - personaggio ?c - luogo)
    :precondition (and (in ?p ?c) (has-key ?p))
    :effect (not (bloccato ?c))
  )
)

**[PROBLEM]**