import streamlit as st
import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot as plt

st.header('COVID-19 Dashboard Portugal')
#st.caption('Atualizado em 15/1/2022')
#DATA_URL = ('./deputados.csv')
CASOS_URL = ('https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv')
TESTES_URL = ('https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/amostras.csv')
VAXX_URL = ('https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/vacinas_detalhe.csv')
@st.cache
def load_data():
    case_info = pd.read_csv(CASOS_URL)
    test_info= pd.read_csv(TESTES_URL)
    vaxx_info = pd.read_csv(VAXX_URL)
    return case_info, test_info, vaxx_info

data_load_state = st.text('Loading data...')
df_portugal, amostras, vacinas_detalhe = load_data()
data_load_state.text('Loading data... done!')
df_portugal_all = df_portugal.copy()
testes = amostras.copy()
df_portugal_all['data'] = pd.to_datetime(df_portugal_all['data'], format='%d-%m-%Y')
df_portugal_all['weekday'] = ((df_portugal_all['data'].dt.dayofweek)).astype('category')
df_portugal_all['month_year'] = df_portugal_all['data']#.dt.to_period('M')
#st.write(df_portugal_all.columns.values)
df_portugal_all['obitos_novos'] = df_portugal_all['obitos'].diff()
df_portugal_all = df_portugal_all.set_index('data')

populacao_pt = (vacinas_detalhe['doses1']/vacinas_detalhe['doses1_perc'])[0]/100
pop_lvt = vacinas_detalhe['populacao1_arslvt'].max()
pop_norte = vacinas_detalhe['populacao1_arsnorte'].max()
pop_centro = vacinas_detalhe['populacao1_arscentro'].max()
pop_alentejo = vacinas_detalhe['populacao1_arsalentejo'].max()
pop_algarve = vacinas_detalhe['populacao1_arsalgarve'].max()
pop_madeira = vacinas_detalhe['populacao1_madeira'].max()
pop_acores = vacinas_detalhe['populacao1_açores'].max()
pop_outras = vacinas_detalhe['populacao1_arscentro'].max()+vacinas_detalhe['populacao1_arsalentejo'].max()+\
                      vacinas_detalhe['populacao1_arsalgarve'].max()
pop_ilhas = vacinas_detalhe['populacao1_açores'].max()+vacinas_detalhe['populacao1_madeira'].max()
pop_pais_sem_lvt = 100*populacao_pt.astype(int) - pop_lvt


df_portugal_all['confirmados_outrascontinente'] = df_portugal_all['confirmados_arscentro'] + \
df_portugal_all['confirmados_arsalentejo'] + df_portugal_all['confirmados_arsalgarve']

df_portugal_all['confirmados_ilhas'] = df_portugal_all['confirmados_madeira'] + df_portugal_all['confirmados_acores']

df_portugal_all['pais_sem_lvt'] = df_portugal_all['confirmados'] - df_portugal_all['confirmados_arslvt']
df_portugal_all['obitos_pais_sem_lvt'] = df_portugal_all['obitos'] - df_portugal_all['obitos_arslvt']


df_portugal_all['obitos_outrascontinente'] = df_portugal_all['obitos_arscentro'] + \
df_portugal_all['obitos_arsalentejo'] + df_portugal_all['obitos_arsalgarve']

df_portugal_all['obitos_ilhas'] = df_portugal_all['obitos_madeira'] + df_portugal_all['obitos_acores']

df_portugal_all['incidencia_14d'] = 1000*df_portugal_all['confirmados_novos'].rolling(window=14).sum()/populacao_pt
df_portugal_all['incidencia_14d_lvt'] = 100000*df_portugal_all['confirmados_arslvt'].diff().rolling(window=14).sum()/pop_lvt
df_portugal_all['incidencia_14d_norte'] = 100000*df_portugal_all['confirmados_arsnorte'].diff().rolling(window=14).sum()/pop_norte
df_portugal_all['incidencia_14d_centro'] = 100000*df_portugal_all['confirmados_arscentro'].diff().rolling(window=14).sum()/pop_centro
df_portugal_all['incidencia_14d_alentejo'] = 100000*df_portugal_all['confirmados_arsalentejo'].diff().rolling(window=14).sum()/pop_alentejo
df_portugal_all['incidencia_14d_algarve'] = 100000*df_portugal_all['confirmados_arsalgarve'].diff().rolling(window=14).sum()/pop_algarve
df_portugal_all['incidencia_14d_madeira'] = 100000*df_portugal_all['confirmados_madeira'].diff().rolling(window=14).sum()/pop_madeira
df_portugal_all['incidencia_14d_acores'] = 100000*df_portugal_all['confirmados_acores'].diff().rolling(window=14).sum()/pop_acores

df_portugal_all['incidencia_14d_outrascontinente'] = 100000*df_portugal_all['confirmados_outrascontinente'].diff().rolling(window=14).sum()/pop_outras
df_portugal_all['incidencia_14d_ilhas'] = 100000*df_portugal_all['confirmados_ilhas'].diff().rolling(window=14).sum()/pop_ilhas
df_portugal_all['incidencia_14d_pais_sem_lvt'] = 100000*df_portugal_all['pais_sem_lvt'].diff().rolling(window=14).sum()/pop_pais_sem_lvt

df_portugal_all['incidencia_ob_14d'] = 1000*df_portugal_all['obitos_novos'].rolling(window=14).sum()/populacao_pt
df_portugal_all['incidencia_ob_14d_lvt'] = 100000*df_portugal_all['obitos_arslvt'].diff().rolling(window=14).sum()/pop_lvt
df_portugal_all['incidencia_ob_14d_norte'] = 100000*df_portugal_all['obitos_arsnorte'].diff().rolling(window=14).sum()/pop_norte
df_portugal_all['incidencia_ob_14d_centro'] = 100000*df_portugal_all['obitos_arscentro'].diff().rolling(window=14).sum()/pop_centro
df_portugal_all['incidencia_ob_14d_alentejo'] = 100000*df_portugal_all['obitos_arsalentejo'].diff().rolling(window=14).sum()/pop_alentejo
df_portugal_all['incidencia_ob_14d_algarve'] = 100000*df_portugal_all['obitos_arsalgarve'].diff().rolling(window=14).sum()/pop_algarve
df_portugal_all['incidencia_ob_14d_madeira'] = 100000*df_portugal_all['obitos_madeira'].diff().rolling(window=14).sum()/pop_madeira
df_portugal_all['incidencia_ob_14d_acores'] = 100000*df_portugal_all['obitos_acores'].diff().rolling(window=14).sum()/pop_acores

df_portugal_all['incidencia_14d_ob_outrascontinente'] = 100000*df_portugal_all['obitos_outrascontinente'].diff().rolling(window=14).sum()/pop_outras
df_portugal_all['incidencia_14d_ob_ilhas'] = 100000*df_portugal_all['obitos_ilhas'].diff().rolling(window=14).sum()/pop_ilhas

df_portugal_all['Rt'] = df_portugal_all[['confirmados']].diff(7) / (df_portugal_all[['confirmados']].diff(11) - 
                                                                    df_portugal_all[['confirmados']].diff(4)  )

df_portugal_all['Rt_lvt'] = df_portugal_all[['confirmados_arslvt']].diff(7) / (df_portugal_all[['confirmados_arslvt']].diff(11) - 
                                                                    df_portugal_all[['confirmados_arslvt']].diff(4)  )
df_portugal_all['Rt_centro'] = df_portugal_all[['confirmados_arscentro']].diff(7) / (df_portugal_all[['confirmados_arscentro']].diff(11) - 
                                                                    df_portugal_all[['confirmados_arscentro']].diff(4)  )
df_portugal_all['Rt_norte'] = df_portugal_all[['confirmados_arsnorte']].diff(7) / (df_portugal_all[['confirmados_arsnorte']].diff(11) - 
                                                                    df_portugal_all[['confirmados_arsnorte']].diff(4)  )
df_portugal_all['Rt_alentejo'] = df_portugal_all[['confirmados_arsalentejo']].diff(7) / (df_portugal_all[['confirmados_arsalentejo']].diff(11) - 
                                                                    df_portugal_all[['confirmados_arsalentejo']].diff(4)  )
df_portugal_all['Rt_algarve'] = df_portugal_all[['confirmados_arsalgarve']].diff(7) / (df_portugal_all[['confirmados_arsalgarve']].diff(11) - 
                                                                    df_portugal_all[['confirmados_arsalgarve']].diff(4)  )
df_portugal_all['Rt_madeira'] = df_portugal_all[['confirmados_madeira']].diff(7) / (df_portugal_all[['confirmados_madeira']].diff(11) - 
                                                                    df_portugal_all[['confirmados_madeira']].diff(4)  )
df_portugal_all['Rt_acores'] = df_portugal_all[['confirmados_acores']].diff(7) / (df_portugal_all[['confirmados_acores']].diff(11) - 
                                                                    df_portugal_all[['confirmados_acores']].diff(4)  )
df_portugal_all['Rt_outrascontinente'] = df_portugal_all[['confirmados_outrascontinente']].diff(7) / (df_portugal_all[['confirmados_outrascontinente']].diff(11) - 
                                                                    df_portugal_all[['confirmados_outrascontinente']].diff(4)  )
df_portugal_all['Rt_ilhas'] = df_portugal_all[['confirmados_ilhas']].diff(7) / (df_portugal_all[['confirmados_ilhas']].diff(11) - 
                                                                    df_portugal_all[['confirmados_ilhas']].diff(4)  )
df_portugal_all['Rt_smooth'] = df_portugal_all['Rt'].rolling(window=7).mean()
df_portugal_all['Rt_lvt_smooth'] = df_portugal_all['Rt_lvt'].rolling(window=7).mean()
df_portugal_all['Rt_norte_smooth'] = df_portugal_all['Rt_norte'].rolling(window=7).mean()
df_portugal_all['Rt_centro_smooth'] = df_portugal_all['Rt_centro'].rolling(window=7).mean()
df_portugal_all['Rt_alentejo_smooth'] = df_portugal_all['Rt_alentejo'].rolling(window=7).mean()
df_portugal_all['Rt_algarve_smooth'] = df_portugal_all['Rt_algarve'].rolling(window=7).mean()
df_portugal_all['Rt_madeira_smooth'] = df_portugal_all['Rt_madeira'].rolling(window=7).mean()
df_portugal_all['Rt_acores_smooth'] = df_portugal_all['Rt_acores'].rolling(window=7).mean()
df_portugal_all['Rt_outrascontinente_smooth'] = df_portugal_all['Rt_outrascontinente'].rolling(window=7).mean()
df_portugal_all['Rt_ilhas_smooth'] = df_portugal_all['Rt_ilhas'].rolling(window=7).mean()

df_portugal_all['Rt_pais_sem_lvt'] = df_portugal_all[['pais_sem_lvt']].diff(7) / (df_portugal_all[['pais_sem_lvt']].diff(11) - 
                                                                    df_portugal_all[['pais_sem_lvt']].diff(4)  )

df_portugal_all['Rt_pais_sem_lvt_smooth'] = df_portugal_all['Rt_pais_sem_lvt'].rolling(window=7).mean()

ars_dic = {'_lvt':'Lisboa e Vale do Tejo',
'_norte':'Norte',
'_centro':'Centro',
'_alentejo':'Alentejo',
'_algarve':'Algarve',
'_madeira':'Madeira',
'_acores':'Açores',
        }

ars_dic2 = {'_lvt':'arslvt',
'_norte':'arsnorte',
'_centro':'arscentro',
'_alentejo':'arsalentejo',
'_algarve':'arsalgarve',
'_madeira':'madeira',
'_acores':'acores',
        }

## PROCESSAMENTO TESTAGEM

testes['data'] = pd.to_datetime(testes['data'], format='%d-%m-%Y')
testes['month_year'] = testes['data']#.dt.to_period('D')
testes = testes.set_index('data')
testes = testes.join(df_portugal_all['confirmados'])
testes['confirmados_novos'] = testes['confirmados'].diff()
testes['positividade'] = 100*testes['confirmados_novos']/testes['amostras_novas']
testes['amostras_novas_mm7d'] = testes['amostras_novas'].rolling(window=7).mean()
testes['amostras_pcr_novas_mm7d'] = testes['amostras_pcr_novas'].rolling(window=7).mean()
testes['amostras_antigenio_novas_mm7d'] = testes['amostras_antigenio_novas'].rolling(window=7).mean()
testes['incidencia_14d'] = 1000*testes['confirmados_novos'].rolling(window=14).sum()/populacao_pt

testes['amostras_novas_mm14d'] = testes['amostras_novas'].rolling(window=14).mean()
testes['confirmados_novos_mm7d'] = testes['confirmados_novos'].rolling(window=7).mean()
testes['positividade_mm7d'] = 100*(testes['confirmados_novos'].rolling(window=7).sum())/(testes['amostras_novas'].rolling(window=7).sum())
testes['positividade_mm14d'] = 100*(testes['confirmados_novos'].rolling(window=14).sum())/(testes['amostras_novas'].rolling(window=14).sum())

#fig, ax = plt.subplots()
#df_portugal_all[['confirmados']].diff().rolling(window=7).mean().plot(figsize=(18,10), fig=fig, ax=ax, linewidth=3)
#plt.grid(linewidth=0.1)
#plt.xticks(fontsize=14)
#plt.yticks(fontsize=14)
#plt.title('Casos confirmados: média móvel 7 dias', fontsize=14)
#st.pyplot(fig)


add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Quadro Geral", "Informação ARS", "Gráficos", 'Comparação entre diferentes datas')
)

if add_selectbox == "Quadro Geral":

    st.subheader("Casos, Óbitos e Transmissibilidade")
    st.caption("Atualizado em: "+ df_portugal_all.index[-1].strftime('%d/%m/%Y'))
    col1, col2, col3 = st.columns(3)
    col1.metric('Casos confirmados no dia',  str("{:,.0f}".format(df_portugal_all['confirmados_novos'][-1])), \
                "")
    col2.metric('Óbitos confirmados no dia',str("{:,.0f}".format(df_portugal_all['obitos_novos'][-1])), \
                "")
    col3.metric('Casos ativos',str("{:,.0f}".format(df_portugal_all['ativos'][-1])), \
                str("{:,.0f}".format(df_portugal_all['ativos'].diff()[-1])))

    col1, col2, col3 = st.columns(3)

    col1.metric('Casos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all['incidencia_14d'][-1])), \
                str("{:,.1f}".format(df_portugal_all['incidencia_14d'].diff()[-1])))
    col2.metric('Óbitos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all['incidencia_ob_14d'][-1])), \
                str("{:,.1f}".format(df_portugal_all['incidencia_ob_14d'].diff()[-1])))
    #col3.metric('Hospitalizados', df_portugal_all['internados'][-1].astype(int), \
    #            int(df_portugal_all['internados'].diff()[-1]))
    col3.metric('Rt estimado', round(df_portugal_all['Rt_smooth'][-1],2), \
                round(df_portugal_all['Rt_smooth'].diff()[-1],2))
    st.caption('Taxas de incidência por 100 mil habitantes')
    st.subheader("Hospitalizações")

    col1, col2, col3 = st.columns(3)

    col1.metric('Hospitalizações', str("{:,.0f}".format(df_portugal_all['internados'][-1])), \
                str("{:,.0f}".format(df_portugal_all['internados'].diff()[-1])))
    col2.metric('UCI', df_portugal_all['internados_uci'][-1].astype(int), \
                int(df_portugal_all['internados_uci'].diff()[-1]))

    st.subheader("Testagem")
    st.caption("Atualizado em: "+ testes.index[-1].strftime('%d/%m/%Y'))

    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total:', str("{:,.0f}".format(testes['amostras_novas_mm7d'][-1])), \
                str("{:,.0f}".format(testes['amostras_novas_mm7d'].diff()[-1])))
    col2.metric('PCR:', str("{:,.0f}".format(testes['amostras_pcr_novas_mm7d'][-1])), \
                str("{:,.0f}".format(testes['amostras_pcr_novas_mm7d'].diff()[-1])))
    col3.metric('Antigénio:', str("{:,.0f}".format(testes['amostras_antigenio_novas_mm7d'][-1])), \
                str("{:,.0f}".format(testes['amostras_antigenio_novas_mm7d'].diff()[-1])))
    col4.metric('Positividade:', str("{:,.2f}".format(testes['positividade_mm7d'][-1]))+"%", \
                str("{:,.2f}".format(testes['positividade_mm7d'].diff()[-1])))
    st.caption('Os valores referentes a testagem são a média móvel de 7 dias')
    st.caption('Fonte dos dados: Data Science for Social Good Portugal - ' + 'https://github.com/dssg-pt/covid19pt-data')

if add_selectbox == "Informação ARS":
    st.caption("Atualizado em: "+ df_portugal_all.index[-1].strftime('%d/%m/%Y'))
    for ars in ['_lvt', '_norte', '_centro', '_alentejo', '_algarve', '_madeira', '_acores']:
        st.subheader("ARS "+ars_dic[ars])

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric('Casos novos',  str("{:,.0f}".format(df_portugal_all['confirmados_'+ars_dic2[ars]].diff()[-1])), \
                    "")
        col2.metric('Incidência 14 dias',  str("{:,.1f}".format(df_portugal_all['incidencia_14d'+ars][-1])), \
                    str("{:,.1f}".format(df_portugal_all['incidencia_14d'+ars].diff()[-1])))
        col3.metric('Óbitos novos',  str("{:,.0f}".format(df_portugal_all['obitos_'+ars_dic2[ars]].diff()[-1])), \
                    "")
        col4.metric('Incidência 14 dias',  str("{:,.1f}".format(df_portugal_all['incidencia_ob_14d'+ars][-1])), \
                    str("{:,.1f}".format(df_portugal_all['incidencia_ob_14d'+ars].diff()[-1])))
        #col3.metric('Hospitalizados', df_portugal_all['internados'][-1].astype(int), \
        #            int(df_portugal_all['internados'].diff()[-1]))
        col5.metric('Rt estimado', round(df_portugal_all['Rt'+ars+'_smooth'][-1],2), \
                    round(df_portugal_all['Rt'+ars+'_smooth'].diff()[-1],2))
    
    st.caption('Taxas de incidência por 100 mil habitantes')
   



if add_selectbox == "Gráficos":

    st.subheader("Hospitalizações vs Incidência a 14 dias")


    st.vega_lite_chart(df_portugal_all, {
     'width': 800,
     'height': 500,
     #'xlabel':'Internados',
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'incidencia_14d', "format": ".1f",'type': 'quantitative', 'title': 'Incidência 14 dias (por 100 mil hab)'},
         'y': {'field': 'internados', 'type': 'quantitative', 'title': 'Numero de pacientes hospitalizados'},
         #'size': {'field': 'c', 'type': 'quantitative'},
         'color': {'field': 'month_year', 'type': 'temporal', "scale": {"range": ["lightgray", "black"]}},
     },
 })

    st.subheader("Hospitalizações UCI vs Incidência a 14 dias")

    st.vega_lite_chart(df_portugal_all, {
     'width': 800,
     'height': 500,
     #'xlabel':'Internados',
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'incidencia_14d', "format": ".1f", 'type': 'quantitative', 
        "axis": {"labelAngle": 0, "labelOverlap": "parity"}, 'title': 'Incidência 14 dias (por 100 mil hab)'},
         'y': {'field': 'internados_uci', 'type': 'quantitative', 'title': 'Numero de pacientes hospitalizados em UCI'},
         #'size': {'field': 'c', 'type': 'quantitative'},
         'color': {'field': 'month_year', 'type': 'temporal', "scale": {"range": ["lightgray", "black"]}},
     },
 })

    st.subheader("Positividade 14 dias vs Incidência a 14 dias")

    st.vega_lite_chart(testes, {
     'width': 800,
     'height': 500,
     #'xlabel':'Internados',
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'incidencia_14d', "format": ".1f", 'type': 'quantitative', 
        "axis": {"labelAngle": 0, "labelOverlap": "parity"}, 'title': 'Incidência 14 dias (por 100 mil hab)'},
         'y': {'field': 'positividade_mm14d', "format": ".1f", 'type': 'quantitative', 'title': 'Positividade 14 dias'},
         #'size': {'field': 'c', 'type': 'quantitative'},
         'color': {'field': 'month_year', 'type': 'temporal', "scale": {"range": ["lightgray", "black"]}},
     },
 })

if add_selectbox == "Comparação entre diferentes datas":

    col1, col2 = st.columns(2)
    d1 = col1.date_input(
     "Escolha a primeira data",
     datetime.date.today()+datetime.timedelta(days=-1), 
     min_value=datetime.date(2020,3,16),
     max_value=df_portugal_all.index[-1])

    d2 = col2.date_input(
     "Escolha a segunda data",
     datetime.date.today()+datetime.timedelta(days=-365))
    d1 = d1.strftime("%Y-%m-%d")
    col1.metric('Casos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all.loc[d1,'incidencia_14d'])), \
                "")
    col1.metric('Óbitos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all.loc[d1,'incidencia_ob_14d'])), \
                "")
    col1.metric('Casos ativos',  str("{:,.0f}".format(df_portugal_all.loc[d1,'ativos'])), \
                "")
    col1.metric('Hospitalizados',  str("{:,.0f}".format(df_portugal_all.loc[d1,'internados'])), \
                "")
    col1.metric('UCI',  str("{:,.0f}".format(df_portugal_all.loc[d1,'internados_uci'])), \
                "")
    if d1 not in testes.index:
        d1 = testes.index[-1]
        col1.metric('Testes efetuados (média 7d)',  str("{:,.0f}".format(testes.loc[d1,'amostras_novas_mm7d'])), \
                "")
        col1.metric('Positividade (média 7d)',  str("{:,.2f}".format(testes.loc[d1,'positividade_mm7d'])+'%'), \
                "")
        st.caption('Dados de testagem referentes a '+d1.strftime("%Y-%m-%d"))
    else:
        col1.metric('Testes efetuados (média 7d)',  str("{:,.0f}".format(testes.loc[d1,'amostras_novas_mm7d'])), \
                "")
        col1.metric('Positividade (média 7d)',  str("{:,.2f}".format(testes.loc[d1,'positividade_mm7d'])+'%'), \
                "")
     
    d2 = d2.strftime("%Y-%m-%d")   
    col2.metric('Casos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all.loc[d2,'incidencia_14d'])), \
                "")
    col2.metric('Óbitos: incidencia 14 dias',  str("{:,.1f}".format(df_portugal_all.loc[d2,'incidencia_ob_14d'])), \
                "")
    col2.metric('Casos ativos',  str("{:,.0f}".format(df_portugal_all.loc[d2,'ativos'])), \
                "")

    col2.metric('Hospitalizados',  str("{:,.0f}".format(df_portugal_all.loc[d2,'internados'])), \
                "")
    col2.metric('UCI',  str("{:,.0f}".format(df_portugal_all.loc[d2,'internados_uci'])), \
                "")
    
    if d2 not in testes.index:
        d2 = testes.index[-1]
        col2.metric('Testes efetuados (média 7d)',  str("{:,.0f}".format(testes.loc[d2,'amostras_novas_mm7d'])), \
                "")
        col2.metric('Positividade (média 7d)',  str("{:,.2f}".format(testes.loc[d2,'positividade_mm7d'])+'%'), \
                "")
        st.caption('Dados de testagem referentes a '+d2.strftime("%Y-%m-%d"))
    else:
        col2.metric('Testes efetuados (média 7d)',  str("{:,.0f}".format(testes.loc[d2,'amostras_novas_mm7d'])), \
                "")
        col2.metric('Positividade (média 7d)',  str("{:,.2f}".format(testes.loc[d2,'positividade_mm7d'])+'%'), \
                "")



