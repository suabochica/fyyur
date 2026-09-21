#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import datetime

import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler

from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from .models import db, Venue, Artist, Show
from .forms import VenueForm, ArtistForm, ShowForm

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('fyyur.config')
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Helper functions.
#----------------------------------------------------------------------------#

def format_venue_shows(venue):
    upcoming_shows = []
    past_shows = []
    now = datetime.now()

    for show in venue.shows:
        show_data = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        }
        if show.date > now:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)

    return {
        'upcoming_shows': upcoming_shows,
        'past_shows': past_shows,
        'upcoming_shows_count': len(upcoming_shows),
        'past_shows_count': len(past_shows),
    }


def format_artist_shows(artist):
    upcoming_shows = []
    past_shows = []
    now = datetime.now()

    for show in artist.shows:
        show_data = {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        }
        if show.date > now:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)

    return {
        'upcoming_shows': upcoming_shows,
        'past_shows': past_shows,
        'upcoming_shows_count': len(upcoming_shows),
        'past_shows_count': len(past_shows),
    }

#----------------------------------------------------------------------------#
# Routes.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/venues')
def list_venues():
    venues = Venue.query.order_by(Venue.city, Venue.state, Venue.name).all()

    areas = []
    area_map = {}

    for venue in venues:
        key = (venue.city, venue.state)
        if key not in area_map:
            area_item = {
                'city': venue.city,
                'state': venue.state,
                'venues': [],
            }
            area_map[key] = area_item
            areas.append(area_item)
        area_map[key]['venues'].append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': 0,
        })

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(
        Venue.name.ilike(f'%{search_term}%')
    ).order_by(Venue.name).all()

    data = [{
        'id': v.id,
        'name': v.name,
        'num_upcoming_shows': len(v.shows),
    } for v in venues]

    return render_template(
        'pages/search_venues.html',
        results={'count': len(data), 'data': data},
        search_term=search_term,
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    shows_data = format_venue_shows(venue)

    return render_template('pages/show_venue.html', venue={
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres.split(',') if venue.genres else [],
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'image_link': venue.image_link,
        'seeking_talent': getattr(venue, 'seeking_talent', False),
        'seeking_description': getattr(venue, 'seeking_description', ''),
        **shows_data,
    })


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)

    if not form.validate():
        flash('An error occurred. Venue could not be listed.')
        return render_template('forms/new_venue.html', form=form)

    try:
        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website_link.data,
            genres=','.join(form.genres.data),
        )
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue {venue.name} was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue could not be listed.')

    return redirect(url_for('index'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(request.form)

    if not form.validate():
        flash('An error occurred. Venue could not be updated.')
        return render_template('forms/edit_venue.html', form=form, venue=venue)

    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website_link.data
        venue.genres = ','.join(form.genres.data)
        db.session.commit()
        flash(f'Venue {venue.name} was successfully updated!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Venue could not be updated.')

    return redirect(url_for('show_venue', venue_id=venue.id))


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('index'))


@app.route('/artists')
def list_artists():
    artists = Artist.query.order_by(Artist.name).all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(
        Artist.name.ilike(f'%{search_term}%')
    ).order_by(Artist.name).all()

    data = [{
        'id': a.id,
        'name': a.name,
        'num_upcoming_shows': len(a.shows),
    } for a in artists]

    return render_template(
        'pages/search_artists.html',
        results={'count': len(data), 'data': data},
        search_term=search_term,
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    shows_data = format_artist_shows(artist)

    return render_template('pages/show_artist.html', artist={
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres.split(',') if artist.genres else [],
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'image_link': artist.image_link,
        'seeking_venue': getattr(artist, 'seeking_venue', False),
        'seeking_description': getattr(artist, 'seeking_description', ''),
        **shows_data,
    })


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)

    if not form.validate():
        flash('An error occurred. Artist could not be listed.')
        return render_template('forms/new_artist.html', form=form)

    try:
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website_link.data,
            genres=','.join(form.genres.data),
        )
        db.session.add(artist)
        db.session.commit()
        flash(f'Artist {artist.name} was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Artist could not be listed.')

    return redirect(url_for('index'))


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(request.form)

    if not form.validate():
        flash('An error occurred. Artist could not be updated.')
        return render_template('forms/edit_artist.html', form=form, artist=artist)

    try:
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website = form.website_link.data
        artist.genres = ','.join(form.genres.data)
        db.session.commit()
        flash(f'Artist {artist.name} was successfully updated!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Artist could not be updated.')

    return redirect(url_for('show_artist', artist_id=artist.id))


@app.route('/shows')
def list_shows():
    shows = (
        db.session.query(Show, Artist, Venue)
        .join(Artist)
        .join(Venue)
        .order_by(Show.date.desc())
        .all()
    )

    data = [{
        'venue_id': venue.id,
        'venue_name': venue.name,
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': show.date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    } for show, artist, venue in shows]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET'])
def create_show_form():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    if not form.validate():
        flash('An error occurred. Show could not be listed.')
        return render_template('forms/new_show.html', form=form)

    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            date=form.start_time.data,
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')

    return redirect(url_for('index'))

#----------------------------------------------------------------------------#
# Error handlers.
#----------------------------------------------------------------------------#

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
