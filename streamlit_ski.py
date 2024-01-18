import pymongo
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import time
from pymongo import MongoClient
import matplotlib.pyplot as plt
import time
from pymongo import MongoClient
import plotly.express as px
import pymongo
from sshtunnel import SSHTunnelForwarder
import paramiko
import ast
import random
import warnings


st.set_page_config(layout="wide")
@st.cache_data
def load_combined_df():
    global combined_df
    combined_df = pd.read_csv("C:/Users/willi/Desktop/Lumiplan_formatted_flocon (2).csv")
    combined_df['Pistes'] = combined_df['Pistes'].apply(ast.literal_eval)
    combined_df['Remontées'] = combined_df['Remontées'].apply(ast.literal_eval)
    combined_df['detail'] = combined_df['detail'].apply(ast.literal_eval)
    combined_df['Ski_Counts'] = combined_df['Ski_Counts'].apply(ast.literal_eval)
    combined_df["remontee_Counts"] = combined_df['remontee_Counts'].apply(ast.literal_eval)
    return combined_df

combined_df = load_combined_df()

def calculate_daily_counts(df, column_name, selected_station):
    filtered_df = df[df[column_name] == selected_station]

    daily_counts = filtered_df.groupby('scrap_date')['Ski_Counts'].agg(
        lambda x: {
            'Open': sum(y['Open'] for y in x),
            'Closed': sum(y['Closed'] for y in x),
            'Green_closed': sum(y['Green_closed'] for y in x),
            'Green_open': sum(y['Green_open'] for y in x),
            'Blue_closed': sum(y['Blue_closed'] for y in x),
            'Blue_open': sum(y['Blue_open'] for y in x),
            'Red_closed': sum(y['Red_closed'] for y in x),
            'Red_open': sum(y['Red_open'] for y in x),
            'Black_closed': sum(y['Black_closed'] for y in x),
            'Black_open': sum(y['Black_open'] for y in x),
        }
    ).reset_index()

    daily_counts[['Open', 'Closed', 'Green_closed', 'Green_open', 'Blue_closed', 'Blue_open', 'Red_closed', 'Red_open', 'Black_closed', 'Black_open']] = pd.json_normalize(daily_counts['Ski_Counts'])

    return daily_counts

def calculate_daily_counts_all():

    daily_counts = combined_df.groupby('scrap_date')['Ski_Counts'].agg(
        lambda x: {
            'Open': sum(y['Open'] for y in x),
            'Closed': sum(y['Closed'] for y in x),
            'Green_closed': sum(y['Green_closed'] for y in x),
            'Green_open': sum(y['Green_open'] for y in x),
            'Blue_closed': sum(y['Blue_closed'] for y in x),
            'Blue_open': sum(y['Blue_open'] for y in x),
            'Red_closed': sum(y['Red_closed'] for y in x),
            'Red_open': sum(y['Red_open'] for y in x),
            'Black_closed': sum(y['Black_closed'] for y in x),
            'Black_open': sum(y['Black_open'] for y in x),
        }
    ).reset_index()

    daily_counts[['Open', 'Closed', 'Green_closed', 'Green_open', 'Blue_closed', 'Blue_open', 'Red_closed', 'Red_open', 'Black_closed', 'Black_open']] = pd.json_normalize(daily_counts['Ski_Counts'])

    return daily_counts
def calculate_daily_remontee():
    daily_counts = combined_df.groupby('scrap_date')['remontee_Counts'].agg(
        lambda x: {
            'Open_remontee': sum(y['Open_remontee'] for y in x),
            'Closed_remontee': sum(y['Closed_remontee'] for y in x),
        }
    ).reset_index()
    daily_counts[['Open_remontee', 'Closed_remontee']] = pd.json_normalize(daily_counts['remontee_Counts'])
    return daily_counts

def calculate_daily_remontee_station(df, column_name, selected_station):
    filtered_df = df[df[column_name] == selected_station]
    daily_counts = filtered_df.groupby('scrap_date')['remontee_Counts'].agg(
        lambda x: {
            'Open_remontee': sum(y['Open_remontee'] for y in x),
            'Closed_remontee': sum(y['Closed_remontee'] for y in x),
        }
    ).reset_index()
    daily_counts[['Open_remontee', 'Closed_remontee']] = pd.json_normalize(daily_counts['remontee_Counts'])
    return daily_counts

def count_color_slopes(ski_counts):
    color_counts = {'Green': 0, 'Blue': 0, 'Red': 0, 'Black': 0}

    color_counts['Green'] += ski_counts['Green_closed'] + ski_counts['Green_open']
    color_counts['Blue'] += ski_counts['Blue_closed'] + ski_counts['Blue_open']
    color_counts['Red'] += ski_counts['Red_closed'] + ski_counts['Red_open']
    color_counts['Black'] += ski_counts['Black_closed'] + ski_counts['Black_open']

    return color_counts

def main():
    #Graphs sur le Ski dans toute la France 
    #test

    color_mapping = {
    'Open': 'yellow',
    'Closed': 'darkgoldenrod',
    'Green_closed': 'darkgreen',
    'Green_open': 'green',
    'Blue_closed': 'darkblue',
    'Blue_open': 'blue',
    'Red_closed': 'darkred',
    'Red_open': 'red',
    'Black_closed': 'darkgray',
    'Black_open': 'gray',
    }

    st.markdown("<h1 style='text-align: center;'>Le Ski en France</h1>", unsafe_allow_html=True)
    all_stations_daily_counts = calculate_daily_counts_all()

    fig_all_stations = px.line(all_stations_daily_counts, x='scrap_date', y=['Open', 'Closed', 'Green_closed', 'Green_open', 'Blue_closed', 'Blue_open', 'Red_closed', 'Red_open', 'Black_closed', 'Black_open'],
                title="Evolution de l'ouverture et fermeture des pistes de skis par couleur",color_discrete_map=color_mapping,width=1300)
    fig_all_stations.update_layout(xaxis_title='Date', yaxis_title='Count', legend_title='Status',title_font=dict(size=20), xaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),yaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),legend=dict(font=dict(size=20)) )

    #   st.plotly_chart(fig_all_stations)

    all_remontee_daily_counts = calculate_daily_remontee()
    fig = px.line(all_remontee_daily_counts, x='scrap_date', y=['Open_remontee', 'Closed_remontee'], title="Evolution de l'ouverture des remontées mécaniques")
    fig.update_layout(xaxis_title='Date', yaxis_title='Count', legend_title='Status',title_font=dict(size=20), xaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),yaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),legend=dict(font=dict(size=20)))
    
    col1, col2 = st.columns((2))  
    

    with col1:
        st.plotly_chart(fig_all_stations,use_container_width=False)

    
    with col2:
        st.plotly_chart(fig,use_container_width=True)


    #Graph sur une station en particulier
    st.markdown("<h1 style='text-align: center;'>Information sur une station en particulier</h1>", unsafe_allow_html=True)
    sorted_stations = combined_df.groupby('station_name')['nombre_flocon_vert'].sum().sort_values(ascending=False).index

    st.markdown(f"""
        <div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
            <div style="text-align: center;">
                <h1>La certification Flocon Vert c'est quoi ? </h1>
                <img src='https://www.bourgsaintmaurice.fr/fileadmin/user_upload/Images/BSM/Transition_Ecologique/InfographieFloconVert.jpg' style='max-width: 100%; max-height: 100%;'>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>Choisissez une station avec un flocon vert ou plus !</h3>", unsafe_allow_html=True)
    def format_station(station):
        flocon_count = combined_df.loc[combined_df['station_name'] == station, 'nombre_flocon_vert'].iloc[0]
        
        if flocon_count > 0:
            return f"{station} - BONNE station qui entreprend des actions responsables! ({flocon_count} flocon{'s' if flocon_count > 1 else ''} vert ! )"
        elif flocon_count == 0:
            return f"{station} - MAUVAISE station pas de flocon vert!"
        else:
            return station

    # Create the selectbox with the custom format function
    selected_station = st.selectbox('', sorted_stations, format_func=format_station)

    selected_station_daily_counts = calculate_daily_counts(combined_df, 'station_name', selected_station)

    #Piste ski
    fig_selected_station = px.line(selected_station_daily_counts, x='scrap_date', y=['Open', 'Closed', 'Green_closed', 'Green_open', 'Blue_closed', 'Blue_open', 'Red_closed', 'Red_open', 'Black_closed', 'Black_open'],
                title=f"Evolution de l'ouverture des pistes de skis à {selected_station} par couleur",color_discrete_map=color_mapping)
    fig_selected_station.update_layout(xaxis_title='Date', yaxis_title='Nombre', legend_title='Status',title_font=dict(size=20), xaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),yaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),legend=dict(font=dict(size=20)))
    #st.plotly_chart(fig_selected_station)

    #Remontee mécanique
    selected_remontee_daily_counts = calculate_daily_remontee_station(combined_df, 'station_name', selected_station)
    fig = px.line(selected_remontee_daily_counts, x='scrap_date', y=['Open_remontee', 'Closed_remontee'],title=f"Evolution de l'ouverture des remontées mécaniques à {selected_station}")
    fig.update_layout(xaxis_title='Date', yaxis_title='Nombre', legend_title='Status',title_font=dict(size=20), xaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),yaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),legend=dict(font=dict(size=20)))
    
    #st.plotly_chart(fig)
    color_mapping = {
    'Green': 'green',
    'Blue': 'blue',
    'Red': 'red',
    'Black': 'black',}
    #
    df2 = combined_df[combined_df["station_name"] == selected_station]
    color_count = count_color_slopes(df2["Ski_Counts"].iloc[0])
    fig_color_counts = px.bar(x=list(color_count.keys()), y=list(color_count.values()), color=list(color_count.keys()),color_discrete_map=color_mapping)
    fig_color_counts.update_layout(xaxis_title='couleur de piste', yaxis_title='Nombre', title=f"Nombre de pistes de skis bleu,rouge,verte,noir à {selected_station}",title_font=dict(size=20), xaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),yaxis=dict(title_font=dict(size=20),tickfont=dict(size=20),),legend=dict(font=dict(size=20)))
    #st.plotly_chart(fig_color_counts)

    col1, col2,col3 = st.columns((3)) 
    
    
    with col1:
        st.plotly_chart(fig_selected_station, use_container_width=True)

    with col2:
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.plotly_chart(fig_color_counts, use_container_width=True)



    flocon_vert_count = df2['nombre_flocon_vert'].iloc[0]

    if flocon_vert_count != 0:
        st.markdown(
            f"<h1 style='text-align: center;'>La station {selected_station} est certifiée Flocon Vert avec : {flocon_vert_count} flocon ! Bon choix de destination !</h1>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 60vh;">
            <img src='https://www.saintfrancoislongchamp.com/content/uploads/2022/03/logo-flocon-vert-263x300.png' style='max-width: 100%; max-height: 100%;'>
        </div>
        """, unsafe_allow_html=True)
    else:
        # First row: Title, image, list of random stations
        
        # Display random stations
        non_zero_flocon_vert_stations = combined_df[combined_df['nombre_flocon_vert'] != 0]
        # Ensure that there are at least 5 unique stations
        unique_stations = set()
        while len(unique_stations) < 5:
            random_stations = random.sample(list(non_zero_flocon_vert_stations['station_name']), 5)
            unique_stations = set(random_stations)

        # Sort stations based on flocon vert count in descending order
        sorted_stations = sorted(unique_stations, key=lambda station: non_zero_flocon_vert_stations.loc[non_zero_flocon_vert_stations['station_name'] == station, 'nombre_flocon_vert'].iloc[0], reverse=True)

        st.markdown(f"""
            <div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
                <div style="text-align: center;  align-self: flex-start;">
                    <h2>Voici d'autres stations qui sont certifiées Flocon Vert que vous devriez considérer. Pensez à la planète !</h3>
                    <!-- Display random stations -->
                  {"".join([f"<h3>{station}: {non_zero_flocon_vert_stations.loc[non_zero_flocon_vert_stations['station_name'] == station, 'nombre_flocon_vert'].iloc[0]} flocon</h3>" for station in sorted_stations])}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Second row: Title and image
      


if __name__ == '__main__':
    main()