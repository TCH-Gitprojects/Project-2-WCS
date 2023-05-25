import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.metrics import accuracy_score, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import streamlit.components.v1 as components
from st_clickable_images import clickable_images 
import json
import requests
from streamlit_lottie import st_lottie
from st_on_hover_tabs import on_hover_tabs

actors = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/Avec_nconst.csv")
top10_2022 = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/top_10_2022.csv")
top10 = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/top10.csv")
avg_runtime = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/avg_runtime.csv")
film2022 = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/film_2022.csv")
testgenres = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/Avec_tconst.csv",low_memory=False)
top10_30y = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/top_10_des_30.csv")
kpi_22 = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/describe_df2.csv")

top10_30y = top10_30y.rename(columns={"Temps du film": "Durée du film en minutes"})

test = actors[(actors['startYear'] >= 1993) & (actors['startYear'] <= 2023) & (actors["category"]=="director")]
test = test.filter(["nconst", "primaryName", "startYear",])
top_director = test['primaryName'].value_counts().head(10)

test2 = actors[(actors['startYear'] >= 1993) & (actors['startYear'] <= 2023) & (actors["category"]=="actor")]
test2 = test2.filter(["nconst", "primaryName", "startYear",])
top_actor = test2['primaryName'].value_counts().head(10)

test3 = actors[(actors['startYear'] >= 1993) & (actors['startYear'] <= 2023) & (actors["category"]=="actress")]
test3 = test3.filter(["nconst", "primaryName", "startYear"])
top_actress = test3['primaryName'].value_counts().head(10)

test = actors[(actors['startYear'] >= 1993) & (actors['startYear'] <= 2023) & (actors["category"].str.contains("actor|actress"))]
actoress = test["category"].value_counts()

testgenres = testgenres[testgenres['startYear'] != '\\N']
testgenres['startYear'] = testgenres['startYear'].astype(int)
testgenres = testgenres[(testgenres['startYear'] >= 1993) & (testgenres['startYear'] <= 2023) &
                        (testgenres["averageRating"]>=6) & (testgenres["runtimeMinutes"]>=60) & (testgenres["numVotes"]>=10000)]
genresiwant = testgenres["genres"].str.get_dummies(sep=",")
totalgenres = genresiwant.sum().sort_values(ascending=False).head(10)

film2022_num_votes = film2022[(film2022['numVotes'] >= 100000)]
top_10_final_kpi = film2022_num_votes.sort_values(by = 'averageRating', ascending=False, inplace= False)
top_10_final_kpi2 = top_10_final_kpi.head(10)
film2022_graph = film2022.reset_index()
film2022_graph1 = film2022_graph.sort_values(by = 'averageRating', ascending=False, inplace= False)
genre_film2022 = film2022_graph1.filter(['Action', 'Adventure', 'Animation',
       'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
       'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical',
       'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War',
       'Western'])
graph2022 = genre_film2022.sum().sort_values(ascending=False)

def make_clickable(url):
	return f'<a href="{url}" target="_blank">IMDb</a>'

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'><em>Wild Code School 2023</em><br><strong>Projet 2 - IMDb</strong></h1>", unsafe_allow_html=True)
css = '''
<style>
    section[data-testid='stSidebar'] {
        background-color: #111;
        min-width: unset !important;
        width: unset !important;
        flex-shrink: unset !important;
    }

    button[kind="header"] {
        background-color: transparent;
        color: rgb(180, 167, 141);
    }

    @media(hover) {
        header[data-testid="stHeader"] {
            display: none;
        }

        section[data-testid='stSidebar'] > div {
            height: 100%;
            width: 95px;
            position: relative;
            z-index: 1;
            top: 0;
            left: 0;
            background-color: #111;
            overflow-x: hidden;
            transition: 0.5s ease;
            padding-top: 60px;
            white-space: nowrap;
        }

        section[data-testid='stSidebar'] > div:hover {
            width: 300px;
        }

        button[kind="header"] {
            display: none;
        }
    }

    @media(max-width: 272px) {
        section[data-testid='stSidebar'] > div {
            width: 15rem;
        }
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)



with st.sidebar:
    tabs = on_hover_tabs(tabName=['Waiting Screen','Présentation', 'La Creuse', 'Exploration', 'KPI',"Machine Learning","Axes d'amélioration","Difficultées"], 
                         iconName=['capture','co_present', 'signpost', 'dashboard', 'data_thresholding','select_all','tips_and_updates','error'], default_choice=0)

if tabs == 'Waiting Screen':
    col1, mid, col2 = st.columns(3)
    with col1:
        st.image("/Users/tony/Downloads/codowski.jpg", width = 1000)

elif tabs =='Présentation':
    st.title('Bienvenue sur le Streamlit de notre projet :man-man-girl-boy:')
    '''
##### Nous sommes The Big Codowski et notre équipe est composée de :
 - **Tia** : *Scrum Master*  
 - **Tony** : *Product Owner* 
 - **Lucas** : *Team member* 
 - **Emmanuel** : *Team member*

##### Nous avons été contactés par un directeur de cinéma éprouvant des difficultés à relancer son activité. L'établissement étant situé dans la Creuse, il nous a demandé conseil pour avoir une liste de recommandations de films à diffuser à un large public.
**Pour ce faire, nous avons établi un plan d'action en trois étapes :**
1. Récupération des databases sur le site internet **IMDB** afin d'avoir un large éventail de données sur les films. Un tri a été fait avec **Visual Studio Code** parmi toutes ses informations pour récupérer celles qui nous seront utiles par rapport au public visé.
2. Création d'un **algorithme de Machine Learning** qui sortira une liste de films en fonction des paramètres établis par le client.
3. Importation des données sur **Streamlit** pour avoir une visualisation des données triées. Cela permettra également d'avoir une interface propre pour permettre au client de saisir ses paramètres et ainsi d'avoir sa recommandation de films.
Nous nous sommes servis de plusieurs bibliothèques sous **Python** comme **Pandas**, **Plotly Express** pour faire du *nettoyage*, *filtrage* et *visualisation* de données parmi les databases à disposition.
Nous avons utilisé la méthode des **proches voisins** comme algorithme d'apprentissage automatique supervisé pour la partie **Machine Learning**.
Il a été nécessaire de faire des choix dans l'utilisation des données pour que le système soit simple d'utilisation et pertinent pour le client.

##### Technos utilisées pour l'organisation et la réalisation du projet :
    ''' 
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1 :	
        st.image("https://logowik.com/content/uploads/images/notion1411.jpg")
    with col2 :	
        st.image("https://www.presse-citron.net/app/uploads/2019/01/Nouveau-logo-Slack-1.jpg")
    with col3 :	
        st.image("https://logowik.com/content/uploads/images/imdb-internet-movie-database5351.jpg")
    with col4 :	
        st.image("https://codersera.com/blog/wp-content/uploads/2019/08/visual-studio-code-codersera.jpg")
    with col5 :	
        st.image("https://cdn.analyticsvidhya.com/wp-content/uploads/2020/10/image4.jpg")
    with col6 :	
        st.image("https://logo-marque.com/wp-content/uploads/2021/10/Python-Symbole.jpg")
    with col7 :	
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png")
    with col8 :	
        st.image("https://jorisvandenbossche.github.io/2018_DigiCosme_Software_Day/img/sklearn_logo.png")

elif tabs == 'La Creuse':
    '''
	# Le département de la Creuse :cow2:
	'''
    
    col1, col2 = st.columns(2)
    col1.metric(label="Population totale de la Creuse", value="115 995 habitants en 2020", delta="-3,8% par rapport à 2014")
    col2.metric("Age moyen", "58 ans en 2020", delta="+6 ans par rapport à 2014",
    delta_color="inverse")
    
    option = {
             'title': {
    'text': 'Répartition de la population de la Creuse',
    'subtext': 'Source : Insee 2019',
    'left': 'left'
  },
  'tooltip': {
    'trigger': "item",
    'formatter': "{a} <br/>{b} : {c} ({d}%)"
  },
  'legend': {
    'top': 'bottom'
  },
  'toolbox': {
    'show': True,
    'feature': {
      'mark': { 'show': True },
      'dataView': { 'show': True, 'readOnly': False },
      'restore': { 'show': True },
      'saveAsImage': { 'show': True }
    }
  },
  'series': [
    {     'name': 'Répartition de la population',
      'type': 'pie',
      'radius': [10, 140],
      'center': ['50%', '50%'],
      'roseType': 'area',
      'itemStyle': {
        'borderRadius': 8
      },
      "label": {
        "show": False
      },
      "emphasis": {
        "label": {
          "show": True
        }
      },
      'data': [
        { 'value': 27254, 'name': '60 à 74 ans' },
        { 'value': 24996, 'name': '45 à 59 ans' },
        { 'value': 17607, 'name': '75 ans ou plus' },
        { 'value': 16871, 'name': '30 à 44 ans' },
        { 'value': 15510, 'name': '0 à 14 ans' },
        { 'value': 14379, 'name' : '15 à 29 ans' }
      ]
    }
  ]
    };
    st_echarts(options=option)
    '''
    La population totale de la Creuse est de **115 995** habitants en 2020. Cela représente une baisse de **3,8%** par rapport à 2014. 
    
    Nous pouvons voir sur ce graphique circulaire que plus de **45%** de la population à plus de **45 ans** et l’âge moyen est de **58 ans**, c’est **+6** années par rapport à 2014.
    
    Le département de la Creuse possède une population vieillissante et en déclin démographique.
    '''

    st.image('/Users/tony/Desktop/Evolution pop.png')
    '''
    Ainsi, nous observons que la Creuse perd bon nombre d'habitants au fil des ans. Les jeunes partent vers les grandes agglomérations en dehors du département, ce qui provoque un déficit important de citoyens.
    
    En outre, avec un taux de pauvreté alarmant (**18.7 %**), un faible nombre d'habitants au km² (**23** en Creuse contre **106** en moyenne nationale) et une moyenne de **7 minutes** pour accéder à un service de proximité, il est préférable pour les jeunes adultes de partir. 
    
    A l'inverse, les retraités y sont nombreux (**2 personnes sur 5**) ainsi que les résidences secondaires et logements vacants qui représentent **35 %** du total des habitations.
    '''


elif tabs == 'Exploration':
    '''
	# Exploration des données IMDb :movie_camera:
	###### Pour répondre au besoin de notre client, nous avons réalisé une étude des databases basées sur les 30 dernières années.
	 - Ce premier graphique montre la durée moyenne des films ainsi que les différents genres de films présents.
	'''
    
    with st.expander("Moyenne de la durée et répartition par genres :"):
        fig4 = go.Figure(go.Treemap(
    	values=totalgenres.values,
    	labels=totalgenres.index,
    	parents=["Genres"] * len(totalgenres.index),
        textinfo = "label+value+percent root",
        textposition='middle center',
        hoverinfo = 'skip',
        texttemplate='<b>%{label}</b><br>%{value} films<br>Ratio : %{percentRoot}',
        insidetextfont=dict(size=16),           
        marker=dict(
            colorscale='Viridis'),
            ))
        fig4.update_layout(margin = dict(t=0, l=0, r=0, b=0),                 
    	height=630,
    	)
        
        fig5 = px.line(avg_runtime, 
                       x="startYearNumeric", 
                       y="runtimeNumeric", 
                       title="Durée moyenne des films (en minutes) au cours des 30 dernières années.", 
                       color_discrete_sequence=px.colors.sequential.Viridis)
        fig5.update_layout(title_x=0.25)
        fig5.update_xaxes(title_text="Année")
        fig5.update_yaxes(title_text="Durée (minutes)")
        st.plotly_chart(fig5, use_container_width=True)
        st.metric(label="Durée moyenne sur les 30 dernières années", value="91 minutes")
        '''
    Nous observons une **baisse significative** au cours des années 2019-2021, nous ne pouvons qu'estimer que cela est dû aux années Covid 19. 

    La durée des films a commencé à **s'allonger** lorsque l'industrie est passée de la projection 35 mm à la projection numérique il y a près de dix ans.

    Comme les studios devaient souvent produire des centaines de copies de films importants, ils avaient intérêt à les maintenir à une longueur standard, la copie d'un film de trois heures coûtant **deux fois plus cher que celle d'un film de 90 minutes.**

    Avec la projection numérique, les films durent plus longtemps sans coût supplémentaire pour le studio, ce qui signifie que "**les réalisateurs peuvent créer le chef-d'œuvre qu'ils souhaitent sans avoir à le couper pour respecter un budget**".
    '''
        
        st.plotly_chart(fig4, use_container_width=True)
        st.metric(label="Genre le plus représenté", value="Drama avec 28%")
        '''
        Au cours des 30 dernières années, le genre Drama arrive largement en tête avec un pourcentage de 28%, suivi de la comédie et de l'action. 
        '''
    
    '''
	 - Le deuxième récapitule les acteurs et actrices les plus représentés.
	'''
    
    with st.expander("Top 10 acteurs/actrices :"):
        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, horizontal_spacing=0.05,
                    subplot_titles=("Acteurs", "Actrices"))
        top_actor = top_actor.sort_values(ascending=True)
        fig.append_trace(go.Bar(x=top_actor.values,
                        y=top_actor.index,
                     textposition='inside',
                     orientation='h', 
                     width=0.7, 
                     showlegend=False, 
                     marker=dict(
                    color=px.colors.sequential.Viridis)), 
                     1, 1)
        top_actress = top_actress.sort_values(ascending=True)
        fig.append_trace(go.Bar(x=top_actress.values,
                        y=top_actress.index,
                     textposition='outside',
                     orientation='h', 
                     width=0.7, 
                     showlegend=False, 
                     marker=dict(
                    color=px.colors.sequential.Viridis),
                     yaxis='y2'), 
                     1, 2)
        fig.update_layout(
    	yaxis=dict(),
    	yaxis2=dict(overlaying='y', side='right'))
        
        fig.update_xaxes(showticklabels=True,title_text="Male", row=1, col=1, autorange='reversed')
        fig.update_xaxes(showticklabels=True,title_text="Female", row=1, col=2)
        
        fig.update_layout(title_text="Top 10 acteurs/actrices sur les 30 dernières années", 
                  width=1000, 
                  height=500,
                  title_x=0.35)
        
        st.plotly_chart(fig, use_container_width=True)
        col1, col2 = st.columns(2)
        col1.metric(label="Acteur ayant jouer dans le plus de films ces 30 dernières années", value="Samuel Lee Jackson")
        col2.metric("Actrice ayant jouer dans le plus de films ces 30 dernières années","Cate Blanchett")
        '''
        Les 10 meilleurs acteurs des 30 dernières années ont tendance à jouer principalement des rôles d'**action**, tandis que les 10 meilleures actrices des 30 dernières années ont tendance à jouer des rôles **dramatiques**.
        
        **20 %** des 10 meilleurs acteurs sont non-américains et **70 %** des 10 meilleures actrices sont non-américaines. 
        '''
        
        labels = actoress.index
        values = actoress.values
        colors = ["Gold","Indigo"]
        
        fig3 = go.Figure(data=[go.Pie(labels=labels, values=values)
                    ])
        fig3.update_traces(marker=dict(
                    colors=colors, line=dict(color='#000000', width=1)))
        
        fig3.update_layout(title_text="Répartiton Hommes/Femmes", 
                  width=1000, 
                  height=500,
                  title_x=0.35)
        st.plotly_chart(fig3, use_container_width=True)
        '''
        Il est difficile de déterminer pourquoi il y a beaucoup plus d'acteurs que d'actrices. 
    On peut imaginer que c'est parce que, même si nous n'aimons pas l'admettre, l'écart salarial entre les sexes existe encore aujourd'hui et qu'il est d'une importance effrayante dans l'industrie cinématographique. 

    Selon les sites web IMDb et Box Office Mojo, qui suivent les recettes du box-office et diffusent les dernières informations sur les films, les économistes ont pris en compte plusieurs variables, dont le succès passé d'une star, basé sur les recettes au box-office, les prix remportés et la popularité sur Twitter. Si l'on exclut ces facteurs, les stars féminines sont payées **56 %** 
    de moins que leurs homologues masculins, soit l'équivalent de **2,2 millions de dollars** de moins par film.
        '''
        
    '''
	 - Le troisème montre les différents réalisateurs ayant produit le plus de films dans cet intervalle de temps.
	'''
    
    with st.expander("Top 10 réalisateurs :"):
        fig2 = go.Figure(go.Bar(x=top_director.index, y=top_director.values, marker=dict(
                    color=px.colors.sequential.Viridis[::-1])))
        fig2.update_layout(title='Classement des réalisateurs/nombre de films', 
                  width=1000, 
                  height=500,
                  title_x=0.35)
        st.plotly_chart(fig2, use_container_width=True)
        st.metric(label="Réalisateur le plus prolifique des 30 dernières années", value="Steven Spielberg")
        '''
        Le réalisateur qui a produit le plus de films au cours des 30 dernières années est un nom que nous connaissons tous : **Steven Spielberg**. 
        
        Il est surtout connu pour des films tels que **Jurassic Park** et **Indiana Jones**. 
        
        En février 2023, Steven Spielberg reste le réalisateur qui a réalisé le plus de films dans l'histoire, avec plus de **10,67 milliards de dollars** américains au box-office mondial tout au long de sa carrière. 
        **Steven Soderbergh** arrive en deuxième position. 
        
        Pour nombre de ses films, **Soderbergh** emploie ce que l'on appelle un style *"multi-narratif"* ou *"hyperlink cinema"*. 
        
        Ce style cinématographique engendre des récits complexes, pleins de perspectives diverses, de rebondissements compliqués et d'intrigues entrelacées qui sautent à la fois en arrière et en avant dans le temps.
        Parmi ses œuvres les plus connues, citons le phénomène **"Ocean's"**, **"Contagion"** et **"Erin Brokovich"**.
        
        Les trois premiers réalisateurs sont américains. Un réalisateur français **Luc Besson** figure dans le top 10 à la **9e place**. 

        '''
        
    '''
	 - Pour finir voici le top 10 des films sortis ces 30 dernières années ainsi que leurs caractéristiques principales.
	'''
        
    with st.expander("Top 10 Films :"):
        st.markdown("<h1 style='text-align: center; color: black;'>Top 10 des 30 dernières années</h1>", unsafe_allow_html=True)
    
        clicked2 = clickable_images(
        [
        "https://images.affiches-et-posters.com//albums/3/57687/medium/the-shawshank-redemption-movie-poster-1994-1020415066.jpg",
        "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "https://images.affiches-et-posters.com//albums/3/4600/medium/4600-affiche-du-film-la-liste-de-schindler.jpg",
        "https://fr.web.img2.acsta.net/medias/nmedia/18/63/97/89/18949761.jpg",
        "https://static.posters.cz/image/750/affiches-et-posters/pulp-fiction-cover-i1288.jpg",
        "https://fr.web.img6.acsta.net/pictures/20/10/05/19/10/4468895.jpg",
        "https://m.media-amazon.com/images/M/MV5BOWNmNWY5YTMtMjk0Yy00YmU2LWFhOWYtYWFmMDZmY2E2MDViXkEyXkFqcGdeQXVyOTA2OTk0MDg@._V1_.jpg",
        "https://m.media-amazon.com/images/M/MV5BNTk2MjUxMjEtZDU5OC00MzYxLTkwMWYtMGM5YWQ0MWMyN2I1XkEyXkFqcGdeQXVyMTE0MzY0NjE1._V1_.jpg",
        "https://m.media-amazon.com/images/M/MV5BNWU1ZmNlYTctYmY1My00ZDlmLTk3M2EtZDcxY2E1ZGU0N2YzXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",
        "https://fr.web.img2.acsta.net/medias/nmedia/18/72/34/14/19476654.jpg"
        ],
        titles=[f"Image #{str(i)}" for i in range(5)],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
	    ) 
        st.dataframe(top10_30y, use_container_width=True)
        
elif tabs == 'KPI':
    '''
# KPI à suivre :bar_chart:
    '''
    col1, col2, col3 = st.columns(3)
    col1.metric("Durée moyenne des films 2022", "93 minutes")
    col2.metric("Note moyenne des films 2022", "7.5 étoiles")
    col3.metric("Nombre de votants moyen sur IMDb en 2022", "95766 votants")
    
    '''
    ##### Classement des genres de films pour 2022 :
    '''
    with st.expander("Top genres 2022 :"):
        kpi_graph = go.Figure(go.Treemap(
        values=graph2022.values,
        labels=graph2022.index,
        parents=["Genres 2022"] * len(graph2022.index),
        textinfo = "label+value+percent root",
        textposition='middle center',
        hoverinfo = 'skip',
        texttemplate='<b>%{label}</b><br>%{value} films<br>Ratio : %{percentRoot}',
        insidetextfont=dict(size=16),
        marker=dict(
            colorscale='Viridis'),
            ))
    
        kpi_graph.update_layout(margin = dict(t=0, l=0, r=0, b=0),
        height=630,
        )
        st.plotly_chart(kpi_graph, use_container_width=True)
        st.metric(label="Genre le plus représenté", value="Drama avec 27%")
        '''
        Pour l'année passée, le genre Drama continue d'occuper une place importante avec un pourcentage de **27%**, 
        suivi par la *comédie* et l'*action*, au coude à coude avec **11%**. 
        '''
    
    '''
    En observant ces KPI, il semble pertinent pour le directeur du cinema de se concentrer sur des films répondants au maximum à **ces caractéristiques**. 
    
    En effet, cela permettrait au cinema de prévoir un nombre de séance compris entre **5 et 7 par salle** et de projeter des films touchant le plus large publique possible. 
    Toujours dans le but d’augmenter la rentabilité du cinema et de pérenniser l’activité commerciale.
    
    ##### Quelques exemples de films de 2022 que notre cinéma pourrait projeter :
    '''
    
    with st.expander("Top 10 films 2022 :"):
        st.markdown("<h1 style='text-align: center; color: black;'>Top 10 2022</h1>", unsafe_allow_html=True)
    
        clicked = clickable_images(
        [
        "https://m.media-amazon.com/images/M/MV5BYzJkZDIwYTAtMGU4Mi00NzU3LWI1MWItODg0M2Q1NmIxYmNlXkEyXkFqcGdeQXVyMTIyNzY0NTMx._V1_.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/pv-target-images/f5a21f64af7359f7aaa7c29dee8a12a97630e707cdbf71e0ae6b063322fb8575._RI_TTW_.jpg",
        "https://fr.web.img3.acsta.net/pictures/22/03/29/15/12/0827894.jpg",
        "https://m.media-amazon.com/images/M/MV5BNjMyMDBjMGUtNDUzZi00N2MwLTg1MjItZTk2MDE1OTZmNTYxXkEyXkFqcGdeQXVyMTQ5NjA0NDM0._V1_.jpg",
        "https://fr.web.img6.acsta.net/pictures/22/06/14/16/36/2606624.jpg",
        "https://m.media-amazon.com/images/M/MV5BMDdmMTBiNTYtMDIzNi00NGVlLWIzMDYtZTk3MTQ3NGQxZGEwXkEyXkFqcGdeQXVyMzMwOTU5MDk@._V1_.jpg",
        "https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_FMjpg_UX1000_.jpg",
        "https://m.media-amazon.com/images/M/MV5BMzM4ZDJhYjYtZGY5Ny00NTk0LWI4ZTYtNjczZDFiMGI2ZjEzXkEyXkFqcGdeQXVyNjc5NjEzNA@@._V1_FMjpg_UX1000_.jpg",
        "https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_FMjpg_UX1000_.jpg",
        "https://fr.web.img6.acsta.net/pictures/22/11/21/09/41/4024615.jpg"
        ],
        titles=[f"Image #{str(i)}" for i in range(5)],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
	    )
        st.dataframe(kpi_22, use_container_width=True)
    
elif tabs == 'Machine Learning':
    '''
# Machine Learning :robot_face:
    '''
    algotest3 = pd.read_csv("/Users/tony/Desktop/StreamLit/dfalgotest2.csv")
    algotest3.index = algotest3["title"]
    algotest3 = algotest3.loc[algotest3["numVotes"]>=100000]
    X2 = algotest3.select_dtypes("number").drop(["numVotes","startYear","runtimeMinutes"],axis=1)
    start_years = algotest3['startYear'].unique()
    
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
          'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir',
          'History', 'Horror', 'Music', 'Musical', 'Mystery',
          'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    
    selected_genres = st.multiselect("Quel est votre genre de film préféré ?", genres, key="unique_key")
    
    selected_start_year_range = st.slider(
    "Quelle plage de date de sortie des films souhaitez vous ?",
    min_value=int(start_years.min()),
    max_value=int(start_years.max()),
    value=(int(start_years.min()), int(start_years.max()))
	)
    
    filtered_movies = algotest3[
    (algotest3['startYear'] >= selected_start_year_range[0]) &
    (algotest3['startYear'] <= selected_start_year_range[1])
	]
    
    for genre in selected_genres: filtered_movies = filtered_movies[filtered_movies[genre] == 1]
    
    option = st.selectbox("Quel est le film que vous aimez?", filtered_movies)
    
    modelNN2 = NearestNeighbors(n_neighbors=5).fit(X2)
    filmchoisi2 = X2.loc[option]
    filmchoisi2_array = np.array(filmchoisi2)
    filmchoisi2_reshaped = filmchoisi2_array.reshape(1,-1)
    
    modelNN2.kneighbors(filmchoisi2_reshaped,
                    n_neighbors=15)
    
    neigh_dist, neigh_index = modelNN2.kneighbors(filmchoisi2_reshaped,
    n_neighbors=15
	)
    
    neigh_index2 = neigh_index[0][1:]
    voisins = pd.DataFrame(algotest3.iloc[neigh_index2])
    voisins["imdb_link"] = voisins["tconst"].apply(lambda x: f"https://www.imdb.com/title/{x}/")
    columns = ["genres","averageRating","numVotes","imdb_link"]
    voisinscol = voisins[columns]
    voisinscol["imdb_link"] = voisinscol["imdb_link"].apply(make_clickable)
    html_table = voisinscol.to_html(escape=False)
    html_table_with_links = html_table.replace("&lt;", "<").replace("&gt;", ">")
    
    with st.spinner('Patience jeune Padawan...'):
        time.sleep(2.5)
    
    st.success('It''s movie time!')
    
    st.write("Vos films recommandés:")
    
    st.markdown(html_table_with_links, unsafe_allow_html=True)

elif tabs == "Axes d'amélioration":
    '''
    # Axes d'amélioration de notre livrable :white_check_mark:
    '''
    col1, col2, col3 = st.columns(3)
    with col1 :	
        st.image("https://www.netheos.com/wp-content/uploads/2017/11/machine-learning.jpg")
        st.header("Machine Learning :robot_face:")
        st.write("Bien que les films proposés soient pertinents, il aurait été possible avec plus de temps et une meilleure maîtrise de l'outil, d'améliorer la qualité des sorties en fonction des paramètres choisis. Cela est d'autant plus vrai que notre client a de grandes ambitions.")
    with col2 : 
        st.image("https://assets.website-files.com/62010c298ad50e2f90f75c5f/635f5ec9c8f1b246e8b45fda_what%20is%20kpi%20featured.png")
        st.header("KPI :chart_with_upwards_trend:")
        st.write("Le choix des indicateurs clefs de performance a été fait de manière arbitraire par manque d'informations sur le public visé. En effet, nous n'avons pu établir une liste de critères sur les potentiels clients se trouvant en Creuse. Un système de recommandation généraliste a donc été établi.")
    with col3 :	
        st.image("https://cdn.analyticsvidhya.com/wp-content/uploads/2021/06/39595st.jpeg", width=400)
        st.header("Interface :globe_with_meridians:")
        st.write("Avec une expérience réduite du framework Streamlit, nous avons pu établir une interface utilisateur et des dataviz de qualités. En ayant une meilleure connaissance de l'outil et des bases en CSS, il aurait été possible d'obtenir un rendu visuel plus optimisé.")

elif tabs == 'Difficultées':
    '''
    # Difficultés rencontrées pendant le projet :x:
	'''
    st.header("Le temps :stopwatch:")
    st.write("Le temps nous a fait défaut, ce qui nous a freiné dans notre apprentissage des outils nécessaires à la réalisation du projet. Par ce fait, nous n'avons pu aller au bout de nos idées, comme la création d'une newsletter pour les clients. Cela aurait pu servir à leur proposer d'autres films en fonction de leurs préférences cinématographiques, centres d'intérêts et ainsi les fidéliser.")

    st.header("Organisation du projet :date:")
    st.write("Le manque d'organisation au début du projet nous a également fait perdre du temps, tout la résolution imprévus de problèmes techniques.")

    st.header("Technique :computer:")
    st.write("Le travail sur Visual Studio Code en local impose un partage des fichiers réguliers auprès des autres membres de l'équipe et empèche d'avoir un visu instantané sur l'avancement de chacun. Il aurait été préférable de travailler sur un outil colaboratif du type Git afin que chacun puisse avancer au même rythme que le reste de l'équipe ou du moins pouvoir jaugé l'avancement du projet en direct.")
