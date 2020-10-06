#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import time
import datetime 
from datetime import datetime
from datetime import date
import dateutil
from dateutil.parser import parse
import babel
import flask
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Table, Column, Integer, String,ForeignKey,func,funcfilter
from sqlalchemy import select, join
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import backref
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from model import Venue,Artist,Shows,app,moment,migrate,db 

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # time_now = date.today()
  # dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"                                                     
  return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  

    data = db.session.query(Venue)

    return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_venues = request.form.get('search_term', '')    
  look_for = '%{}%'.format(search_venues)
  count = db.session.query(Venue).filter(Venue.name.ilike(look_for)).count()
  data = db.session.query(Venue.id,Venue.name).filter(Venue.name.ilike(look_for)).all()

  
  return render_template('pages/search_venues.html', results_count=count ,results=data, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

   
  query1 = db.session.query(Venue).filter(Venue.id == venue_id)
  query2 = db.session.query(Shows.artist_id,Shows.venue_id,Artist.image_link,Artist.name,Shows.start_time).join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time <= datetime.now())
  query3 = db.session.query(Shows.artist_id,Shows.venue_id,Artist.image_link,Artist.name,Shows.start_time).join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time >= datetime.now())
  PastShows = db.session.query(func.count(Shows.id).label('PastShows')).filter(Shows.venue_id==venue_id).filter(Shows.start_time <= datetime.now()).scalar()
  UpcomingShows = db.session.query(func.count(Shows.id).label('UpcomingShows')).filter(Shows.venue_id==venue_id).filter(Shows.start_time >= datetime.now()).scalar()
  db.session.close()
  return render_template('pages/show_venue.html', venues=query1,pastshows=query2,upcomingshows=query3,past_shows_count=PastShows,upcoming_shows_count=UpcomingShows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  try:
  # data = request.get_json()
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link'] 

    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link)
    print(venue)
    db.session.add(venue)
    db.session.commit()
    db.session.close()
  
  except: 
      error = True
      db.session.rollback()
      print(sys.exc_info())
      if error:
        flask.abort(400)
      else:
        flash('Venue ' + name + ' was successfully listed!')
        return flask.jsonify(venue)
  finally:
    db.session.close()
  return render_template('pages/home.html')

  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + name + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
    

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  try:
    db.session.query(Shows).filter(Shows.venue_id == venue_id).delete(synchronize_session=False)
    db.session.query(Venue).filter(Venue.id == venue_id).delete(synchronize_session=False)
    
    db.session.commit()
  except SQLAlchemyError as e:
    reason=str(e)
    print("ErroR:"+reason)
    db.session.rollback()
  finally:
    db.session.close()

    
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_artists = request.form.get('search_term', '')    
  look_for = '%{}%'.format(search_artists)
  count = db.session.query(Artist).filter(Artist.name.ilike(look_for)).count()
  data = db.session.query(Artist.id,Artist.name).filter(Artist.name.ilike(look_for)).all()

  return render_template('pages/search_artists.html', results_count=count ,results=data, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  query1 = db.session.query(Artist).filter(Artist.id==artist_id)     
  query2 = db.session.query(Shows.artist_id,Shows.venue_id,Venue.image_link,Venue.name,Shows.start_time).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time <= datetime.now())
  query3 = db.session.query(Shows.artist_id,Shows.venue_id,Venue.image_link,Venue.name,Shows.start_time).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time >= datetime.now())
  PastShows = db.session.query(func.count(Shows.id).label('PastShows')).filter(Shows.artist_id==artist_id).filter(Shows.start_time <= datetime.now()).scalar()
  UpcomingShows = db.session.query(func.count(Shows.id).label('UpcomingShows')).filter(Shows.artist_id==artist_id).filter(Shows.start_time >= datetime.now()).scalar()
  db.session.commit()
  db.session.close()
  return render_template('pages/show_artist.html', Artist=query1,pastshows=query2,upcomingshows=query3,past_shows_count=PastShows,upcoming_shows_count=UpcomingShows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # TODO: populate form with fields from artist with ID <artist_id>
  data = db.session.query(Artist).filter(Artist.id==artist_id)
  
  return render_template('forms/edit_artist.html',form=form, Artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  try:
  # called upon submitting the new artist listing form
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
  # TODO: insert form data as a new Venue record in the db, instead
    
    Artist.query.filter(Artist.id==artist_id).update({Artist.name:name,Artist.city:city,Artist.state:state,Artist.phone:phone,Artist.genres:genres,Artist.image_link:image_link,Artist.facebook_link:facebook_link})
    db.session.commit()
    db.session.close()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
    if error:
      flask.abort(400)
    else:
      flash('Artist ' + name + ' was successfully updated!')
      
  finally:
    db.session.close()
    
    # artist record with ID <artist_id> using the new attributes
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  # TODO: populate form with values from venue with ID <venue_id>
  data = db.session.query(Venue).filter(Venue.id==venue_id)

  return render_template('forms/edit_venue.html', form=form, Venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
  # called upon submitting the new Venue listing form
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    address = request.get_json()['address']
    seeking_talent = request.get_json()['seeking_talent']
    seeking_description = request.get_json()['seeking_description']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
  # TODO: insert form data as a new Venue record in the db, instead    
        
    Venue.query.filter(Venue.id==venue_id).update({Venue.name:name,Venue.city:city,Venue.state:state,Venue.address:address,Venue.phone:phone,Venue.image_link:image_link,Venue.facebook_link:facebook_link,Venue.seeking_talent:seeking_talent,Venue.seeking_description:seeking_description})
    db.session.commit()
    db.session.close()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
    if error:
      flask.abort(400)
    else:
      flash('Venue ' + name + ' was successfully updated!')
      
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
  # called upon submitting the new artist listing form
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
  # TODO: insert form data as a new Venue record in the db, instead

    artist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link)
    db.session.add(artist)
    db.session.commit()
    db.session.close()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
    if error:
      flask.abort(400)
    else:
      flash('Artist ' + name + ' was successfully listed!')
      return flask.jsonify(artist)
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
 
  data = db.session.query(Shows.start_time,Artist.image_link.label("artist_image_link"),Artist.name,Venue.name.label("venue_name")).join(Artist).join(Venue)
  db.session.commit()
  db.session.close()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    artist_id = request.get_json()['artist_id']
    venue_id = request.get_json()['venue_id']
    start_time = request.get_json()['start_time']
    shows = Shows(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    db.session.add(shows)
    db.session.commit()
    db.session.close()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    if error:
      flask.abort(400)
    else:
      return flask.jsonify(shows)
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
