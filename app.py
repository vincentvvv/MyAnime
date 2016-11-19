import os
import sys
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Anime, Tag, tags

app = Flask(__name__)

engine = create_engine('sqlite:///listofanime.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# root path of application
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/anime/JSON')
def animeJSON():
    animes = session.query(Anime).all()
    return jsonify(animes=[a.serialize for a in animes])


# Show all Anime
@app.route('/')
@app.route('/anime')
def listAnime():
    animes = session.query(Anime).all()
    return render_template('animes.html', animes=animes)

@app.route('/anime/<string:tag_name>')
def listByTag(tag_name):
    theTags = session.query(tags).filter_by(tag_name=tag_name)
    animes = session.query(Anime)
    for tag in theTags:
        animes = animes.filter(Anime.tags.any(Tag.name == tag.tag_name))
    return render_template('listTags.html', animes=animes, tag_name=tag_name)

# Create a new Anime
@app.route('/anime/new/', methods=['GET', 'POST'])
def newAnime():
    if request.method == 'POST':
        destination   = ""
        imageLocation = os.path.join(APP_ROOT, 'static/images/')

        newAnime = Anime(name=request.form['name'], 
                         episodes=request.form['episodes'],
                         description=request.form['description'])

        for img in request.files.getlist("file"):
            filename = ""
            # No file was uploaded
            if img.filename == "":
                filename = "tmp.png"
                newAnime.image = filename
            # File was upload
            else:
                filename = newAnime.name + ".png"
                destination = "/".join([imageLocation, filename])
                img.save(destination)
                newAnime.image = filename  

        tags = []
        tags_from_form = request.form.getlist('tags')
        for tag in tags_from_form:
            t = session.query(Tag).filter_by(name=tag).one()
            tags.append(t)
        newAnime.tags = tags
        session.add(newAnime)
        session.commit()
        return redirect(url_for('listAnime'))
    else:
        return render_template('newAnime.html')

# Edit a Anime
@app.route('/anime/<int:anime_id>/edit/', methods=['GET', 'POST'])
def editAnime(anime_id):
    anime = session.query(Anime).filter_by(id=anime_id).one()
    if request.method == 'POST':
        destination   = ""
        imageLocation = os.path.join(APP_ROOT, 'static/images/')

        if (request.form['name'] != anime.name):
            anime.name = request.form['name']
        if (request.form['episodes'] != anime.episodes):
            anime.episodes = request.form['episodes']
        if (request.form['description'] != anime.description):
            anime.description = request.form['description']

        for img in request.files.getlist("file"):
            # file was uploaded
            if img.filename != "":
                filename = anime.name + ".png"
                destination = "/".join([imageLocation, filename])
                img.save(destination)
                anime.image = filename

        tags = []
        tags_from_form = request.form.getlist('tags')
        for tag in tags_from_form:
            t = session.query(Tag).filter_by(name=tag).one()
            tags.append(t)
        anime.tags = tags
        session.commit()
        return redirect(url_for('listAnime'))
    else:
        return render_template('editAnime.html', anime=anime)

# Delete a Anime
@app.route('/anime/<int:anime_id>/delete/', methods=['GET', 'POST'])
def deleteAnime(anime_id):
    animeToDelete = session.query(Anime).filter_by(id=anime_id).one()
    if request.method == 'POST':
        imageLocation = os.path.join(APP_ROOT, 'static/images/')
        fileLocation = "/".join([imageLocation, animeToDelete.image])
        os.remove(fileLocation)
        session.delete(animeToDelete)
        session.commit()
        return redirect(url_for('listAnime'))
    else:
        return render_template('deleteAnime.html', anime=animeToDelete)

# View Anime
@app.route('/anime/<int:anime_id>/')
def viewAnime(anime_id):
    anime = session.query(Anime).filter_by(id=anime_id).one()
    return render_template('anime_view.html', anime=anime)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
