
from flask import Blueprint, make_response, render_template, url_for

blueprint = Blueprint(
    'darter',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/')
def home():
    r = make_response(render_template(
        'home.html',
        rq_url_prefix=url_for('.home')
    ))
    r.headers.set('Cache-Control', 'no-store')
    return r

