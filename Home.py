import streamlit as st
import re
from ImportandoDados import BancoDados
from datetime import datetime,timedelta


bd = BancoDados()

st.set_page_config(layout='wide')
col1, col2, col3 = st.columns ([1, 2, 1])  
with col2:

  etiquetaID = st.text_input('Horario da etiqueta:',key='etiquetaID')
  etiquetaID = re.sub('\s{2,}',' ',etiquetaID)
  validacao = re.match('\d\d/\d\d/\d{4} \d{2}:\d{2}',etiquetaID)
  if not validacao:
    st.error('O valor deve está no formato de data e hora. Exemplo: 10/01/2002 16:34')

  skid = st.text_input('Número do carrinho:',key='skid')
  skid = re.sub('\s+','',skid)
  validacao = re.match('\d{1,3}',skid)
  if not validacao:
    st.error('Os valores do carrinhos tem ser númericos. Exemplo: 165')
  else:
    if not(int(skid)>=1 and int(skid)<=165):
      st.error('Os valores do carrinhos vão de 1 a 165. Exemplo: 100')
    
query_limite_entrada = f'''
  DECLARE @horario DATETIME;
  DECLARE @limite DATETIME;
  DECLARE @skid INT;  -- Declare a variável @skid

  -- Atribuindo os valores às variáveis
  SET @horario = CONVERT(DATETIME, '{etiquetaID}', 103);
  SET @skid = {skid};

  -- Query para buscar e atribuir o valor à variável @limite
  SET @limite = (
    SELECT TOP 1 [E3TimeStamp]
    FROM [p4_relatorio].[dbo].[RegistroSkid]
    WHERE E3TimeStamp <= @horario
      AND SaidaEstufa >= @horario
      AND Skid = @skid
    ORDER BY E3TimeStamp DESC
);

-- Retornar o valor da variável @limite (opcional)
SELECT @limite AS Limite; -- tem que ter esta linha para funcionar a função
'''
limite = bd.Get_Value(query_limite_entrada)

query_limite_saida = f'''
  DECLARE @horario DATETIME;
  DECLARE @limite DATETIME;
  DECLARE @skid INT;  -- Declare a variável @skid

  -- Atribuindo os valores às variáveis
  SET @horario = CONVERT(DATETIME, '{etiquetaID}', 103);
  SET @skid = {skid};

  -- Query para buscar e atribuir o valor à variável @limite
  SET @limite = (
    SELECT TOP 1 [SaidaEstufa]
    FROM [p4_relatorio].[dbo].[RegistroSkid]
    WHERE E3TimeStamp <= @horario
      AND SaidaEstufa >= @horario
      AND Skid = @skid
    ORDER BY E3TimeStamp DESC
);
-- Retornar o valor da variável @limite (opcional)
SELECT @limite AS Limite; -- tem que ter esta linha para funcionar a função
'''
limite_saida = bd.Get_Value(query_limite_saida)

query_limite_entrada_estufa = f'''
  DECLARE @horario DATETIME;
  DECLARE @limite DATETIME;
  DECLARE @skid INT;  -- Declare a variável @skid

  -- Atribuindo os valores às variáveis
  SET @horario = CONVERT(DATETIME, '{etiquetaID}', 103);
  SET @skid = {skid};

  -- Query para buscar e atribuir o valor à variável @limite
  SET @limite = (
    SELECT TOP 1 [EntraEStufa]
    FROM [p4_relatorio].[dbo].[RegistroSkid]
    WHERE E3TimeStamp <= @horario
      AND SaidaEstufa >= @horario
      AND Skid = @skid
    ORDER BY E3TimeStamp DESC
);
-- Retornar o valor da variável @limite (opcional)
SELECT @limite AS Limite; -- tem que ter esta linha para funcionar a função
'''
limite_entrada_estufa = bd.Get_Value(query_limite_entrada_estufa) #limite = horario que a peça entrou na cabine de pintura



if limite: #tratando as variaveis str para datetime
  delta = limite_saida- limite
  limite = datetime.strftime(limite,"%d/%m/%Y %H:%M") 
  limite_saida = datetime.strftime(limite_saida,"%d/%m/%Y %H:%M")
  limite_entrada_estufa = datetime.strftime(limite_entrada_estufa,"%d/%m/%Y %H:%M")
  st.write(f'Entrada no processo: {limite} --- Saída do processo: {limite_saida} --- total: {(delta.total_seconds()/60):.2f} minutos')

query_primer = f'''

  SELECT top(1) 
  format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Inicio Aplicação'
  ,format([FimAplicacao], 'dd/MM/yyyy HH:mm:ss') as 'Fim Aplicação'
  ,DATEDIFF(SECOND,E3TimeStamp,FimAplicacao) as Duração
  ,[Skid]
  ,[Giro]
  ,[Programa]
  ,[Material]
  ,[Temperatura]
  ,[Umidade]
    ,[Status]
  FROM [p4_relatorio].[dbo].[AplPRM]
  where E3TimeStamp >  CONVERT(DATETIME, '{limite}', 103)
  and E3TimeStamp < CONVERT(DATETIME, '{etiquetaID}', 103)
  and FimAplicacao < CONVERT(DATETIME, '{etiquetaID}', 103)
  and Skid = {skid}

'''
query_bc1 = f'''

  SELECT top(1) 
  format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Inicio Aplicação'
  ,format([FimAplicacao], 'dd/MM/yyyy HH:mm:ss') as 'Fim Aplicação'
  ,DATEDIFF(SECOND,E3TimeStamp,FimAplicacao) as Duração
  ,[Skid]
  ,[Giro]
  ,[Programa]
  ,[Material]
  ,[Temperatura]
  ,[Umidade]
    ,[Status]
  FROM [p4_relatorio].[dbo].[AplBC1]
  where E3TimeStamp >  CONVERT(DATETIME, '{limite}', 103)
  and E3TimeStamp < CONVERT(DATETIME, '{etiquetaID}', 103)
  and FimAplicacao < CONVERT(DATETIME, '{etiquetaID}', 103)
  and Skid = {skid}

'''
query_bc2 = f'''

  SELECT top(1) 
  format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Inicio Aplicação'
  ,format([FimAplicacao], 'dd/MM/yyyy HH:mm:ss') as 'Fim Aplicação'
  ,DATEDIFF(SECOND,E3TimeStamp,FimAplicacao) as Duração
  ,[Skid]
  ,[Giro]
  ,[Programa]
  ,[Material]
  ,[Temperatura]
  ,[Umidade]
    ,[Status]
  FROM [p4_relatorio].[dbo].[AplBC2]
  where E3TimeStamp >  CONVERT(DATETIME, '{limite}', 103)
  and E3TimeStamp < CONVERT(DATETIME, '{etiquetaID}', 103)
  and FimAplicacao < CONVERT(DATETIME, '{etiquetaID}', 103)
  and Skid = {skid}

'''
query_cc1 = f'''

  SELECT top(1) 
  format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Inicio Aplicação'
  ,format([FimAplicacao], 'dd/MM/yyyy HH:mm:ss') as 'Fim Aplicação'
  ,DATEDIFF(SECOND,E3TimeStamp,FimAplicacao) as Duração
  ,[Skid]
  ,[Giro]
  ,[Programa]
  ,[Material]
  ,[Temperatura]
  ,[Umidade]
    ,[Status]
  FROM [p4_relatorio].[dbo].[AplCC1]
  where E3TimeStamp >  CONVERT(DATETIME, '{limite}', 103)
  and E3TimeStamp < CONVERT(DATETIME, '{etiquetaID}', 103)
  and FimAplicacao < CONVERT(DATETIME, '{etiquetaID}', 103)
  and Skid = {skid}

'''
query_cc2 = f'''

  SELECT top(1) 
  format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Inicio Aplicação'
  ,format([FimAplicacao], 'dd/MM/yyyy HH:mm:ss') as 'Fim Aplicação'
  ,DATEDIFF(SECOND,E3TimeStamp,FimAplicacao) as Duração
  ,[Skid]
  ,[Giro]
  ,[Programa]
  ,[Material]
  ,[Temperatura]
  ,[Umidade]
    ,[Status]
  FROM [p4_relatorio].[dbo].[AplCC2]
  where E3TimeStamp >  CONVERT(DATETIME, '{limite}', 103)
  and E3TimeStamp < CONVERT(DATETIME, '{etiquetaID}', 103)
  and FimAplicacao < CONVERT(DATETIME, '{etiquetaID}', 103)
  and Skid = {skid}

'''


if limite:

  with st.container(border=True) as primer:
    df_primer = bd.Df_Query(query_primer)
    st.markdown('# Cabine Primer')
    st.markdown('## Robo 1')
    st.write(df_primer)
    if not df_primer.empty:
      st.write(bd.Query_Alarme(df_primer['Inicio Aplicação'].iloc[0],df_primer['Fim Aplicação'].iloc[0]))
    else:
      st.markdown('### _Aplicação Manual_')

  with st.container(border=True) as base:
    st.markdown('# Cabine Base')
    col1,col2 = st.columns(2)
    with col1:
      st.markdown('## Robô 1')
      df_bc1 = bd.Df_Query(query_bc1)
      st.write(df_bc1)  
      if not df_bc1.empty:
        st.write(bd.Query_Alarme(df_bc1['Inicio Aplicação'].iloc[0],df_bc1['Fim Aplicação'].iloc[0]))
      else:
        st.markdown('### _Aplicação Manual_')

    with col2:
      st.markdown('## Robô 2')
      df_bc2 = bd.Df_Query(query_bc2)
      st.write(df_bc2)
      if not df_bc2.empty:
        st.write(bd.Query_Alarme(df_bc2['Inicio Aplicação'].iloc[0],df_bc2['Fim Aplicação'].iloc[0]))
      else:
        st.markdown('### _Aplicação Manual_')

  with st.container(border=True) as verniz:
    st.markdown('# Cabine Verniz')
    col1,col2 = st.columns(2)

    with col1:
      st.markdown('## Robô 1')
      df_cc1 = bd.Df_Query(query_cc1)
      st.write(df_cc1)
      if not df_cc1.empty:
        st.write(bd.Query_Alarme(incio=df_cc1['Inicio Aplicação'].iloc[0],fim=df_cc1['Fim Aplicação'].iloc[0]))
      else:
        st.markdown('### _Aplicação Manual_')

    with col2:
      st.markdown('## Robô 2')
      df_cc2 = bd.Df_Query(query_cc2)
      st.write(df_cc2)
      if not df_cc2.empty:
        st.write(bd.Query_Alarme(incio=df_cc2['Inicio Aplicação'].iloc[0],fim=df_cc2['Fim Aplicação'].iloc[0]))
      else:
        st.markdown('### _Aplicação Manual_')

 
  col1, col2 = st.columns(2) # informações de alarmes e cura na estufa
  with col1:
    df_alarmes = bd.Query_Alarme(limite,limite_saida)
    st.markdown('# Alarmes durante o processo')
    st.write(df_alarmes)
  with col2:
    st.markdown('# Temperatura da estufa durante a cura')
    df_estufa = bd.Query_Estufa(limite_entrada_estufa,limite_saida)
    st.write(df_estufa)



  
  
