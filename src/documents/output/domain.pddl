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

  (:action esplora
    :parameters (?p - personaggio ?from - luogo ?to - luogo)
    :precondition (and (in ?p ?from) (accessibile ?from ?to) (not (bloccato ?to)))
    :effect (and (not (in ?p ?from)) (in ?p ?to))
  )

  (:action trova-chiave
    :parameters (?p - personaggio ?o - oggetto ?l - luogo)
    :precondition (and (in ?p ?l) (collezionato ?p ?o) (usa ?o ?l))
    :effect (not (bloccato ?l))
  )

  (:action sconfiggi-mostro
    :parameters (?p - personaggio ?m - oggetto)
    :precondition (and (in ?p ?l) (collezionato ?p ?m))
    :effect (sconfitto ?m)
  )

  (:action risolve-enigma
    :parameters (?p - personaggio ?e - oggetto)
    :precondition (and (in ?p ?l) (collezionato ?p ?e))
    :effect (not (bloccato ?l))
  )

  (:action sconfiggi-guardiano
    :parameters (?p - personaggio ?g - oggetto)
    :precondition (and (in ?p ?l) (collezionato ?p ?g))
    :effect (not (bloccato ?l))
  )
)