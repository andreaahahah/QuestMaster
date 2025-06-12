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