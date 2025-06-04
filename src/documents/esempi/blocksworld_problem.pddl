(define (problem blocksworld-example) ; Definizione del problema chiamato "blocksworld-example"
    (:domain blocksworld) ; Specifica che questo problema usa il dominio "blocksworld"

    (:objects
        red yellow blue orange - block ; Definizione degli oggetti presenti nel mondo: quattro blocchi
    )

    (:init ; Stato iniziale del mondo
        (ontable yellow) ; Il blocco yellow è sul tavolo
        (ontable orange) ; Il blocco orange è sul tavolo
        (ontable red) ; Il blocco red è sul tavolo
        (on blue orange) ; Il blocco blue è sopra il blocco orange
        (clear blue) ; Il blocco blue non ha niente sopra
        (clear red) ; Il blocco red non ha niente sopra
        (clear yellow) ; Il blocco yellow non ha niente sopra
        (handempty) ; La mano è libera (non sta tenendo nessun blocco)
    )

    (:goal ; Obiettivo da raggiungere
        (and
            (on orange blue) ; Il blocco orange deve essere sopra il blocco blue
            (ontable blue) ; Il blocco blue deve essere sul tavolo
            (ontable yellow) ; Il blocco yellow deve essere sul tavolo
            (ontable red) ; Il blocco red deve essere sul tavolo
            (clear orange) ; Il blocco orange non deve avere niente sopra
            (clear yellow) ; Il blocco yellow non deve avere niente sopra
            (clear red) ; Il blocco red non deve avere niente sopra
        )
    )
)
