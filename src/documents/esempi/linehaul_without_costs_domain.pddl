(define (domain linehaul_without_costs) ; Definizione del dominio chiamato "linehaul_without_costs"
    (:requirements :strips :typing) ; Richiede STRIPS e supporto per tipi

    (:types
        location truck quantity - object ; Definizione dei tipi base: location, truck e quantity sono sotto-tipi di object
        refrigerated_truck - truck ; refrigerated_truck è un sotto-tipo di truck (camion refrigerati)
    )

    (:predicates
        (at ?t - truck ?l - location) ; Predicato che indica che il camion ?t si trova nella location ?l
        (free_capacity ?t - truck ?q - quantity) ; Capacità libera ?q del camion ?t
        (demand_chilled_goods ?l - location ?q - quantity) ; Domanda di merci refrigerate alla location ?l di quantità ?q
        (demand_ambient_goods ?l - location ?q - quantity) ; Domanda di merci ambientali (non refrigerate) alla location ?l di quantità ?q
        (plus1 ?q1 ?q2 - quantity) ; Relazione aritmetica: ?q2 = ?q1 + 1 (usata per decrementare quantità)
    )

    ;; L’effetto dell’azione deliver_ambient è diminuire la domanda di merci ambientali ?l
    ;; e la capacità libera del camion ?t di una unità.
    (:action deliver_ambient
        :parameters (?t - truck ?l - location ?d ?d_less_one ?c ?c_less_one - quantity) ; Parametri: camion, location, quantità correnti e decrementate
        :precondition (and (at ?t ?l) ; Il camion deve essere nella location ?l
            (demand_ambient_goods ?l ?d) ; Deve esserci domanda di merci ambientali ?d in ?l
            (free_capacity ?t ?c) ; Il camion deve avere capacità libera ?c
            (plus1 ?d_less_one ?d) ; ?d = ?d_less_one + 1 (per decremento)
            (plus1 ?c_less_one ?c)) ; ?c = ?c_less_one + 1 (per decremento)
        :effect (and (not (demand_ambient_goods ?l ?d)) ; La domanda corrente ?d viene rimossa
            (demand_ambient_goods ?l ?d_less_one) ; Ora la domanda è decrementata
            (not (free_capacity ?t ?c)) ; La capacità libera attuale viene rimossa
            (free_capacity ?t ?c_less_one)) ; La capacità libera è decrementata
    )

    (:action deliver_chilled
        ;; Nota: restrizione di tipo su ?t, deve essere un camion refrigerato.
        :parameters (?t - refrigerated_truck ?l - location ?d ?d_less_one ?c ?c_less_one - quantity)
        :precondition (and (at ?t ?l) ; Il camion refrigerato deve essere nella location
            (demand_chilled_goods ?l ?d) ; Deve esserci domanda di merci refrigerate
            (free_capacity ?t ?c) ; Capacità libera attuale
            (plus1 ?d_less_one ?d) ; Quantità richiesta decrementata di 1
            (plus1 ?c_less_one ?c)) ; Capacità libera decrementata di 1
        :effect (and (not (demand_chilled_goods ?l ?d)) ; Rimuove la domanda corrente
            (demand_chilled_goods ?l ?d_less_one) ; Inserisce la domanda decrementata
            (not (free_capacity ?t ?c)) ; Rimuove capacità libera attuale
            (free_capacity ?t ?c_less_one)) ; Inserisce capacità decrementata
    )

    (:action drive
        :parameters (?t - truck ?from ?to - location) ; Parametri: camion, luogo di partenza e destinazione
        :precondition (at ?t ?from) ; Il camion deve essere nel luogo di partenza
        :effect (and (not (at ?t ?from)) ; Il camion non è più nel luogo di partenza
            (at ?t ?to)) ; Ora è nella destinazione
    )
)
