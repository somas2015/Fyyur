
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

Base = declarative_base()

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model,Base):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean(), default=False, nullable=True)
    seeking_description = db.Column(db.String(500))
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model,Base):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Artists = db.relationship("Shows")

class Shows(db.Model,Base):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id",ondelete='SET NULL'), nullable = False)   
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    venues = db.relationship("Venue",backref=db.backref("venues", passive_deletes=True,cascade="all, delete-orphan"))

    def __repr__(self):
            return '<Shows {}>'.format(self.venue_id)
        
db.create_all()