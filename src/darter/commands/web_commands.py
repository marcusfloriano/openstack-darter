# -*- coding: utf-8 -*-
import click
import rq_dashboard

from flask import Flask
from darter.web import blueprint

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


@click.group()
def web():
    pass


@web.command("server")
@click.pass_obj
def server(util):
    """Start Flask App"""
    app.register_blueprint(blueprint)
    app.run(debug=True)
