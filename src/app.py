import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# Dicionário com Regiões e seus Estados
RegionStates = {#North
                'AM': 'North',
                'RR': 'North',
                'AP': 'North',
                'PA': 'North',
                'TO': 'North',
                'RO': 'North',
                'AC': 'North', 
                #Northeast
                'MA': 'Northeast',
                'PI': 'Northeast',
                'CE': 'Northeast',
                'RN': 'Northeast',
                'PE': 'Northeast',
                'PB': 'Northeast',
                'SE': 'Northeast',
                'AL': 'Northeast',
                'BA': 'Northeast',
                #Midwest
                'MT': 'Midwest',
                'MS': 'Midwest',
                'GO': 'Midwest',
                'DF': 'Midwest',
                #Southest
                'SP': 'Southest',
                'RJ': 'Southest',
                'ES': 'Southest',
                'MG': 'Southest',
                #South
                'PR': 'South',
                'RS': 'South',
                'SC': 'South'
                }


States = {#North
          'AM': 'Amazonas',
          'RR': 'Roraima',
          'AP': 'Amapá',
          'PA': 'Para',
          'TO': 'Tocantins',
          'RO': 'Rondônia',
          'AC': 'Acre',
          #Northeast
          'MA': 'Maranhão',
          'PI': 'Piauí',
          'CE': 'Ceará',
          'RN': 'Rio Grande do North',
          'PE': 'Pernambuco',
          'PB': 'Paraíba',
          'SE': 'Sergipe',
          'AL': 'Alagoas',
          'BA': 'Bahia',
          #Midwest
          'MT': 'Mato Grosso',
          'MS': 'Mato Grosso do South',
          'GO': 'Goiás',
          'DF': 'Distrito Federal',
          #Southest
          'SP': 'São Paulo',
          'RJ': 'Rio de Janeiro',
          'ES': 'Espírito Santo',
          'MG': 'Minas Gerais',
          #South
          'PR': 'Paraná',
          'RS': 'Rio Grande do South',
          'SC': 'Santa Catarina'
          }      

regions_list = ['NORTH', 
                'SOUTH' ,
                'MIDWEST',
                'SOUTHEAST',
                'NORTHEAST']                    

@st.cache
def load_data(path):
    data  = pd.read_csv(path)
    return data

def plot_comparation_graph(data_2019,
                           data_2020,
                           data_2021,
                           death_cause = 'ALL',
                           state = 'BRASIL'):

    if state == 'BRASIL':
        total_2019 = data_2019.groupby(['tipo_doenca']).sum()
        total_2020 = data_2020.groupby(['tipo_doenca']).sum()
        total_2021 = data_2021.groupby(['tipo_doenca']).sum()

        disease_list = [int(total_2019.loc[death_cause]), 
                        int(total_2020.loc[death_cause]),
                        int(total_2020.loc[death_cause])]
        title = 'in Brazil'
    elif state.upper() in regions_list:
        print(state.upper())
        total_2019 = data_2019.groupby(['region','tipo_doenca']).sum()
        total_2020 = data_2020.groupby(['region','tipo_doenca']).sum()
        total_2021 = data_2021.groupby(['region','tipo_doenca']).sum()

        disease_list = [int(total_2019.loc[state, death_cause] if (state, death_cause) in total_2019.index else 0),
                        int(total_2020.loc[state, death_cause] if (state, death_cause) in total_2020.index else 0),
                        int(total_2021.loc[state, death_cause] if (state, death_cause) in total_2021.index else 0)]        
      
        title = f'in the {state.lower()} region'        

    elif death_cause != 'ALL':                          
        total_2019 = data_2019.groupby(['uf','tipo_doenca']).sum()
        total_2020 = data_2020.groupby(['uf','tipo_doenca']).sum()
        total_2021 = data_2021.groupby(['uf','tipo_doenca']).sum()

        disease_list = [int(total_2019.loc[state, death_cause] if (state, death_cause) in total_2019.index else 0),
                        int(total_2020.loc[state, death_cause] if (state, death_cause) in total_2020.index else 0),
                        int(total_2021.loc[state, death_cause] if (state, death_cause) in total_2021.index else 0)]        
      
        title = f'in the state of {state.upper().replace(state, States[state])}'

    data = pd.DataFrame({'Total': disease_list,
                         'Year': [2019, 2020, 2021]})

    sns.set_style("white")   
    palette = sns.color_palette("hls", 8) 
    fig, ax = plt.subplots(figsize=(8, 5))

    ax = sns.barplot(x = 'Year' , y = 'Total', data = data, palette= palette)
 
    ax.set_title(f'Cause of death - {death_cause} - {title}')
    ylabels = ['{:,.2f}'.format(y) + ' K' for y in ax.get_yticks()/1000]
    #ax.grid()

    ax.set_yticklabels(ylabels)

    return fig

def main():

   # data_2019 = load_data('data/obitos-2019.csv')
   # data_2020 = load_data('data/obitos-2020.csv') 
   # data_2021 = load_data('data/obitos-2021.csv')    
   # 
    data_2019 = load_data('C:\Dev\GitHub\streamlit_covid\data\obitos-2019.csv')
    data_2020 = load_data('C:\Dev\GitHub\streamlit_covid\data\obitos-2020.csv')
    data_2021 = load_data('C:\Dev\GitHub\streamlit_covid\data\obitos-2021.csv')

    disease_types = data_2021['tipo_doenca'].unique().tolist()
    states = np.append(data_2021['uf'].unique(),'BRASIL').tolist()


    st.title('Deaths by diseases in Brazil')
    st.markdown('Deaths analysis per state / country - **2019 - 2021**')
    st.markdown('app by Pablo Pereira')

    default_ix1 = disease_types.index('SRAG')
    default_ix2 = states.index('BRASIL')

    pDisease = st.sidebar.selectbox('Select the disease type', disease_types, index=default_ix1)
    pState = st.sidebar.selectbox('Select a Brazilian state', states, index=default_ix2)

    figure = plot_comparation_graph(data_2019,
                                data_2020,
                                data_2021,
                                pDisease,
                                pState)

    st.pyplot(figure)

if __name__ == '__main__':
    main()