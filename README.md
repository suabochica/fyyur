# Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Overview

This app is nearly complete. It is only missing one thing... real data! While the views and controllers are defined in this application, it is missing models and model interactions to be able to store retrieve, and update data from a database. By the end of this project, you should have a fully functioning site that is at least capable of doing the following, if not more, using a PostgreSQL database:

- creating new venues, artists, and creating new shows.
- searching for venues and artists.
- learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Tech Stack (Dependencies)

### 1. Backend Dependencies

- **Python >= 3.14** and **Flask 3** as our server language and server framework
- **SQLAlchemy ORM** (via Flask-SQLAlchemy) to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **psycopg 3** as the PostgreSQL adapter
- **Flask-WTF** / **WTForms** for form handling and CSRF protection
- **Flask-Moment** and **python-dateutil** for date/time handling
- **Babel** for locale-aware formatting

All dependencies are declared in `pyproject.toml` and installed via [uv](https://docs.astral.sh/uv/).

### 2. Frontend Dependencies

The frontend uses **Bootstrap 3**, **jQuery**, **Moment.js**, and **FontAwesome**. Static assets are bundled under `static/` — no build step is required.

## Project Structure

The project uses a `src`-layout. All application code lives under `src/fyyur/`:

```
├── Dockerfile.postgres        # PostgreSQL Docker image definition
├── docker-compose.yml         # Docker Compose config (PostgreSQL service)
├── pyproject.toml             # Package metadata, dependencies (uv)
├── seed.py                    # Database seed script
└── src/
    └── fyyur/
        ├── __init__.py        # Package entry point
        ├── app.py             # Flask app, all routes, filters, error handlers
        ├── config.py          # SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI
        ├── forms.py           # WTForms: VenueForm, ArtistForm, ShowForm
        ├── models.py          # SQLAlchemy models: Venue, Artist, Show + db instance
        ├── static/
        │   ├── css/            # Bootstrap 3 + custom stylesheets
        │   ├── js/             # jQuery, Moment.js, Bootstrap JS, custom
        │   ├── fonts/          # FontAwesome webfonts
        │   └── img/            # Front-page splash image
        └── templates/
            ├── errors/         # 404.html, 500.html
            ├── forms/          # new_venue, new_artist, new_show, edit_*
            ├── layouts/        # main.html, form.html (shared chrome)
            └── pages/          # Home, venues, artists, shows, search, detail
```

Key file roles:

| File                          | Role                                                                                                                        |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `app.py`                      | Flask app init, all routes/controllers, `format_datetime` Jinja filter, error handlers, logging                             |
| `models.py`                   | SQLAlchemy models (`Venue`, `Artist`, `Show`), shared `db` instance                                                         |
| `config.py`                   | `SECRET_KEY`, `DEBUG`, `SQLALCHEMY_DATABASE_URI` (defaults to local Postgres, overridable via `FYYUR_DATABASE_URI` env var) |
| `forms.py`                    | `VenueForm`, `ArtistForm`, `ShowForm` — state selects (50 US states + DC), genre multi-select (19 genres), seeking fields   |
| `templates/layouts/main.html` | Master layout — navbar with contextual search, flash messages, footer, global scripts                                       |
| `templates/pages/`            | Page-level views (extends main layout)                                                                                      |
| `templates/forms/`            | Create/edit forms for venues, artists, shows                                                                                |

> **Note:** `fabfile.py` is a legacy Fabric deployment script (Heroku) and is no longer functional. `error.log` is written only when `DEBUG=False`.

## Getting Started

### Prerequisites

- **Python >= 3.14**
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** package manager
- **Docker** (for running PostgreSQL locally)

### 1. Start the PostgreSQL database

A Docker container is the easiest way to get a local Postgres running with no extra configuration.

**Using docker compose (recommended):**

```bash
docker compose up -d
```

To stop it later:

```bash
docker compose down
```

To stop and remove the data volume:

```bash
docker compose down -v
```

**Using docker run (manual):**

```bash
docker run -d \
  --name fyyur-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fyyurdb \
  -p 5433:5432 \
  postgres:16-alpine
```

This creates a container named `fyyur-postgres` on port **5433** (to avoid clashing with any system Postgres on 5432).

To stop it later:

```bash
docker stop fyyur-postgres
```

To start it again after a reboot:

```bash
docker start fyyur-postgres
```

To enable a interactive session run the `psql` on the docker container:

```bash
docker exec -it fyyur-postgres psql -U postgres -d fyyurdb
```

### 2. Install dependencies

From the **project root** (`packages/fyyur/`):

```bash
uv sync
```

This reads `pyproject.toml` and installs everything into a local `.venv`.

### 3. Run the development server

```bash
uv run flask --app fyyur.app run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### 4. Seed the database

```bash
uv run python seed.py
```

This populates the database with sample venues, artists, and shows.

### 5. Verify the connection

```bash
uv run python -c "from fyyur.app import db; print(db.engine.url)"
# postgresql+psycopg://postgres:postgres@localhost:5433/fyyurdb
```

### Database connection details

| Key      | Value                 |
| -------- | --------------------- |
| Host     | `localhost`           |
| Port     | `5433`                |
| User     | `postgres`            |
| Password | `postgres`            |
| Database | `fyyurdb`             |
| Driver   | `psycopg` (psycopg 3) |

Override the default URI by setting the `FYYUR_DATABASE_URI` environment variable:

```bash
export FYYUR_DATABASE_URI='postgresql+psycopg://user:pass@host:port/dbname'
```

## Development Setup (UDACITY)

> The sections below are carried over from the original Udacity FSND starter and have not been updated to match the current project layout.

1. Understand the Project Structure (explained above) and where important files are located.
2. Build and run local development following the Getting Started section above.
3. Fill in the missing functionality in this application: this application currently pulls in fake data, and needs to now connect to a real database and talk to a real backend.
4. Fill out every `TODO` section throughout the codebase. We suggest going in order of the following:
   - Connect to a database in `config.py`. A project submission that uses a local database connection is fine.
   - Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. Check out the sample pages provided at /artists/1, /venues/1, and /shows for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate.
   - Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.
   - Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.
   - Implement search, powering the `/search` endpoints that serve the application's search functionalities.
   - Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.

#### Data Handling with `Flask-WTF` Forms

The starter codes use an interactive form builder library called [Flask-WTF](https://flask-wtf.readthedocs.io/). This library provides useful functionality, such as form validation and error handling. You can peruse the Show, Venue, and Artist form builders in `forms.py` file. The WTForms are instantiated in the `app.py` file. For example, in the `create_shows()` function, the Show form is instantiated from the command: `form = ShowForm()`. To manage the request from Flask-WTF form, each field from the form has a `data` attribute containing the value from user input. For example, to handle the `venue_id` data from the Venue form, you can use: `show = Show(venue_id=form.venue_id.data)`, instead of using `request.form['venue_id']`.

## Acceptance Criteria

1. The web app should be successfully connected to a PostgreSQL database. A local connection to a database on your local computer is fine.
2. There should be no use of mock data throughout the app. The data structure of the mock data per controller should be kept unmodified when satisfied by real data.
3. The application should behave just as before with mock data, but now uses real data from a real backend server, with real search functionality. For example:

- when a user submits a new artist record, the user should be able to see it populate in /artists, as well as search for the artist by name and have the search return results.
- I should be able to go to the URL `/artist/<artist-id>` to visit a particular artist's page using a unique ID per artist, and see real data about that particular artist.
- Venues should continue to be displayed in groups by city and state.
- Search should be allowed to be partial string matching and case-insensitive.
- Past shows versus Upcoming shows should be distinguished in Venue and Artist pages.
- A user should be able to click on the venue for an upcoming show in the Artist's page, and on that Venue's page, see the same show in the Venue Page's upcoming shows section.

1. As a fellow developer on this application, I should be able to run `flask db migrate`, and have my local database (once set up and created) be populated with the right tables to run this application and have it interact with my local postgres server, serving the application's needs completely with real data I can seed my local database with.

- The models should be completed (see TODOs in the `Models` section of `app.py`) and model the objects used throughout Fyyur.
- Define the models in a different file to follow [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) design principles. You can refactor the models to a new file, such as `models.py`.
- The right _type_ of relationship and parent-child dynamics between models should be accurately identified and fit the needs of this particular application.
- The relationship between the models should be accurately configured, and referential integrity amongst the models should be preserved.
- `flask db migrate` should work, and populate my local postgres database with properly configured tables for this application's objects, including proper columns, column data types, constraints, defaults, and relationships that completely satisfy the needs of this application. The proper type of relationship between venues, artists, and shows should be configured.

##### Stand Out

Looking to go above and beyond? This is the right section for you! Here are some challenges to make your submission stand out:

- Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
- Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
- Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.

Best of luck in your final project! Fyyur depends on you!

## Demo

![demo](./src/fyyur/static/img/demo.gif)

To check the tables please run:

```bash
docker exec fyyur-postgres psql -U postgres -d fyyurdb -c "SELECT * FROM \"Artist\";"
```

You will get:

```
 id |       name        |     city      | state |    phone     |     genres     |                                                              image_link                                                               |                 facebook_link                 | website
----+-------------------+---------------+-------+--------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------+---------
  2 | Matt Quevedo      | New York      | NY    | 300-400-5000 | Jazz           | https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80 | https://www.facebook.com/mattquevedo923251523 |
  3 | The Wild Sax Band | San Francisco | CA    | 432-325-5432 | Jazz,Classical | https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80    |                                               |
  1 | Guns N Plants     | San Francisco | CA    | 326-123-5000 | Classical      | https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80    | https://www.facebook.com/GunsNPetals          |
  4 | Alcolyricoz       | Miamo         | OR    | 123456765    | Alternative    |                                                                                                                                       | http://facebook.com/alcolyricoz               |

```
