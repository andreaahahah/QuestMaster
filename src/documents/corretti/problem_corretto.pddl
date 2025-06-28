(define (problem linehaul-example) ; Definizione del problema chiamato "linehaul-example"
    (:domain linehaul_without_costs) ; Specifica il dominio associato

    (:objects
        ADoubleRef - refrigerated_truck ; Camion refrigerato chiamato ADoubleRef
        BDouble - truck ; Camion normale chiamato BDouble
        depot GV E BW - location ; Quattro location: deposito e tre destinazioni GV, E, BW
        n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14 n15 n16 n17 n18 n19 n20 n21 n22 n23 n24 n25 n26 n27 n28 n29 n30 n31 n32 n33 n34 n35 n36 n37 n38 n39 n40 - quantity ; Definisce quantità da n0 a n40 come oggetti di tipo quantity
    )

    (:init
        (at ADoubleRef depot) ; Il camion refrigerato ADoubleRef è inizialmente al deposito
        (at BDouble depot) ; Anche il camion BDouble è al deposito
        (free_capacity ADoubleRef n40) ; Capacità libera di ADoubleRef è 40 (n40)
        (free_capacity BDouble n34) ; Capacità libera di BDouble è 34 (n34)

        (demand_chilled_goods GV n18) ; Domanda di merci refrigerate a GV è 18
        (demand_ambient_goods GV n12) ; Domanda di merci ambientali a GV è 12
        (demand_chilled_goods E n7) ; Domanda refrigerata a E è 7
        (demand_ambient_goods E n2) ; Domanda ambientale a E è 2
        (demand_chilled_goods BW n3) ; Domanda refrigerata a BW è 3
        (demand_ambient_goods BW n0) ; Domanda ambientale a BW è 0 (nessuna domanda)

        ;; Definizione delle relazioni successore "plus1" tra tutte le quantità
        (plus1 n0 n1)
        (plus1 n1 n2)
        (plus1 n2 n3)
        (plus1 n3 n4)
        (plus1 n4 n5)
        (plus1 n5 n6)
        (plus1 n6 n7)
        (plus1 n7 n8)
        (plus1 n8 n9)
        (plus1 n9 n10)
        (plus1 n10 n11)
        (plus1 n11 n12)
        (plus1 n12 n13)
        (plus1 n13 n14)
        (plus1 n14 n15)
        (plus1 n15 n16)
        (plus1 n16 n17)
        (plus1 n17 n18)
        (plus1 n18 n19)
        (plus1 n19 n20)
        (plus1 n20 n21)
        (plus1 n21 n22)
        (plus1 n22 n23)
        (plus1 n23 n24)
        (plus1 n24 n25)
        (plus1 n25 n26)
        (plus1 n26 n27)
        (plus1 n27 n28)
        (plus1 n28 n29)
        (plus1 n29 n30)
        (plus1 n30 n31)
        (plus1 n31 n32)
        (plus1 n32 n33)
        (plus1 n33 n34)
        (plus1 n34 n35)
        (plus1 n35 n36)
        (plus1 n36 n37)
        (plus1 n37 n38)
        (plus1 n38 n39)
        (plus1 n39 n40)
    )

    (:goal
        (and
            (demand_chilled_goods GV n0) ; Obiettivo: la domanda refrigerata a GV deve essere azzerata
            (demand_ambient_goods GV n0) ; Obiettivo: la domanda ambientale a GV deve essere azzerata
            (demand_chilled_goods E n0) ; Obiettivo: domanda refrigerata a E azzerata
            (demand_ambient_goods E n0) ; Obiettivo: domanda ambientale a E azzerata
            (demand_chilled_goods BW n0) ; Obiettivo: domanda refrigerata a BW azzerata
            (demand_ambient_goods BW n0) ; Obiettivo: domanda ambientale a BW azzerata
            (at ADoubleRef depot) ; Entrambi i camion devono tornare al deposito
            (at BDouble depot)
        )
    )
)

