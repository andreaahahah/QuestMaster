file PDDL generati:

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
)

[PROBLEM]
(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    liora foresta tempio - luogo
    chiave- speciale amuleto-del-sole - oggetto
    machete corda - oggetto
  )

  (:init
    (in arlen liora)
    (accessibile liora foresta)
    (accessibile foresta tempio)
    (bloccato foresta) ;; pericolo nella foresta
    (bloccato tempio) ;; cancello magico richiede chiave speciale
    (usa machete foresta) ;; il machete serve per superare la foresta
    (usa corda tempio) ;; la corda serve per superare il cancello magico
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-del-sole)
    )
  )
)

Nota che ho seguito le regole di sintassi PDDL e ho definito i tipi di oggetti, i predicati logici rilevanti e le azioni STRIPS che il protagonista può intraprendere. Inoltre, ho definito gli oggetti specifici della missione, lo stato iniziale e lo stato obiettivo.