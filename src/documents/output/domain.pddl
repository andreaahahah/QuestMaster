(define (domain simeon-quest)
  (:requirements :strips :typing)

  ;; Definizione dei tipi di oggetti nel mondo
  (:types
    luogo oggetto personaggio
  )

  ;; Predicati che rappresentano lo stato del mondo
  (:predicates
    (in ?p - personaggio ?l - luogo) ;; Il personaggio si trova in un certo luogo
    (collezionato ?p - personaggio ?o - oggetto) ;; Il personaggio ha raccolto un oggetto
    (accessibile ?from - luogo ?to - luogo) ;; È possibile spostarsi da un luogo a un altro
    (bloccato ?l - luogo) ;; Il luogo ha un ostacolo che impedisce l'accesso
    (sconfitto ?ostacolo - oggetto) ;; L'ostacolo è stato superato (es. animale pericoloso)
    (usa ?o - oggetto ?l - luogo) ;; Un oggetto può essere usato per superare un luogo
  )

  ;; Azione per muoversi tra luoghi
  (:action muovi
    :parameters (?p - personaggio ?from - luogo ?to - luogo)
    :precondition (and (in ?p ?from) (accessibile ?from ?to) (not (bloccato ?to)))
    :effect (and (not (in ?p ?from)) (in ?p ?to))
  )

  ;; Azione per raccogliere un oggetto
  (:action raccogli
    :parameters (?p - personaggio ?o - oggetto ?l - luogo)
    :precondition (and (in ?p ?l))
    :effect (collezionato ?p ?o)
  )

  ;; Azione per usare un oggetto per superare un ostacolo
  (:action usa-ogg
    :parameters (?p - personaggio ?o - oggetto ?l - luogo)
    :precondition (and (in ?p ?l) (collezionato ?p ?o) (usa ?o ?l))
    :effect (not (bloccato ?l))
  )
)
