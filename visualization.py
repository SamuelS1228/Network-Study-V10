import pydeck as pdk
import pandas as pd
import streamlit as st

def plot_network(stores_df, centers):
    st.subheader("Network Map")
    store_layer = pdk.Layer(
        'ScatterplotLayer',
        data=stores_df,
        get_position='[Longitude, Latitude]',
        get_color='[0, 128, 255]',
        get_radius=15000,
        opacity=0.6,
    )
    center_df = pd.DataFrame(centers, columns=['Longitude','Latitude'])
    warehouse_layer = pdk.Layer(
        'ScatterplotLayer',
        data=center_df,
        get_position='[Longitude, Latitude]',
        get_color='[255, 0, 0]',
        get_radius=30000,
        opacity=0.8,
    )
    # edges
    edges=[]
    for _,row in stores_df.iterrows():
        wh = center_df.iloc[int(row['Warehouse'])]
        edges.append({'from_lon':row['Longitude'], 'from_lat':row['Latitude'],
                      'to_lon':wh['Longitude'], 'to_lat':wh['Latitude']})
    edge_layer = pdk.Layer(
        'LineLayer',
        data=edges,
        get_source_position='[from_lon, from_lat]',
        get_target_position='[to_lon, to_lat]',
        get_width=2,
        get_color='[200,200,200]'
    )
    view_state = pdk.ViewState(latitude=39, longitude=-98, zoom=3.5)
    r = pdk.Deck(layers=[edge_layer, store_layer, warehouse_layer], initial_view_state=view_state,
                 map_style='mapbox://styles/mapbox/light-v10')
    st.pydeck_chart(r)

def summary(stores_df, total_cost, trans_cost, wh_cost):
    st.subheader("Cost Summary")
    st.metric("Total Annual Cost", f"${total_cost:,.0f}")
    col1,col2=st.columns(2)
    col1.metric("Transportation", f"${trans_cost:,.0f}")
    col2.metric("Warehousing", f"${wh_cost:,.0f}")
    st.bar_chart(stores_df['Warehouse'].value_counts().sort_index())
