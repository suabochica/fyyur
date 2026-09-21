"""Seed the database with sample data."""
from fyyur.app import app, db
from fyyur.models import Venue, Artist, Show

venues = [
    Venue(
        name='The Musical Hop',
        city='San Francisco',
        state='CA',
        address='1015 Folsom Street',
        phone='123-123-1234',
        image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
        facebook_link='https://www.facebook.com/TheMusicalHop',
        website='https://www.themusicalhop.com',
    ),
    Venue(
        name='The Dueling Pianos Bar',
        city='New York',
        state='NY',
        address='335 Delancey Street',
        phone='914-003-1132',
        image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
        facebook_link='https://www.facebook.com/theduelingpianos',
        website='https://www.theduelingpianos.com',
    ),
    Venue(
        name='Park Square Live Music & Coffee',
        city='San Francisco',
        state='CA',
        address='34 Whiskey Moore Ave',
        phone='415-000-1234',
        image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
        facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
        website='https://www.parksquarelivemusicandcoffee.com',
    ),
]

artists = [
    Artist(
        name='Guns N Petals',
        city='San Francisco',
        state='CA',
        phone='326-123-5000',
        image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
        facebook_link='https://www.facebook.com/GunsNPetals',
        website='https://www.gunsnpetalsband.com',
        genres='Rock n Roll',
    ),
    Artist(
        name='Matt Quevedo',
        city='New York',
        state='NY',
        phone='300-400-5000',
        image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
        facebook_link='https://www.facebook.com/mattquevedo923251523',
        genres='Jazz',
    ),
    Artist(
        name='The Wild Sax Band',
        city='San Francisco',
        state='CA',
        phone='432-325-5432',
        image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
        genres='Jazz,Classical',
    ),
]

with app.app_context():
    db.session.add_all(venues)
    db.session.add_all(artists)
    db.session.commit()

    v1, v2, v3 = venues
    a1, a2, a3 = artists

    shows = [
        Show(artist_id=a1.id, venue_id=v1.id, date='2019-05-21T21:30:00'),
        Show(artist_id=a2.id, venue_id=v3.id, date='2019-06-15T23:00:00'),
        Show(artist_id=a3.id, venue_id=v3.id, date='2035-04-01T20:00:00'),
        Show(artist_id=a3.id, venue_id=v3.id, date='2035-04-08T20:00:00'),
        Show(artist_id=a3.id, venue_id=v3.id, date='2035-04-15T20:00:00'),
    ]
    db.session.add_all(shows)
    db.session.commit()

    print(f'Seeded {len(venues)} venues, {len(artists)} artists, {len(shows)} shows')
