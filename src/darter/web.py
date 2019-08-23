
from flask import Blueprint, make_response, render_template, url_for
from darter.models import Capacity

blueprint = Blueprint(
    'darter',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/')
def home():
    capacity = Capacity().find_all()

    r = make_response(render_template(
        'home.html',
        rq_url_prefix=url_for('.home'),
        regions=capacity.keys(),
        capacity=capacity
    ))
    r.headers.set('Cache-Control', 'no-store')
    return r

