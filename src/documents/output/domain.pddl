e file PDDL generati a partire dalla descrizione narrativa:

[DOMAIN]
(define (domain arlen-quest)
  (:requirements :strips :typing)

  (:types
    luogo oggetto personaggio
  )

  (:predicates
    (in ?p - personaggio ?l - luogo) ;; Il personaggio si trova in un certo luogo
    (collezionato ?p - personaggio ?o - oggetto) ;; Il personaggio ha raccolto un oggetto
    (accessibile ?from - luogo ?to - luogo) ;; È possibile spostarsi da un luogo a un altro
    (bloccato ?l - luogo) ;; Il luogo ha un ostacolo che impedisce l'accesso
    (usa ?o - oggetto ?l - luogo) ;; Un oggetto può essere usato per superare un luogo
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

  (:action apre-cancello
    :parameters (?p - personaggio ?c - luogo)
    :precondition (and (in ?p ?c) (collezionato ?p "chiave"))
    :effect (not (bloccato ?c))
  )
)

[PROBLEM]
(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    liora foresta tempio - luogo
    machete corda amuleto-del-sole chiave - oggetto
  )

  (:init
    (in arlen liora)
    (accessibile liora foresta)
    (accessibile foresta tempio)
    (bloccato foresta)
    (bloccato tempio)
    (usa machete foresta)
    (usa corda tempio)
    (not (collezionato arlen chiave))
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-del-sole)
    )
  )
)

Nota: Ho aggiunto un'azione "apre-cancello" per permettere a Arlen di superare il cancello magico con la chiave speciale