<div align="center">
  <center><h1>Project 2 - IMDb :</h1></center>
</div>


Projet de groupe réalisé dans le cadre de la formation de DATA ANALYST à la Wild Code School de Nantes. A partir de la base de données issue d'IMDb, nous devions extraire, filtrer, nettoyer et traiter les données afin de définir une orientation commercial cohérente pour un cinéma en perte de vitesse et situé dans le département de la Creuse.

# Pour avoir accès à notre livrable web : 
https://tch-gitprojects-project-2-wcs-streamlit-app-f30yon.streamlit.app/

# Plusieurs axes d'étude pour la réalisation de ce projet :

- Etude du département de la Creuse. 
- Etude des tendances du marché du cinéma. 
- Définition de KPI pour le suivi commercial du cinéma. 
- Réalisation d'un algorithme de recommandation de film.

# Etude du département de la Creuse :

Pour réalisé cette étude, nous nous sommes basés sur les données disponibles sur le site de l'INSEE afin d'établir un constat de la population de la Creuse en terme de densité, nombre d'habitants, age moyen.
Ces données nous ont permis d'avoir un oeil plus avisé sur le potentiel publique du cinéma pour lequel nous travaillons.

Nous avons représentés les données sous forme de Datavisualisation ainsi que de Metrics importantes.

Le code de ces représentations est le suivant :
```python
# Les données ont été rentrées en brute dans le code par soucis de rapidité

# Représentation des Metrics importants sous forme de colonnes pour une meilleure visibilité sur le livrable
    col1, col2 = st.columns(2)
    col1.metric(label="Population totale de la Creuse", value="115 995 habitants en 2020", delta="-3,8% par rapport à 2014")
    col2.metric("Age moyen", "58 ans en 2020", delta="+6 ans par rapport à 2014",
    delta_color="inverse")

# Code de la réprésentation, sous forme de Pie Chart, de la répartition de la population de la Creuse par tranche d'age
# Code écrit en JS via la librairie st_echarts
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
```

# Etude des tendances du marché du cinéma :

Pour cette étude, nous avons utilisé la base de données en open source de IMDb disponible sur ce lien https://developer.imdb.com/non-commercial-datasets/.

Il a été nécessaire d'utiliser différents filtrages, de nettoyer ainsi que de joindre les différents Dataframe afin d'obtenir les informations dont nous avions besoin pour réaliser une étude du marché du cinéma qui soit à la fois cohérente, juste, et surtout qui réponde aux besoins qu'un directeur de cinéma pourrait avoir.

Quelques exemples de code utilisé pour réaliser ces actions :
```python
# Lecture des différents fichiers présent sur IMDb sous formes de tsv

ratings = pd.read_csv("https://datasets.imdbws.com/title.ratings.tsv.gz", sep="\t",low_memory=False)
actorslist = pd.read_csv("https://datasets.imdbws.com/title.principals.tsv.gz", sep="\t",low_memory=False)
title_akas = pd.read_csv("https://datasets.imdbws.com/title.akas.tsv.gz", sep="\t",low_memory=False)
name_basics = pd.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz", sep="\t",low_memory=False)
title_basic = pd.read_csv("https://datasets.imdbws.com/title.basics.tsv.gz", sep="\t",low_memory=False)

# Quelques exemples de filtrage des TSV afin d'obtenir les données qui nous intéresse pour notre étude de marché

# Acteurs, Actrices, Réalisateurs
actors_male_female = actorslist.loc[actorslist["category"].str.contains("director|actress|actor")]

# Films qui ne sont pas pour Adulte uniquement
title_basic_mov = title_basic[(title_basic["titleType"]== "movie") & (title_basic["isAdult"]=="0")]

# Récupération des films sorties dans un pays francophone
title_aka_fr = title_akas[title_akas["region"] == "FR"]

# Filtrage sur les notes, durées, nombre de votants ainsi que création d'une matrice creuse pour les genres de nos films
tconstmovs = imdbmovs.loc[(imdbmovs["averageRating"]>=6) & (imdbmovs["runtimeMinutes"]>=60) & (imdbmovs["numVotes"]>=10000)]
tconstmovs["genres"].str.get_dummies(sep=",").sum().sort_values(ascending=False).head(10)

# Quelques exemples de jointures tables
actors = pd.merge(actors_male_female,
                       name_basics,
                       how = "inner",
                       left_on = "nconst",
                       right_on = "nconst")
                       
imdbmovs2 = pd.merge(imdbmovs,
                       actors,
                       how = "inner",
                       left_on = "tconst",
                       right_on = "tconst")
```

A la fin de nos manipulations de données, nous avons pu produire deux Dataframe à partir desquels nous avons produits notre étude de marché et nos Datavisualisations ainsi que nos Metrics importantes.

Il nous a paru plus judicieux de focaliser notre analyse sur les 30 dernières années afin de concerver la cohérence d'une étude de marché pour un directeur de cinéma.

Une partie du code de ces représentations :
```python
# Utilisation des expander de StreamLit pour une meilleure lecture de notre site

 with st.expander("Moyenne de la durée et répartition par genres :"):
 
# Utilisation de la librairie Plotly Express avec le module go pour plus de personalisations des graphiques, ici une Treemap des genres
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
    
# Utilisation de la librairie Plotly Express pour un Line chart de l'évolution de la durée des films sur les 30 dernières années
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
```

# Définition de KPI pour le suivi commercial du cinéma :

Pour la réalisation des différents KPI de suivi, nous avons choisi l'année passée (2022) afin de pouvoir comparer l'évolution du cinéma en cours d'année 2023 et voir si notre offre de films répond bien aux évolutions du marché ainsi qu'a la demande du publique.

Pour ce faire, nous avons utilisé les Dataframe obtenus après filtrage et appliqué un filtre supplémentaire pour obtenir uniquement les données de 2022.

Nous avons ensuite réalisé les différents Metrics et Datavisualisations avec le même principe que pour l'exploration de données.

Exemples :
```python
# Treemap des genres pour l'année 2022 
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
   
# Scrapping manuel des affiches des films du top 10 2022 pour affichage sur notre livrable
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
```

# Réalisation d'un algorithme de recommandation de film :

Pour répondre à la demande du directeur de cinéma, nous avons réalisé un système de recommandation de films.
Celui-ci est en phase de test et permet à l'heure actuel de fournir une liste de recommandation selon un film choisi par l'utilisateur.

Il est prévu à terme (fictif) que ce système de recommandation soit automatisé selon le film vu par le client et qu'il envoi directement les recommandations au client via son adresse e-mail à chaque fois que celui ci vient voir un film au cinéma.

La base de données utilisé pour la réalisation de ce système de recommandation comprend un csv avec une matrice creuse des genres ainsi que des acteurs principaux. 

Il est possible via notre livrable de filtrer les films par genre ainsi que par plage d'années afin d'obtenir une sélection de films plus précise et de contourner le problème des poids dans l'agorithme KNN Nearest Neighbors.

Voici le code de notre algorithme :
```python
# Lecture du CSV utilisé pour l'algorithme (Filtrage avec films > 60 minutes, > 6 average_ratings, > 100.000 numVotes)
    algo = pd.read_csv("https://raw.githubusercontent.com/TCH-Gitprojects/Project-2-WCS/main/StreamLit/dfalgotest2.csv")
# Changement de l'index par le titre des films en FR
    algo.index = algo["title"]
    algo = algo.loc[algo["numVotes"]>=100000]
# Définition du X pour l'algorithme, choix de drop les colonnes numVotes, startYear et runtimeMinutes qui ne sont pas assez corrélées pour un résultat probant
    X = algo.select_dtypes("number").drop(["numVotes","startYear","runtimeMinutes"],axis=1)
    start_years = algo['startYear'].unique()
    
# Création du selecteur de genres pour le livrable
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
          'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir',
          'History', 'Horror', 'Music', 'Musical', 'Mystery',
          'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    
    selected_genres = st.multiselect("Quel est votre genre de film préféré ?", genres, key="unique_key")

# Création du selecteur de plage d'années pour le livrable
    selected_start_year_range = st.slider(
    "Quelle plage de date de sortie des films souhaitez vous ?",
    min_value=int(start_years.min()),
    max_value=int(start_years.max()),
    value=(int(start_years.min()), int(start_years.max()))
	)
    
    filtered_movies = algo[
    (algo['startYear'] >= selected_start_year_range[0]) &
    (algo['startYear'] <= selected_start_year_range[1])
	]
    
    for genre in selected_genres: filtered_movies = filtered_movies[filtered_movies[genre] == 1]
    
# Création du selecteur de film pour l'algorithme
    option = st.selectbox("Quel est le film que vous aimez?", filtered_movies)

# Utilisation de l'algo NearestNeighbors
    modelNN = NearestNeighbors(n_neighbors=5).fit(X)
    filmchoisi = X.loc[option]
    filmchoisi_array = np.array(filmchoisi)
    filmchoisi_reshaped = filmchoisi_array.reshape(1,-1)
    
    modelNN.kneighbors(filmchoisi_reshaped,
                    n_neighbors=15)
    
    neigh_dist, neigh_index = modelNN.kneighbors(filmchoisi_reshaped,
    n_neighbors=15
	)

# Affichage des résultats sous forme de dataframe avec lien IMDb cliquable
    neigh_index2 = neigh_index[0][1:]
    voisins = pd.DataFrame(algo.iloc[neigh_index2])
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
```

# L'équipe ayant réalisé ce projet :

<p>https://www.linkedin.com/in/tonychatri/<br>
https://www.linkedin.com/in/lucas-zubiarrain/<br>
https://www.linkedin.com/in/tabitha-corazon/<br>
https://www.linkedin.com/in/emmanuel-balthazar-1420ab252/</p>

<div align="center">
  <center><h1>Merci à tous</h1></center>
</div>

