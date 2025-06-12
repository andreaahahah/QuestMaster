;;; ------------------------
;;; STORY 1: Simeon e l'Acqua Magica
;;; Dominio: Avventura nel Deserto
;;; ------------------------
;;; === STORIA ===

"Simeon è un giovane che parte da un piccolo borgo per recuperare la cosidetta "Acqua magica",che risolverebbe i problemi di siccità del villaggio.Questa acqua si trova in una sorgente in un luogo remoto e nascosto.Per arrivare sul posto,simeon dovrà attraversare il deserto,una strada pericolosa piena di animali feroci ed altri ostacoli lungo il cammino;durante la quest potrà collezionare oggetti che gli serviranno per andare avanti.Branching Factor: minimo 2, massimo 4
Depth Constraints: minimo 4, massimo 7";


;;; === DOMAIN FILE ===
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

;;; === PROBLEM FILE ===
(define (problem simeon-problema)
  (:domain simeon-quest)

  ;; Oggetti nel mondo
  (:objects
    simeon - personaggio
    villaggio deserto grotta sorgente - luogo
    spada bastone acqua-magica - oggetto
  )

  ;; Stato iniziale
  (:init
    (in simeon villaggio)
    (accessibile villaggio deserto)
    (accessibile deserto grotta)
    (accessibile grotta sorgente)
    (bloccato deserto) ;; pericolo nel deserto
    (bloccato grotta) ;; ostacolo nella grotta
    (usa spada deserto) ;; la spada può sconfiggere i pericoli nel deserto
    (usa bastone grotta) ;; il bastone serve per superare la grotta
  )

  ;; Obiettivo finale
  (:goal
    (and
      (in simeon sorgente)
      (collezionato simeon acqua-magica)
    )
  )
)