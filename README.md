<div align="center">
  <center><h1>Project 2 - IMDb :</h1></center>
</div>


Projet de groupe réalisé dans le cadre de la formation de DATA ANALYST à la Wild Code School de Nantes. A partir de la base de données issue d'IMDb, nous devions extraire, filtrer, nettoyer et traiter les données afin de définir une orientation commercial cohérente pour un cinéma en perte de vitesse et situé dans le département de la Creuse.

## Plusieurs axes d'étude pour la réalisation de ce projet :

- Etude du département de la Creuse. 
- Etude des tendances du marché du cinéma. 
- Définition de KPI pour le suivi commercial du cinéma. 
- Réalisation d'un algorithme de recommandation de film.

### Etude du département de la Creuse :

Pour réalisé cette étude, nous nous sommes basés sur les données disponibles sur le site de l'INSEE afin d'établir un constat de la population de la Creuse en terme de densité, nombre d'habitants, age moyen.
Ces données nous ont permis d'avoir un oeil plus avisé sur le potentiel publique du cinéma pour lequel nous travaillons.

Nous avons représentés les données sous forme de Datavisualisation ainsi que de Metrics importantes.

Le code de ces représentations est le suivant :
```python
# Les données ont été rentrée en brute dans le code par soucis de rapidité

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

### Etude des tendances du marché du cinéma :

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

Il nous a paru plus judicieux de focaliser notre analyse sur les 30 dernières années afin de concervé la cohérence d'une étude de marché pour un directeur de cinéma.

Le code de ces représentations est le suivant :
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
