import os

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from blueprints.chat import chat_bp
from blueprints.oauth import oauth_bp
from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from extensions import db, login_manager, csrf, moment, socketio, oauth
from models import User, Message
from config import config

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('app')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_commands(app)

    if not app.debug and not app.testing:
        # Log to stdout config for heroku
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/chatroom.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Chatroom startup")

    return app


def register_extensions(app):
    db.init_app(app)
    oauth.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(admin_bp)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error.html', description=e.description, code=e.code), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', description=e.description, code=e.code), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', description=e.description, code=e.code), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template("error.html", description=e.description, code=e.code), 400


def register_commands(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after dropping tables")
    def initdb(drop):
        if drop:
            click.confirm("This operation will delete the database, continue?", abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    @click.option("--message", default=300, help="Generate fake messages of a default 300 pieces")
    def forge(message):
        """Generating fake messages"""
        import random
        from sqlalchemy.exc import IntegrityError

        from faker import Faker

        fake = Faker()

        click.echo("Initializing database")
        db.drop_all()
        db.create_all()

        click.echo("Begin forging data")
        admin = User(nickname="Nate", email="n.wang1010@yahoo.ca")
        admin.set_password("flaskchatroom")
        db.session.add(admin)
        db.session.commit()

        click.echo("Generating Users")
        for i in range(50):
            user = User(
                nickname=fake.name(),
                github=fake.url(),
                website=fake.url(),
                email=fake.email()
            )
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.roll_back()

        click.echo("Generating Messages")
        for i in range(message):
            message = Message(
                author=User.query.get(random.randint(1, User.query.count())),
                body=fake.sentence(),
                timestamp=fake.date_time_between("-30d", "-2d")
            )
            db.session.add(message)

        db.session.commit()
        click.echo('Done.')

