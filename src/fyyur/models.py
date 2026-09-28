from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String()), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship("Show", backref="venues", lazy=False)

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"

    def upcoming_shows_count(self):
        now = datetime.now()
        return Show.query.filter(Show.venue_id == self.id, Show.date > now).count()

    def past_shows_count(self):
        now = datetime.now()
        return Show.query.filter(Show.venue_id == self.id, Show.date <= now).count()

    def get_upcoming_shows(self):
        now = datetime.now()
        return (
            db.session.query(Show, Artist)
            .join(Artist, Show.artist_id == Artist.id)
            .filter(Show.venue_id == self.id, Show.date > now)
            .order_by(Show.date.asc())
            .all()
        )

    def get_past_shows(self):
        now = datetime.now()
        return (
            db.session.query(Show, Artist)
            .join(Artist, Show.artist_id == Artist.id)
            .filter(Show.venue_id == self.id, Show.date <= now)
            .order_by(Show.date.desc())
            .all()
        )

    def format_shows(self):
        upcoming_shows = self.get_upcoming_shows()
        past_shows = self.get_past_shows()
        return {
            "upcoming_shows": [
                {
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": show.date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }
                for show, artist in upcoming_shows
            ],
            "past_shows": [
                {
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": show.date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }
                for show, artist in past_shows
            ],
            "upcoming_shows_count": len(upcoming_shows),
            "past_shows_count": len(past_shows),
        }


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship("Show", backref="artists", lazy=False)

    def __repr__(self):
        return f"<Artist {self.id} {self.name}>"

    def upcoming_shows_count(self):
        now = datetime.now()
        return Show.query.filter(Show.artist_id == self.id, Show.date > now).count()

    def past_shows_count(self):
        now = datetime.now()
        return Show.query.filter(Show.artist_id == self.id, Show.date <= now).count()

    def get_upcoming_shows(self):
        now = datetime.now()
        return (
            db.session.query(Show, Venue)
            .join(Venue, Show.venue_id == Venue.id)
            .filter(Show.artist_id == self.id, Show.date > now)
            .order_by(Show.date.asc())
            .all()
        )

    def get_past_shows(self):
        now = datetime.now()
        return (
            db.session.query(Show, Venue)
            .join(Venue, Show.venue_id == Venue.id)
            .filter(Show.artist_id == self.id, Show.date <= now)
            .order_by(Show.date.desc())
            .all()
        )

    def format_shows(self):
        upcoming_shows = self.get_upcoming_shows()
        past_shows = self.get_past_shows()
        return {
            "upcoming_shows": [
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }
                for show, venue in upcoming_shows
            ],
            "past_shows": [
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }
                for show, venue in past_shows
            ],
            "upcoming_shows_count": len(upcoming_shows),
            "past_shows_count": len(past_shows),
        }


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)

    venue = db.relationship("Venue")
    artist = db.relationship("Artist")

    def __repr__(self):
        return f"<Show {self.id} {self.date}>"

    @classmethod
    def get_all_with_artists_and_venues(cls):
        return (
            db.session.query(cls, Artist, Venue)
            .join(Artist)
            .join(Venue)
            .order_by(cls.date.desc())
            .all()
        )
