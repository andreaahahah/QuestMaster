(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    villaggio foresta tempio - luogo
    machete corda amuleto-del-sol - oggetto
  )

  (:init
    (in arlen villaggio)
    (accessibile villaggio foresta)
    (accessibile foresta tempio)
    (bloccato foresta)
    (bloccato tempio)
    (usa machete foresta)
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-del-sol)
    )
  )
)

Nota: Ho mantenuto la struttura sintetica e le azioni chiave identificate nella descrizione narrativa, anche se non ho copiato i nomi di variabili o tipi da altri esempi.