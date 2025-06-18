(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    liora foresta montagna tempio - luogo
    machete corda amuleto-solare has-key - oggetto
  )

  (:init
    (in arlen liora)
    (accessibile liora foresta)
    (accessible foresta montagna)
    (accessible montagna tempio)
    (bloccato foresta)
    (has-key false)
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-solare)
    )
  )
)