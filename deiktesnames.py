# -*- coding: utf-8 -*-

columnnames={
    'ky':u'Κέντρο υγείας',
    'perif_iatreio':u'Περιφερειακό ιατρείο',
    'u_description':u'Δήμος',
    'peu_description': u'ΠΕ',
    'eponymia':u'Νοσοκομείο',
    'nearest_ks':u'Εγγύτερο Κρατικό νοσοκομείο',
    'nearest_ky':u'Εγγύτερο Κέντρο Υγείας',
    'monimos2011':u'Μόνιμος πληθυσμός 2011',
    'year':u'Έτος',
    'iatroi': u'Ιδιώτες Ιατροί',
    'polyiatreia':u'Πολυιατρεία',
    'kentra_ygeias':u'Κέντρα υγείας',
    'diagnostika_ergastiria':u'Διαγνωστικά εργαστήρια',
    'kratika_nosokomeia' :u'Κρατικά νοσοκομεία',
    'per_iatreia':u'Περιφερειακά ιατρεία',
    'deiktis':u'Δείκτης',
    'deiktis21111':u'Μόνιμος πληθυσμός που εξυπηρετούνται απο το ΚΥ',
    'distance21113':u'Απόσταση προς εγγύτερο Κρατικό Νοσοκομείο (σε χλμ.)',
    'deiktis21116':u'Μέση απόσταση των κατοίκων ως προς το πλησιέστερο Κ.Υ',
    'deiktis21118':u'Μέγιστη απόσταση των κατοίκων ως προς το πλησιέστερο Κ.Υ',
    'index211110':u'ΚΥ με πολλαπλή σχέση με την τοπική αυτοδιοίκηση.',
    'index21131':u'Ποσοστό κάλυψης οργανικών θέσεων σύνολο',
    'index21132':u'Iατροί σύνολο/εξετασθέντες ',
    'index21134':u'Iατροί σύνολο/εξετάσεις',
    'index21136':u'Iατροί σύνολο/συνταγογrαφήσεις',
    'index21138':u'Κατοικοι ανα νοσηλευτή',
    'index21139':u'Κατοικοι ανα παραιατρικο προσωπικό',
    'index211310':u'Εξετάσεις/Πληθυσμό ',
    'index21112':u'Μόνιμος πληθυσμός που εξυπηρετούνται απο το ΠΙ',
    'index21114':u'Απόσταση από κρατικό νοσοκομείο(σε χλμ.)',
    'distance21115':u'Απόσταση από ΚΥ(σε χλμ.)',
    'deiktis21117':u'Μέση απόσταση των κατοίκων ως προς το πλησιέστερο Π.Ι',
    'deiktis21119':u'Μέγιστη απόσταση των κατοίκων ως προς το πλησιέστερο Π.Ι ',

    'deiktis21121':u'Σύνολο Ιατρών (ΚΥ) ανά κάτοικο(‰)',
    'deiktis21124':u'Σύνολο Ιδιωτών Ιατρών ανά κάτοικο(‰)',

}


deiktes = \
    {

        u"Δείκτες υποδομής":
            [
        {'label': u'Κ.Υ. με πολλαπλή σχέση με την τοπική αυτοδιοίκηση','sql':u'select pk_uid::integer, ky from fun_deiktis_211110','hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':True ,'perYearData':True},
        {'label': u'Μόνιμος πληθυσμός που εξυπηρετούνται απο το ΚΥ', 'sql':u'select pk_uid,ky ,deiktis FROM fun_deiktis_21111', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Μόνιμος πληθυσμός που εξυπηρετούνται απο το ΠΙ', 'sql':u'select pk_uid, perif_iatreio, deiktis  FROM fun_deiktis_21112', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Μέση απόσταση των κατοίκων ως προς το πλησιέστερο Κ.Υ', 'sql':u'select pk_uid, ky,deiktis  FROM   fun_deiktis_21116', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Μέση απόσταση των κατοίκων ως προς το πλησιέστερο Π.Ι', 'sql':u'select pk_uid, perif_iatreio ,deiktis   FROM fun_deiktis_21117', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Μέγιστη απόσταση των κατοίκων ως προς το πλησιέστερο Κ.Υ', 'sql':u'select pk_uid, ky,deiktis  FROM   fun_deiktis_21118', 'hideColumns':[0],'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Μέγιστη απόσταση των κατοίκων ως προς το πλησιέστερο Π.Ι', 'sql':u'select pk_uid, perif_iatreio ,deiktis   FROM fun_deiktis_21119' , 'hideColumns':[0],'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Χωρική εξάρτηση & Απόσταση Νοσοκομείο – ΚΥ (χλμ)', 'sql':u'select pk_uid_ky::integer as pk_uid,ky ,pk_uid_nosok,eponymia ,distance from fun_deiktis_21113', 'hideColumns':[0,2], 'SearchField':'pk_uid', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Χωρική εξάρτηση & Απόσταση Νοσοκομείο – ΠΙ (χλμ)', 'sql':u'select  pk_uid_pi::integer as pk_uid,  perif_iatreio,  pk_uid_nosok,  eponymia , distance from fun_deiktis_21114', 'hideColumns':[0,2], 'SearchField':'pk_uid', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Χωρική εξάρτηση & Απόσταση ΚΥ – ΠΙ (χλμ)', 'sql':u'select pk_uid_ky ,pk_uid_pi::integer as pk_uid, perif_iatreio, ky , distance from fun_deiktis_21115', 'hideColumns':[0,1],  'SearchField':'pk_uid', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Ζώνες χωρικής επιρροής των κέντρων υγείας', 'sql':u'select pk_uid::integer, ky from fun_deiktis_211111', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':True, 'perYearData':True}
             ],
        u"Δείκτες Επάρκειας των Ανθρωπίνων Πόρων":
            [
        {'label': u'Ποσοστό κάλυψης οργανικών θέσεων σύνολο', 'sql':u'select pk_uid, ky, deiktis  from fun_deiktis_21131', 'hideColumns':[0],  'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Iατροί σύνολο/εξετασθέντες  (‰)', 'sql':u'select pk_uid, ky, deiktis  from fun_deiktis_21132', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Iατροί σύνολο/εξετάσεις  (‰)', 'sql':u'select pk_uid, ky , deiktis  from fun_deiktis_21134', 'hideColumns':[0],  'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Iατροί σύνολο/συνταγογραφήσεις  (‰)', 'sql':u'select pk_uid, ky, deiktis  from fun_deiktis_21136', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Αριθμός κατοίκων ανά νοσηλευτή', 'sql':u'select pk_uid, ky , deiktis   from fun_deiktis_21138', 'hideColumns':[0],  'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Αριθμός κατοίκων ανά παραϊατρικό προσωπικό', 'sql':u'select pk_uid, ky , deiktis   from fun_deiktis_21139', 'hideColumns':[0],  'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Εξετάσεις/Πληθυσμό', 'sql':u'select pk_uid, ky , deiktis    from fun_deiktis_211310', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':False,'perYearData':True}
            ],

        u"Πλήθος υποδομών ανά διοικητική ενότητα":
            [
        {'label': u'Πλήθος υποδομών ανά δήμο', 'sql':u'select elstatid2011, peu_description, u_description ,monimos2011, iatroi , polyiatreia, diagnostika_ergastiria , ky as kentra_ygeias, kratika_nosokomeia, per_iatreia from fun_deiktis_21141', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Πλήθος υποδομών ανά περιφερειακή ενότητα', 'sql':u'select elstatid2011, u_description as "peu_description", monimos2011, iatroi , polyiatreia, diagnostika_ergastiria, ky as "kentra_ygeias", kratika_nosokomeia, per_iatreia from fun_deiktis_21142', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':True,'perYearData':True},
             ],

        u"Σύνοψη δεικτών":
            [
        {'label': u'Σύνοψη δεικτών ΚΥ', 'sql':u'select pk_uid,ky,year,deiktis21111,eponymia as nearest_ks, distance21113 ,deiktis21116 ,deiktis21118,index211110,index21131,index21132,index21134,index21136,index21138,index21139,index211310 from fun_deiktis_21151', 'hideColumns':[0,2],  'SearchField':'pk_uid', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Σύνοψη δεικτών ΠΙ', 'sql':u'select pk_uid,perif_iatreio,year,index21112,eponymia as nearest_ks,index21114,ky,distance21115,deiktis21117,deiktis21119 from fun_deiktis_21152', 'hideColumns':[0], 'SearchField':'pk_uid', 'OnlyAdd':True,'perYearData':True},
        {'label': u'Σύνοψη δεικτών δήμων', 'sql':u'select elstatid2011,u_description,deiktis21121,deiktis21124,iatroi,polyiatreia,diagnostika_ergastiria,ky as kentra_ygeias,kratika_nosokomeia,per_iatreia from fun_deiktis_21153', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':True,'perYearData':True},
            ],

        u"Δείκτες Επάρκειας Υγειονομικής Κάλυψης (ανά δήμο)":
        [
        {'label': u'Σύνολο Ιατρών (K.Υ.) ανά κάτοικο(‰)', 'sql':u'select elstatid2011, u_description,  deiktis from fun_deiktis_21121_iatroi_ky_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΑΚΤΙΝΟΛΟΓΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description   , deiktis from fun_deiktis_21123_iatroi_ky_aktinologiko_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΓΥΝΑΙΚΟΛΟΓΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_gynaikologia_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΚΑΡΔΙΟΛΟΓΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis  from fun_deiktis_21123_iatroi_ky_kardiologia_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΜΙΚΡΟΒΙΟΛΟΓΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description , deiktis  from fun_deiktis_21123_iatroi_ky_mikroviologoi_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΟΔΟΝΤΙΑΤΡΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_odontiatriki_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΟΡΘΟΠΕΔΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_orthopediki_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΠΑΙΔΙΑΤΡΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_paidiatriki_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΠΑΙΔΟΨΥΧΙΑΤΡΙΚΟ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_paidopsix_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:Γ.Ι.-ΠΑΘΟΛΟΓΙΑ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_pathologia_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΨΥΧΙΑΤΡΙΚΗ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_psixiatriki_per_dimo', 'hideColumns':[0], 'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιατρών (K.Υ.)(Ειδικότητα:ΧΕΙΡΟΥΡΓΙΚΗ) ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description  , deiktis   from fun_deiktis_21123_iatroi_ky_xeirourgiki_per_dimo', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False,'perYearData':True},
        {'label': u'Σύνολο Ιδιωτών Ιατρών ανά κάτοικο (‰)', 'sql':u'select elstatid2011, u_description , deiktis  from deiktis_21124', 'hideColumns':[0],  'SearchField':'elstatid2011', 'OnlyAdd':False, 'perYearData':False}
        ]

    }
