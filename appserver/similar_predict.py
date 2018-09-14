#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 16:48:00 2018

@author: shanthakumarp
"""

import pandas as pd
import csv, json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings

count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')


def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

def get_recommendations_by_budget(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    
    recommended_movies = df.iloc[movie_indices][['title','budget']]
    movie = df.iloc[idx][['title','budget']]
    movie_budget = float(movie.budget)
    recommended_movies['budget_sim'] = recommended_movies['budget'].apply(lambda x: 1 - abs((float(x)-movie_budget)/20))
    recommended_movies = recommended_movies.sort_values('budget_sim', ascending=False)
    return recommended_movies


# reco_wo_bd = get_recommendations('Aruvi').head(10)


# reco_budget = get_recommendations_by_budget('Aruvi').head(10)




def get_similar(request,  **data):
    title = data['title']
    production = data['production']
    release_year = data['release_year']
    genre1 = data['genre1']
    genre2 = data['genre2']
    genre3 = data['genre3']
    director1 = data['director1']
    director2 = data['director2']
    actor1 = data['actor1']
    actor2 = data['actor2']
    actor3 = data['actor3']
    budget = data['budget']
    production_country = data['production_country']

    fields=[title,production,release_year,genre1,genre2,genre3,director1,director2,actor1,actor2,actor3,budget,production_country]

    f_name = settings.SOURCE_FILE #'/home/local/TAG/shanthakumarp/projects/Data_science_projecs/similar_movie/similarMovies/appserver/moviesData_test2.csv'

    dfOriginal = pd.read_csv(f_name)


    with open(f_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


    df = pd.read_csv(f_name)

    df['genre']=df['genre1'].astype(str)+','+df['genre2'].astype(str)+','+df['genre3'].astype(str)
    df['directors']=df['director1'].astype(str)+','+df['director2'].astype(str)
    df['actors']=df['actor1'].astype(str)+','+df['actor2'].astype(str)+','+df['actor3'].astype(str)

    df.drop(['genre1','genre2','genre3','director1','director2','actor1','actor2','actor3'], axis=1, inplace = True)

    df['actors'] = df['actors'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
    df['genre'] = df['genre'].apply(lambda x: str.lower(x.replace(" ", "")))
    df['directors'] = df['directors'].apply(lambda x: str.lower(x.replace(" ", "")))
    df['production'] = df['production'].astype(str).apply(lambda x: str.lower(x.replace(" ", "")))
    df['production_country'] = df['production_country'].astype(str).apply(lambda x: str.lower(x.replace(" ", "")))


    df['soup'] = df['actors'] +" "+ df['directors'] +" "+ df['genre']+" "+df['production']+" "+df['production_country']

    df['soup']= df['soup'].astype('str').apply(lambda x: str.lower(x.replace(",", " ")))


    count_matrix = count.fit_transform(df['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    df = df.reset_index()
    titles = df['title']
    indices = pd.Series(df.index, index=df['title'])

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    recommend_data =  titles.iloc[movie_indices]

    #print "recommend data --->", recommend_data

    dfOriginal.to_csv(f_name, index=False)

    return {"result":recommend_data}