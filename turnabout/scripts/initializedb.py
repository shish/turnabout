import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    User,
    Tracker,
    StoryType,
    Story,
    Comment,
    Attachment,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_stub_data()


def add_stub_data():
    with transaction.manager:
        tracker = Tracker(name='tt', title=u"Test Tracker")
        DBSession.add(tracker)

        feature = StoryType(
            name=u"feature",
            tracker=tracker,
            fields={
                "points": "Integer(0, 12)",
                "state": "State(['iced:scheduled','scheduled:started'])",
                "requester": "User()",
                "owner": "User()",
                "reviewer": "User()",
                "passed_tests": "Boolean()",
            }
        )
        DBSession.add(feature)

        bug = StoryType(
            name=u"bug",
            tracker=tracker,
            fields={
                "state": "State(['iced:scheduled','scheduled:started'])",
                "requester": "User()",
                "owner": "User()",
                "reviewer": "User()",
                "passed_tests": "Boolean()",
            }
        )
        DBSession.add(bug)

        user = User(username="shish", password="")
        DBSession.add(user)

        s1 = Story(
            title=u"A Feature Story",
            description=u"""
# Markdown support!

- format your stories sanely
- *italic*, **bold**
            """,
            storytype=feature,
            tracker=tracker,
            fields={
                "points": u"3",
                "state": u"iced",
                "requester": u"shish",
            }
        )
        s1.comments.append(Comment(
            user=user,
            text=u"Comment on a feature",
        ))
        s1.attachments.append(Attachment(
            user=user,
            filename="test attachment.txt",
            data="hello world!",
            hash="x",
            mime="text/plain",
            size=0,
        ))
        DBSession.add(s1)

        s2 = Story(
            title=u"A Bug Story",
            storytype=bug,
            tracker=tracker,
            fields={
                "state": u"iced",
                "requester": u"shish",
            }
        )
        s2.comments.append(Comment(
            user=user,
            text=u"Comment on a bug",
        ))
        DBSession.add(s2)

        tracker2 = Tracker(name='t2', title=u"Other Tracker")
        DBSession.add(tracker2)

        bug2 = StoryType(
            name=u"bug",
            tracker=tracker2,
            fields={
                "state": "State(['iced:scheduled','scheduled:started'])",
                "requester": "User()",
                "owner": "User()",
            }
        )
        DBSession.add(bug2)

        s2 = Story(
            title=u"A Bug Story (in another tracker)",
            storytype=bug2,
            tracker=tracker2,
            fields={
                "state": u"iced",
                "requester": u"shish",
            }
        )
        s2.comments.append(Comment(
            user=user,
            text=u"Comment on a bug",
        ))
        DBSession.add(s2)
