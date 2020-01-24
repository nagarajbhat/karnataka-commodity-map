""" flask_example.py

    Required packages:
    - flask
    - folium
    - xlrd
    - pandas
    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask,render_template, request, redirect
import pandas as pd
#from IPython.core.display import display, HTML


import folium

app = Flask(__name__)



@app.route('/')
def my_form():
  
   
    data = pd.read_excel('./data/CommMktArrivals2012.xls')
    kar_latlong = pd.read_excel("./data/karnataka_latlong.xlsx")
    state_geo = f'./data/kar.json'

    #group by and filtering data
    df = data.groupby(['Commodity','District Name','Unit'],as_index=False)
    df = df.sum().filter(["Commodity","District Name","Arrival","Unit"])
    df = df[df["Unit"]=="Quintal   "]
    #merge data with ['latitude','longitude']
    df_merged = pd.merge(df,kar_latlong)
    df_com = df_merged["Commodity"].unique()
    m = folium.Map([15, 74], zoom_start=6,tiles="cartodbpositron",overlay=False)
  
    geojson1 = folium.GeoJson(data=state_geo,
               name='karnataka district',
               style_function=lambda x: {'color':'black','fillColor':"#fc7978",'weight':0.5},
                tooltip=folium.GeoJsonTooltip(fields=['NAME_2'],
                                              labels=False,
                                              sticky=True),
              highlight_function=lambda x: {'weight':3,'fillColor':'red'},
                        
                       ).add_to(m)
    aframe = m._repr_html_()

    return render_template('my-form.html',aframe=aframe,df_com=df_com)
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

   
    #df_merged
    #read data
    data = pd.read_excel('./data/CommMktArrivals2012.xls')
    kar_latlong = pd.read_excel("./data/karnataka_latlong.xlsx")
    state_geo = f'./data/kar.json'

    #group by and filtering data
    df = data.groupby(['Commodity','District Name','Unit'],as_index=False)
    df = df.sum().filter(["Commodity","District Name","Arrival","Unit"])
    df = df[df["Unit"]=="Quintal   "]
    #merge data with ['latitude','longitude']
    df_merged = pd.merge(df,kar_latlong)

    m = folium.Map([15, 74], zoom_start=6,tiles=None,overlay=False)
    #commodity = input("enter the commodity")
    commodity= text
    commodity = commodity.title()

    commodity_data = df_merged[df_merged["Commodity"]==commodity]

    choropleth1 = folium.Choropleth(
    geo_data=state_geo,
    name='map',
    data=commodity_data,
    columns=['District Name', 'Arrival'],
    key_on='feature.properties.NAME_2',
    fill_color='YlGn',
    nan_fill_color="black",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Arrival (in Quintal)',
    highlight=True,
    line_color='black').add_to(m)

    geojson1 = folium.GeoJson(data=state_geo,
               name='karnataka district',
                         smooth_factor=2,
               style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                tooltip=folium.GeoJsonTooltip(fields=['NAME_2'],
                                              labels=False,
                                              sticky=True),
              highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        
                       ).add_to(choropleth1)

    folium.TileLayer('cartodbpositron',overlay=False,name="light mode").add_to(m)
    folium.TileLayer('cartodbdark_matter',overlay=False,name="dark mode").add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    #m.save('all_commodities.html')

    iframe = m._repr_html_()
    #display(HTML(iframe))
    

    return iframe


if __name__ == '__main__':
    app.run(debug=True)