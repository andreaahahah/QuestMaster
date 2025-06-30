(define (problem arlen-problema)
  (:domain arlen-quest)

  (:objects
    arlen - personaggio
    liora foresta montagna tempio - luogo
    machete corda amuleto-del-sol - oggetto
  )

  (:init
    (in arlen liora)
    (accessibile liora foresta)
    (accessible foresta montagna)
    (accessible montagna tempio)
    (bloccato foresta)
    (bloccato montagna)
    (usa machete foresta)
    (usa corda montagna)
  )

  (:goal
    (and
      (in arlen tempio)
      (collezionato arlen amuleto-del-sol)
    )
  )
)

Nota: ho mantenuto la struttura generale degli esempi precedenti, ma ho modificato alcuni dettagli per adattarla alla storia narrativa specifica.