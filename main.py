from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# API to return most popular articles.
@app.route("/popular-articles")
def popular_articles():
    global popular_articles
    col_names=['original_title','poster_link','release_date','runtime','weighted_scaling']
    all_popular_recommendated_articles=pd.DataFrame(col_names)
    all_popular_recommendated_articles=all_popular_recommendated_articles.append(output)

    all_popular_recommendated_articles.drop_duplicates(subset=['original_title'])

    recommended_articles=[]
    
    for index,row in all_popular_recommendated_articles.itterows():
        _p={
            'original_title':row["original_title"],
            'poster_link':row["poster_link"],
            


        }
        all_popular_recommendated_articles.append(_p)
    return all_popular_recommendated_articles.show_rows(20) 

# API to return top 10 similar articles using content based filtering method.
@app.route("/recommended-articles")
def recommended_articles():
    global recommended_articles_articles
    col_names=['original_title','poster_link','release_date','runtime','weighted_scaling']
    recommendated_articles=pd.DataFrame(col_names)
    recommendated_articles=recommendated_articles.append(output)

    recommendated_articles.drop_duplicates(subset=['original_title'])

    recommended_articles=[]
    
    for index,row in recommendated_articles.itterows():
        _p={
            'original_title':row["original_title"],
            'poster_link':row["poster_link"],
            


        }
        recommendated_articles.append(_p)
    return recommendated_articles.show_rows(10) 
    
    return "Top 10 articles using content based filtering method"

if __name__ == "__main__":
    app.run()