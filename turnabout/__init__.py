from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid, authenticated_userid
from pyramid.security import has_permission

from sqlalchemy import engine_from_config

import locale

from .models import (
    DBSession,
    Base,
    )


def configure_routes(config):
    config.add_static_view('static', 'static', cache_max_age=0)

    config.add_route('index', '/')

    config.add_route('trackers', '/tracker')
    config.add_route('tracker', '/tracker/{tracker_id}')

    config.add_route('storytypes', '/tracker/{tracker_id}/storytype')

    config.add_route('stories', '/tracker/{tracker_id}/story')
    config.add_route('story', '/tracker/{tracker_id}/story/{story_id}')

    config.add_route('comments', '/tracker/{tracker_id}/story/{story_id}/comment')
    config.add_route('comment', '/tracker/{tracker_id}/story/{story_id}/comment/{comment_id}')

    config.add_route('attachments', '/tracker/{tracker_id}/story/{story_id}/attachment')
    config.add_route('attachment', '/tracker/{tracker_id}/story/{story_id}/attachment/{attachment_id}')

    config.scan("turnabout")


def configure_templates(config):
    pass


def configure_locale(config, settings):
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')


def configure_cache(config, settings):
    try:
        cache.fast.configure_from_config(settings, "cache.fast.")
        cache.slow.configure_from_config(settings, "cache.slow.")
    except Exception:
        pass


def configure_auth(config):
    def principals(username, request):
        u = User.by_username(username)
        return ["u:"+u.username, ]#"g:"+u.category]
    config.set_authentication_policy(AuthTktAuthenticationPolicy('tuttuuttuttututu?', callback=principals, hashalg='sha512'))
    config.set_authorization_policy(ACLAuthorizationPolicy())


def configure_user(config):
    def user(request):
        from turnabout.models import User
        un = authenticated_userid(request)
        u = User.by_username(un)
        if not u:
            u = User.by_username("shish")
        if not u:
            raise Exception("Anonymous is missing")
        u.ip = "127.0.0.9"  # request.headers["REMOTE_ADDR"]
        return u
    config.add_request_method(user, property=True, reify=True)


def main(global_config, **settings):  # pragma: no cover
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    configure_routes(config)
    configure_templates(config)
    configure_locale(config, settings)
    configure_cache(config, settings)
    configure_auth(config)
    configure_user(config)

    return config.make_wsgi_app()
