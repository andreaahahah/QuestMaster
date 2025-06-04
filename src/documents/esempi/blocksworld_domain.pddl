(define (domain blocksworld) ; Definizione del dominio chiamato 'blocksworld'
    (:requirements :strips :typing) ; Specifica che il dominio usa STRIPS e typing

    (:types
        block ; Definizione del tipo 'block'
    )

    (:predicates
        (on ?x - block ?y - block) ; Il blocco ?x è sopra il blocco ?y
        (ontable ?x - block)       ; Il blocco ?x è direttamente sul tavolo
        (clear ?x - block)         ; Nessun blocco è sopra il blocco ?x
        (holding ?x - block)       ; Il robot tiene in mano il blocco ?x
        (handempty)                ; Il robot non tiene nulla in mano
    )

    (:action pick-up ; Azione per prendere un blocco dal tavolo
        :parameters (?x - block) ; Parametro: blocco ?x
        :precondition (and (clear ?x) (ontable ?x) (handempty)) ; Precondizioni: il blocco è libero, sul tavolo, e la mano è vuota
        :effect (and
            (not (ontable ?x)) ; Il blocco non è più sul tavolo
            (not (clear ?x))   ; Il blocco non è più libero (ora è tenuto)
            (not (handempty))  ; La mano non è più vuota
            (holding ?x))      ; Il blocco è ora tenuto in mano
    )

    (:action put-down ; Azione per appoggiare un blocco sul tavolo
        :parameters (?x - block) ; Parametro: blocco ?x
        :precondition (holding ?x) ; Precondizione: il blocco è in mano
        :effect (and
            (ontable ?x)       ; Il blocco è ora sul tavolo
            (clear ?x)         ; Il blocco è libero
            (handempty)        ; La mano è vuota
            (not (holding ?x))) ; Il blocco non è più in mano
    )

    (:action unstack ; Azione per togliere un blocco da sopra un altro
        :parameters (?x - block ?y - block) ; Parametri: blocco ?x sopra blocco ?y
        :precondition (and (on ?x ?y) (clear ?x) (handempty)) ; Precondizioni: ?x è sopra ?y, è libero, e la mano è vuota
        :effect (and
            (holding ?x)        ; Il blocco ?x è ora in mano
            (clear ?y)          ; Il blocco ?y è ora libero
            (not (on ?x ?y))    ; ?x non è più sopra ?y
            (not (clear ?x))    ; ?x non è più libero
            (not (handempty)))  ; La mano non è più vuota
    )

    (:action stack ; Azione per mettere un blocco sopra un altro
        :parameters (?x - block ?y - block) ; Parametri: blocco ?x da mettere sopra blocco ?y
        :precondition (and (holding ?x) (clear ?y)) ; Precondizioni: ?x è in mano, ?y è libero
        :effect (and
            (on ?x ?y)          ; ?x è ora sopra ?y
            (clear ?x)          ; ?x è libero
            (handempty)         ; La mano è vuota
            (not (holding ?x))  ; Il blocco non è più in mano
            (not (clear ?y)))   ; ?y non è più libero
    )
)
