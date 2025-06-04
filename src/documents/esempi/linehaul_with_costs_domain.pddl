;; Dominio linehaul con costi, esempio tratto da Chapter 2.
;; Sintassi verificata con VAL@github: nessun errore o warning.

(define (domain linehaul_with_costs)
    (:requirements :strips :typing :action-costs) ;; Requisiti del dominio: STRIPS, tipi e costi azione

    (:types
        location truck quantity - object        ;; Tipi base: location, truck, quantity derivano da object
        refrigerated_truck - truck              ;; refrigerated_truck è un sottotipo di truck
    )

    ;; Modalità alternativa di dichiarazione tipi:
    ;; (:types
    ;;  refrigerated_truck - truck
    ;;  location truck quantity
    ;;  )

    (:predicates
        (at ?t - truck ?l - location)                    ;; Predicate: camion ?t si trova nella location ?l
        (free_capacity ?t - truck ?q - quantity)         ;; Predicate: camion ?t ha capacità libera ?q
        (demand_chilled_goods ?l - location ?q - quantity) ;; Predicate: domanda di beni refrigerati in ?l pari a ?q
        (demand_ambient_goods ?l - location ?q - quantity) ;; Predicate: domanda di beni ambientali in ?l pari a ?q
        (plus1 ?q1 ?q2 - quantity)                        ;; Predicate: ?q2 è il successore di ?q1 (es. q2 = q1+1)
    )

    (:functions
        (distance ?l1 ?l2 - location)      ;; Funzione che restituisce la distanza tra due location
        (per_km_cost ?t - truck)           ;; Funzione che restituisce costo per km per un camion ?t
        (total-cost)                       ;; Funzione globale che tiene traccia del costo totale
    )

    ;; Azione di consegna di beni ambientali (non refrigerati)
    (:action deliver_ambient
        :parameters (?t - truck ?l - location ?d ?d_less_one ?c ?c_less_one - quantity)  ;; Parametri azione
        :precondition (and (at ?t ?l)               ;; Il camion ?t deve essere in posizione ?l
            (demand_ambient_goods ?l ?d)             ;; La domanda a ?l è ?d
            (free_capacity ?t ?c)                     ;; La capacità libera del camion ?t è ?c
            (plus1 ?d_less_one ?d) ;; vero solo se ?d > n0, cioè ?d_less_one è ?d - 1
            (plus1 ?c_less_one ?c)) ;; vero solo se ?c > n0, cioè ?c_less_one è ?c - 1
        :effect (and (not (demand_ambient_goods ?l ?d)) ;; diminuisce la domanda ambientale di 1
            (demand_ambient_goods ?l ?d_less_one)         ;; aggiorna la domanda a ?d_less_one
            (not (free_capacity ?t ?c))                   ;; diminuisce la capacità libera del camion di 1
            (free_capacity ?t ?c_less_one))
    )

    ;; Azione di consegna di beni refrigerati
    (:action deliver_chilled
        ;; Nota: ?t deve essere un camion refrigerato (refrigerated_truck)
        :parameters (?t - refrigerated_truck ?l - location ?d ?d_less_one ?c ?c_less_one - quantity)
        :precondition (and (at ?t ?l)
            (demand_chilled_goods ?l ?d)
            (free_capacity ?t ?c)
            (plus1 ?d_less_one ?d) ;; vero solo se ?d > n0
            (plus1 ?c_less_one ?c)) ;; vero solo se ?c > n0
        :effect (and (not (demand_chilled_goods ?l ?d))
            (demand_chilled_goods ?l ?d_less_one)
            (not (free_capacity ?t ?c))
            (free_capacity ?t ?c_less_one))
    )

    ;; Azione di guida del camion da una location a un'altra
    (:action drive
        :parameters (?t - truck ?from ?to - location)    ;; Parametri: camion e due location
        :precondition (at ?t ?from)                       ;; Precondizione: camion deve essere nella posizione di partenza
        :effect (and (not (at ?t ?from))                  ;; Effetto: camion non è più alla posizione di partenza
            (at ?t ?to)                                   ;; Camion si trova alla destinazione
            (increase                                       ;; Incrementa il costo totale
                (total-cost)
                (* (distance ?from ?to) (per_km_cost ?t))))  ;; Costo = distanza percorsa * costo per km del camion
    )
)
