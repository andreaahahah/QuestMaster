;;; ------------------------
;;; STORY 2: Lidia e la Bacchetta Mistica
;;; Dominio: Avventura nella Foresta
;;; ------------------------

;;; === DOMAIN FILE ===
(define (domain lidia-quest)
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
)

;;; === PROBLEM FILE ===
(define (problem lidia-problema)
  (:domain lidia-quest)

  (:objects
    lidia - personaggio
    citta foresta montagna tempio - luogo
    machete corda bacchetta-mistica - oggetto
  )

  (:init
    (in lidia citta)
    (accessibile citta foresta)
    (accessibile foresta montagna)
    (accessibile montagna tempio)
    (bloccato foresta)
    (bloccato montagna)
    (usa machete foresta)
    (usa corda montagna)
  )

  (:goal
    (and
      (in lidia tempio)
      (collezionato lidia bacchetta-mistica)
    )
  )
)
