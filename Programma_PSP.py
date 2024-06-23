import streamlit as st
import pandas as pd
import pyodbc
import csv
import subprocess
import mysql.connector
import os #Libreria per ottenere la directory di lavoro

def connessione():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user= "root",
            password= "Francesco2003gg!",
            database= "fattoria"
        )
        return conn
    except mysql.connector.Error as errore:
        return None
    

def esegui_query(q):
    cursor.execute(q)
    ris = cursor.fetchall()
    column_names = cursor.column_names
    df = pd.DataFrame(ris, columns=column_names)
    if not ris:
        st.write('Risultato non trovato')
    else:
        st.dataframe(df)
    return None


query_soluzione_1 = 'set sql_safe_updates = 0;'
   
query_soluzione_2 = '''
update dati_galline_1
set g_salute = 'Cattiva'
where g_salute != 'Pessima' and g_Salute != 'cattiva' and( g_peso BETWEEN 1.2  AND 1.2975 or g_peso BETWEEN 1.70 AND 1.8 );'''

query_soluzione_3 ='''
update dati_galline_1
set g_salute = 'Pessima'
where g_salute != 'Pessima' and g_Salute != 'cattiva' and( g_peso < 1.2 or g_peso  > 1.8 );'''

qqq = "SELECT GallinaiD,data1, g_peso, g_salute from dati_galline_1 where g_salute != 'Pessima' and g_Salute != 'cattiva' and( g_peso < 1.2975 or g_peso > 1.70);"

###############################################################################

st.title('Analisi fattoria')
st.write('_By PSP_')


conn = connessione()

if conn:
    cursor = conn.cursor()
    file_to_upload = st.file_uploader("##### Caricare file SQL")
    if file_to_upload is not None:
        dati = file_to_upload.read().decode("utf-8") # Leggere il file SQL come stringa
        queries = dati.split(";")
        for query in queries:
            if query.strip():
                try:
                    cursor.execute(query)
                except:
                    st.write(query)           #Che query da problemi
                    cursor.execute(query)     #Che problema da
                    break                     #fermare esecuzione
        st.write('Import effettuato con successo')

        st.write('---------------------------------')

        st.write('''È necessario risolvere il problema del calcolo nella salute delle galline, premere il pulsante
                 che si trova di seguito per sostituire gli errori con le situazioni corrette''')
        b = st.button('Risoluzione')
        if b:
            cursor.execute(query_soluzione_1)
            cursor.execute(query_soluzione_2)
            cursor.execute(query_soluzione_3)
            st.write('Problemi risolti')
        
        st.write('---------------------------------')

        st.write('## _Scelta opzioni animali_')
        
        date_to_choose = ['2010-01-01','2010-04-01','2010-07-01','2010-10-01',
                          '2011-01-01','2011-04-01','2011-07-01','2011-10-01',
                          '2012-01-01','2012-04-01','2012-07-01','2012-10-01',
                          '2013-01-01','2013-04-01','2013-07-01','2013-10-01',
                          '2014-01-01','2014-04-01','2014-07-01','2014-10-01',
                          '2015-01-01','2015-04-01','2015-07-01','2015-10-01',
                          '2016-01-01','2016-04-01','2016-07-01','2016-10-01',
                          '2017-01-01','2017-04-01','2017-07-01','2017-10-01',
                          '2018-01-01','2018-04-01','2018-07-01','2018-10-01',
                          '2019-01-01','2019-04-01','2019-07-01','2019-10-01',
                          '2020-01-01','2020-04-01','2020-07-01','2020-10-01',
                          '2021-01-01','2021-04-01','2021-07-01','2021-10-01',
                          '2022-01-01','2022-04-01','2022-07-01','2022-10-01',
                          '2023-01-01','2023-04-01','2023-07-01','2023-10-01']

        animali = ['Gallina','Mucca','Pecora','Capra','Cavallo']


        data_scelta = st.selectbox('#### Selezionare una data',date_to_choose)
        animale_scelta = st.selectbox('#### Selezionare un animale',animali)
        stato_scelto = st.selectbox('#### Selezionare uno stato di salute', ['Pessima','Cattiva','Normale','Buona','Eccellente'])


        if (animale_scelta == 'Gallina'):
            id_scelta = 'GallinaID'
        if (animale_scelta == 'Mucca'):
            id_scelta = 'MuccaID'
        if (animale_scelta == 'Pecora'):
            id_scelta = 'PecoreID'
        if (animale_scelta == 'Capra'):
            id_scelta = 'CapreID'
        if (animale_scelta == 'Cavallo'):
            id_scelta = 'CavalliID'

        Eta_scelta    = animale_scelta[0] + '_Eta' if (animale_scelta != 'Cavallo') else 'H_Eta'
        Peso_scelta   = animale_scelta[0] + '_Peso' if (animale_scelta != 'Cavallo') else 'H_Peso'
        Razza_scelta  = animale_scelta[0] + '_Razza' if (animale_scelta != 'Cavallo') else 'H_Razza'
        Colore_scelta = animale_scelta[0] + '_Colore' if (animale_scelta != 'Cavallo') else 'H_Colore'
        Born_scelta   = animale_scelta[0] + '_Data_nascita' if (animale_scelta != 'Cavallo') else 'H_Data_nascita'
        Salute_scelta = animale_scelta[0] + '_Salute' if (animale_scelta != 'Cavallo') else 'H_Salute'
        
        if (animale_scelta == 'Gallina'):
            dati_scelti = 'dati_galline_1'
        if (animale_scelta == 'Mucca'):
            dati_scelti = 'dati_mucche_1'
        if (animale_scelta == 'Pecora'):
            dati_scelti = 'dati_pecore_1'
        if (animale_scelta == 'Capra'):
            dati_scelti = 'dati_capre_1'
        if (animale_scelta == 'Cavallo'):
            dati_scelti = 'dati_cavalli_1'

        st.write('---------------------------------')
        st.write('### Query sugli animali')
        q1 = st.button('Animali per razza in data specifica')
        if q1:
            esegui_query(f'SELECT {Razza_scelta}, COUNT(DISTINCT {id_scelta}) as NumeroAnimale FROM {dati_scelti} where data1 = \'{data_scelta}\' GROUP BY {Razza_scelta};')


        q2 = st.button('Calcolare il peso medio di una tipologia di animali in una data')
        if q2:
            esegui_query(f'SELECT Round(AVG({Peso_scelta}),2) AS Peso_medio FROM {dati_scelti} where Data1 = \'{data_scelta}\';')


        q3 = st.button('Vedere la razza più diffusa di un animale in una determinata data')
        if q3:
            esegui_query(f'''select {Razza_scelta} AS Razza_più_diffusa from {dati_scelti} group by {Razza_scelta} HAVING COUNT({Razza_scelta}) = (
                            SELECT max(conto) FROM ( SELECT COUNT({Razza_scelta})  as conto FROM {dati_scelti} group by {Razza_scelta}) as t);''')
            
        
        q4 = st.button('Selezione di animali in base a condizioni di salute specifiche')
        if q4:
            esegui_query(f'''SELECT Data1, {Salute_scelta} as Salute,COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE {Salute_scelta} = \'{stato_scelto}\' and 
                         Data1 = \'{data_scelta}\' GROUP BY {Salute_scelta};''')
            
        
        q5 = st.button('Vedere in un determinato giorno quanti animali hanno una determinata età')
        if q5:
            esegui_query(f'''SELECT {Eta_scelta}, COUNT(DISTINCT {id_scelta}) AS NumeroGalline FROM {dati_scelti} WHERE Data1 = \'{data_scelta}\'  GROUP BY {Eta_scelta} asc;''')


        lb = st.slider('Seleziona il valore minimo d\'età (È gestito anche il caso in cui il minimo sia maggiore del massimo)',1,10,1)
        ub = st.slider('Seleziona il valore massimo d\'età (È gestito anche il caso in cui il minimo sia maggiore del massimo)',1,10,1)
        if lb > ub:
            lb,ub = ub,lb
        stagione = st.selectbox('Selezionare la stagione',['Inverno','Primavera','Estate','Autunno'])
        q6 = st.button('Selezione di tutti gli animali con età compresa tra i precedenti  anni e nati in una precisa stagione in una determinata data')
        if q6:
            if stagione == 'Inverno':
                esegui_query(f'''SELECT month({Born_scelta}) as mese_nascita,COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE {Eta_scelta} >= {lb} AND {Eta_scelta} <= {ub} and month({Born_scelta}) in (1,2,12) 
                                 and data1 = \'{data_scelta}\' group by mese_nascita;''')
            if stagione == 'Primavera':
                esegui_query(f'''SELECT month({Born_scelta}) as mese_nascita,COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE {Eta_scelta} >= {lb} AND {Eta_scelta} <= {ub} and month({Born_scelta}) in (3,4,5) 
                                and data1 = \'{data_scelta}\' group by mese_nascita;''')
            if stagione == 'Estate':
                esegui_query(f'''SELECT month({Born_scelta}) as mese_nascita,COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE {Eta_scelta} >= {lb} AND {Eta_scelta} <= {ub} and month({Born_scelta}) in (6,7,8) 
                                and data1 = \'{data_scelta}\' group by mese_nascita;''')
            if stagione == 'Autunno':
                esegui_query(f'''SELECT month({Born_scelta}) as mese_nascita,COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE {Eta_scelta} >= {lb} AND {Eta_scelta} <= {ub} and month({Born_scelta}) in (9,10,11) 
                                and data1 = \'{data_scelta}\' group by mese_nascita;''')
        

        razze = ['Gallina Livornese','Gallina Padovana','Gallina Bianca Italiana','Gallina di Polverara','Gallina Rossa Italiana','Gallina Mostra di Oltremare','Gallina Siciliana']
        razza_ = st.select_slider('Scegli la razza',razze)
        q7 = st.button('Selezione delle galline in base alla razza')
        if q7:
            esegui_query(f'''select data1, count(distinct gallinaID) as NumeroAnimale, g_razza from dati_galline_1 where g_razza = '{razza_}' and data1 = \'{data_scelta}\' group by g_razza;''')


        q8 = st.button('Calcolare l’eta media in una determinatà data')
        if q8:
            esegui_query(f'''SELECT data1, Round(AVG({Eta_scelta}),4) as Età_Media, COUNT(DISTINCT {id_scelta}) AS NumeroAnimale FROM {dati_scelti} WHERE Data1 = \'{data_scelta}\' order by età_media asc;''')


        st.write('---------------------------------')
        st.write('## _Scelta opzioni monitoraggi ambientali_')
        data_scelta_c = st.selectbox('Selezionare una data per i monitoraggi',date_to_choose)
        temp_scelta = st.number_input('Selezionare la temperatura', min_value=-2.0, max_value=32.0, step=0.5)
        umid_scelta = st.number_input('Selezionare l’umidità', min_value=0.6, max_value=1.0, step=0.01)
        qual_scelta = st.number_input('Selezionare la qualtià del suolo', min_value=4.0, max_value=8.0, step=0.1)


        st.write('---------------------------------')
        st.write('### Query sull’ambiente')
        a1 = st.button('Selezione dati con valori superiori a quelli indicati',)
        if a1:
            esegui_query(f'''Select Data,Temperatura,Umidita,qualita_del_suolo from Dati_monitoraggio_1 where Temperatura >= {temp_scelta} and Umidita >= {umid_scelta} AND Qualita_del_Suolo >= {qual_scelta};''')
        

        a2 = st.button('Selezione di dati per un giorno preciso')
        if a2:
            esegui_query(f'''select * from dati_monitoraggio_1 where Data = \'{data_scelta_c}\'''')
        
        st.write('\n')
        st.write('\n')
        st.write('\n')
        
        data_1 = st.select_slider('Selezionare data minima',date_to_choose)
        data_2 = st.select_slider('Selezionare data massima',date_to_choose)
        if data_1 > data_2:
            data_1,data_2 = data_2,data_1
        a3 = st.button('Calcolo di temperatura media in un intervallo di tempo')
        if a3:
            esegui_query(f'''SELECT Round(AVG(Umidita),2)  AS Umidita_media , Round(AVG(Temperatura),2) as Temperatura_media, round(avg(Qualita_Del_suolo),2) as Qualitadelsuolomedia 
                            FROM Dati_monitoraggio_1 where Data between \'{data_1}\' and \'{data_2}\';''')
            
        
        a4 = st.button('Calcolo della temperatura massima per ogni estate e poi selezionare solo le prime 3')
        if a4:
            cursor.execute('''create or replace view Pino2(Temperatura,Mese, Anno) as select Temperatura, month(data) as mese , year(data) as Anno from dati_monitoraggio_1 where  month(data) between 6 and 8;''')
            esegui_query('''select Anno,mese,max(temperatura) as max_temp from Pino2 group by Anno, mese order by max_temp desc limit 3 ;''')


        a5 = st.button('Calcolo del numero di giorni con qualità del suolo superiore a un valore specifico')
        if a5:
            esegui_query(f'''select data, qualita_del_suolo from Dati_monitoraggio_1 where qualita_del_suolo >= {qual_scelta};''')

        
        a6 = st.button('Selezione di dati per giorni con temperature estreme (massima(>31) e minima(<4))')
        if a6:
            esegui_query(f'''SELECT MAX(Temperatura) AS Max_Temperatura, MIN(temperatura) as Min_temperatura, data as DATA FROM Dati_monitoraggio_1 
                            GROUP BY DATA HAVING Max_Temperatura > 31 OR Min_temperatura < 4 order by Min_Temperatura asc;''')
            
        st.write('\n')
        st.write('\n')
        st.write('\n')
        
        data_cj_min = st.select_slider('Selezionare data minima primo intervallo',date_to_choose)
        data_cj_max = st.select_slider('Selezionare data massima primo intervallo',date_to_choose)
        if data_cj_min > data_cj_max:
            data_cj_min,data_cj_max = data_cj_max,data_cj_min
        data_cj_min_2 = st.select_slider('Selezionare data minima secondo intervallo',date_to_choose)
        data_cj_max_2 = st.select_slider('Selezionare data massima secondo intervallo',date_to_choose)
        if data_cj_min_2 > data_cj_max_2:
            data_cj_min_2,data_cj_max_2 = data_cj_max_2,data_cj_min_2
        a7 = st.button('Confronto delle qualità del suolo medie tra due intervalli di date')
        if a7:
            esegui_query(f'''SELECT i1.Media_Qualita_Suolo AS Media_Qualita_Suolo_Intervallo_1,i2.Media_Qualita_Suolo AS Media_Qualita_Suolo_Intervallo_2
                            FROM (SELECT AVG(Qualita_Del_Suolo) AS Media_Qualita_Suolo FROM Dati_monitoraggio_1 WHERE Data BETWEEN \'{data_cj_min}\' AND \'{data_cj_max}\' AND Qualita_Del_Suolo > 3) i1
                            CROSS JOIN (SELECT AVG(Qualita_Del_Suolo) AS Media_Qualita_Suolo  FROM Dati_monitoraggio_1  WHERE Data BETWEEN \'{data_cj_min_2}\' AND \'{data_cj_max_2}\' AND Qualita_Del_Suolo > 3) i2;''')


        st.write('\n')
        st.write('\n')
        st.write('\n')

        data_cj_min_3 = st.select_slider('Selezionare data minima primo intervallo ',date_to_choose)
        data_cj_max_3 = st.select_slider('Selezionare data massima primo intervallo ',date_to_choose)
        if data_cj_min_3 > data_cj_max_3:
            data_cj_min_3,data_cj_max_3 = data_cj_max_3,data_cj_min_3
        data_cj_min_4 = st.select_slider('Selezionare data minima secondo intervallo ',date_to_choose)
        data_cj_max_4 = st.select_slider('Selezionare data massima secondo intervallo ',date_to_choose)
        if data_cj_min_4 > data_cj_max_4:
            data_cj_min_4,data_cj_max_4 = data_cj_max_4,data_cj_min_4
        a8 = st.button('Confronto delle umidità medie tra due intervalli di date') 
        if a8:
            esegui_query(f'''SELECT i1.Media_umidita AS Media_umidita_1,i2.Media_umidita AS Media_umidita_2 FROM 
                            (SELECT AVG(umidita) AS Media_umidita FROM Dati_monitoraggio_1 WHERE Data BETWEEN \'{data_cj_min_3}\' AND \'{data_cj_max_3}\' AND umidita > 0.4) i1 CROSS JOIN 
                            (SELECT AVG(umidita) AS Media_umidita FROM Dati_monitoraggio_1 WHERE Data BETWEEN \'{data_cj_min_4}\' AND \'{data_cj_max_4}\' AND umidita > 0.4) i2;''')
            
        
        st.write('---------------------------------')
        st.write('### Query sulle spese')

        s1 = st.button('Calcolo della spesa media per ogni mese e vedere il mese in cui spendiamo di piu')
        if s1:
            esegui_query('''select month(data) as MESE,YEAR(data) AS Anno, round(AVG(Spesa_totale),2)AS Spesa_Media_totale FROM dati_spesa_Animali_1 GROUP BY MESE, Anno ORDER BY Spesa_Media_totale desc;''')

        

        st.write('---------------------------------')
        st.write('## _Scelta opzioni colture_')
        coltura = st.selectbox('Selezionare la coltura',['Patate','Pomodori','Carote','Mais','Lattuga'])
        coltura_scelta_p = 'P_' + coltura #Produzione
        coltura_scelta_m = 'M_' + coltura #Metri dedicati
        anno_colture = st.selectbox('Selezionare una data per le colture',[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023])

        st.write('---------------------------------')
        st.write('### Query sulla coltura')

        c1 = st.button('Produzione colture per metro quadro')
        if c1:
            esegui_query(f'''select distinct p.Anno, round(p.{coltura_scelta_p} / o.{coltura_scelta_m}, 2) as Produzione_per_metroquadro 
                            from produzione_annua_1 as P inner join Organizzazione_campi_1 as O on P.anno = O.anno where p.anno = {anno_colture};''')
            

        
        minimo_c = st.select_slider('Scegliere la metratura desiderata',[300,600,900,1200])
        c2 = st.button('Anni in cui una determinata coltura ha una produzione specifica')
        if c2:
            esegui_query(f'''select * from organizzazione_campi_1 where {coltura_scelta_m} = {minimo_c};''')
        
        c3 = st.button('Anni in cui la produzione è maggiore della sua media')
        if c3:
            esegui_query(f'''SELECT anno, SUM({coltura_scelta_p}) AS Produzione FROM produzione_annua_1 GROUP BY anno
                            HAVING SUM({coltura_scelta_p}) > (SELECT AVG({coltura_scelta_p}) FROM produzione_annua_1)
                            ORDER BY Produzione desc;''')
            

        seconda_coltura = st.selectbox('Selezionare la seconda coltura',['Patate','Pomodori','Carote','Mais','Lattuga'])
        seconda_coltura_p = 'P_' + seconda_coltura
        c4 = st.button('Produzione media di due ortaggi da un anno in poi')
        if c4:
            esegui_query(f'''SELECT ROUND(AVG({coltura_scelta_p}),2) AS {coltura}, ROUND(AVG({seconda_coltura_p}),2) AS {seconda_coltura} FROM produzione_annua_1 WHERE Anno >= {anno_colture};''')
        
        st.write('Progetto eseguito da Francesco Picaro, Lorenzo Salerno, Rosario Pepe')
        
else:
    st.write('Problema durante la connessione a mysql')

        




    
        
        
    


    
    













#animale_scelto = st.selectbox('Scegli un animale',animali)







