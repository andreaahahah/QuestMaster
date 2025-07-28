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
      (apre-cancello arlen tempio) ; Arlen opens the door to the temple
      (in arlen tempio)          ; Arlen is in the temple
      (collezionato arlen amuleto-del-sole) ; Arlen has collected the amulet of the sun
    )
  )
)

