(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    liora foresta montagna tempio - luogo
    machete corda amuleto-del-sole - oggetto
  )

  (:init
    (in arlen liora)
    (accessibile liora foresta)
    (accessibile foresta montagna)
    (accessibile montagna tempio)
    (bloccato foresta)
    (bloccato montagna)
    (usa machete foresta)
    (usa corda montagna)
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-del-sole)
    )
  )
)