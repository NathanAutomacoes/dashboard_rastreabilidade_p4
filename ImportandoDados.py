import pandas as pd
import pyodbc



class BancoDados():  
  def __init__(self):
    server = r'126.1.1.33\AUTOMES'
    database = 'p4_relatorio'
    username = 'Pintura4'
    password = 'P4#auto01'

    self.conexao_str = ( f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
    )

    database = 'p4_alarmes'
    self.conexao_alarmes=( f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
    )

  # Função para executar a query e retornar um DataFrame usando pandas
  def Df_Query(self,query):
      try:
          # Conectando e executando a query diretamente com pandas
          with pyodbc.connect(self.conexao_str) as connect:
              df = pd.read_sql_query(query, connect)
          return df  
      except pyodbc.Error as e:
          print(f'Erro: {e}')
          return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
  
  def Get_Value(self,query):
    try:
      with pyodbc.connect(self.conexao_str) as connect:
        with connect.cursor() as cursor:
          # Executar a consulta
          cursor.execute(query)
          result = cursor.fetchone()
          # Se houver resultado, retornar o valor, caso contrário, None
          if result:
              return result[0]  # O valor da primeira (e única) coluna é o que você quer
          else:
              return None
    except pyodbc.Error as e:
          print(f'Erro: {e}')
          return None
    
  def Query_Alarme(self,incio,fim):
    query = f'''
      SELECT TOP (1000)
          --,DATEDIFF(second,InTime,OutTime) as duracao
            format([InTime],'dd/MM/yyyy HH:mm:ss') as 'Início do Alarme'
          ,format(OutTime,'dd/MM/yyyy HH:mm:ss') as 'Fim do Alarme'
            ,[Message]
            ,[Source]
            ,[Tipo de Alarme]
            , format(AckTime,'dd/MM/yyyy HH:mm:ss') as 'Horario de reconhecimento'
        FROM [p4_alarmes].[dbo].[Alarms_E3]
        where InTime >= CONVERT(datetime,'{incio}',103)
        and OutTime <= CONVERT(datetime,'{fim}',103)
        and OutTime <> '1899-12-30 00:00:00.000'
        order by E3TimeStamp desc
    '''
    try:
      # Conectando e executando a query diretamente com pandas
      with pyodbc.connect(self.conexao_str) as connect:
          df = pd.read_sql_query(query, connect)
      return df  
    except pyodbc.Error as e:
      print(f'Erro: {e}')
      return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
   
  def Query_Estufa(self,incio,fim):
    query = f'''SELECT TOP (1000) format([E3TimeStamp],'dd/MM/yyyy HH:mm:ss') as 'Data e Hora'
        ,[ZonaAquecimento1]
        ,[ZonaAquecimento2] 
        ,[14S0TA211-B40N1]
        ,[14S0TA211-B40N2]
        ,[14S0TA211-B40N3]
        ,[14S0TA211-B40N4]
        ,[14S0TA211-B40N5]
        ,[14S0TA311-B40N1]
        ,[14S0TA311-B40N2]
        ,[14S0TA311-B40N3]
        ,[14S0TA311-B40N4]
        ,[14S0TA311-B40N5]
        ,[14S0WH114-B40N]
        ,[14S0WH114-B25N]
        FROM [p4_graficos].[dbo].[14S0]
        where E3TimeStamp >= CONVERT(datetime,'{incio}',103)
        and E3TimeStamp <= CONVERT(datetime,'{fim}',103)
        order by E3TimeStamp asc''' 
    try:
      # Conectando e executando a query diretamente com pandas
      with pyodbc.connect(self.conexao_str) as connect:
          df = pd.read_sql_query(query, connect)
      return df  
    except pyodbc.Error as e:
      print(f'Erro: {e}')
      return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro
   

if __name__ =='__main__':
   
   query = 'Select * from [p4_relatorio].[dbo].[AplPRM]'
   bd = BancoDados()
   df = bd.Df_Query(query)

   print(df.head())

   

