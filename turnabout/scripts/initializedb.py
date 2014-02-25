import os
import sys
import six
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
    State,
    Transition,
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


def add_default_states(s, st):
    iced = State(storytype=st, name=u"Iced", color="a2f8f3")
    scheduled = State(storytype=st, name=u"Scheduled", color="a2f8bb")
    in_progress = State(storytype=st, name=u"In Progress", color="5dde4c")
    needs_review = State(storytype=st, name=u"Needs Review", color="c3b85d")
    needs_staging_check = State(storytype=st, name=u"Needs Staging Check", color="bc8647")
    to_release = State(storytype=st, name=u"To Release", color="4770bc")
    released = State(storytype=st, name=u"Released", color="0c3176")
    wontfix = State(storytype=st, name=u"Wontfix", color="b8b8b8")

    DBSession.add(Transition(iced, scheduled, "Schedule"))
    DBSession.add(Transition(scheduled, in_progress, "Start Work"))
    DBSession.add(Transition(in_progress, needs_review, "Finish"))
    DBSession.add(Transition(needs_review, needs_staging_check, "Pass"))
    DBSession.add(Transition(needs_review, in_progress, "Fail"))
    DBSession.add(Transition(needs_staging_check, to_release, "Pass"))
    DBSession.add(Transition(needs_staging_check, in_progress, "Fail"))
    DBSession.add(Transition(to_release, released, "Release"))

    return iced


def add_stub_data():
    with transaction.manager:
        user = User(username="shish", email="webmaster@shishnet.org")
        user.set_password("test")
        DBSession.add(user)

        user = User(username="test", email="example@example.com")
        user.set_password("test")
        DBSession.add(user)

        tracker = Tracker(name='tt', title=u"Test Tracker")
        DBSession.add(tracker)

        feature = StoryType(
            name=u"Feature",
            icon="feature",
            tracker=tracker,
            fields={
                "points": "Integer(0, 12)",
                "requester": "User()",
                "owner": "User()",
                "reviewer": "User()",
                "passed_tests": "Boolean()",
                "parent": "Story()",
                "requested": "DateTime()",
            }
        )
        iced_feature = add_default_states(DBSession, feature)
        DBSession.add(feature)

        bug = StoryType(
            name=u"Bug",
            icon="bug",
            tracker=tracker,
            fields={
                "requester": "User()",
                "owner": "User()",
                "reviewer": "User()",
                "passed_tests": "Boolean()",
                "bug in": "Story()",
            }
        )
        iced_bug = add_default_states(DBSession, bug)
        DBSession.add(bug)

        epic = StoryType(
            name=u"Epic",
            icon="epic",
            tracker=tracker,
            fields={
                "due": "Date()",
            }
        )
        iced = State(storytype=epic, name=u"Iced", color="a2f8f3")
        in_progress = State(storytype=epic, name=u"In Progress", color="5dde4c")
        finished = State(storytype=epic, name=u"Finished", color="0c3176")
        DBSession.add(Transition(iced, in_progress, "Start"))
        DBSession.add(Transition(in_progress, finished, "Finish"))
        DBSession.add(epic)

        se = Story(
            title=u"Take Over The World",
            storytype=epic,
            state=iced,
            tracker=tracker,
            rank=100,
        )
        DBSession.add(se)
        DBSession.flush()

        s1 = Story(
            title=u"A Feature Story",
            description=u"""
# Markdown support!

- format your stories sanely
- *italic*, **bold**
            """,
            storytype=feature,
            state=iced_feature,
            tracker=tracker,
            rank=2000,
            fields={
                "parent": six.text_type(se.story_id),
                "points": u"3",
                "state": u"Needs Review",
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
            data=six.binary_type("hello world!", "utf8") if six.PY3 else six.binary_type("hello world!"),
            thumbnail=six.binary_type("thumb", "utf8") if six.PY3 else six.binary_type("thumb"),
            hash="x",
            mime="text/plain",
            size=0,
        ))
        DBSession.add(s1)
        DBSession.flush()

        s2 = Story(
            title=u"A Bug Story",
            storytype=bug,
            state=iced_bug,
            tracker=tracker,
            rank=1000,
            fields={
                "state": u"In Progress",
                "requester": u"shish",
            }
        )
        s2.comments.append(Comment(
            user=user,
            text=u"Comment on a bug",
        ))
        DBSession.add(s2)
        DBSession.flush()

        for n in range(0, 20):
            s3 = Story(
                title=u"Story %d" % n,
                storytype=feature,
                state=iced_feature,
                tracker=tracker,
                rank=5000+n,
                fields={"requester": u"shish"}
            )
            DBSession.add(s3)
        DBSession.flush()

        tracker2 = Tracker(name='t2', title=u"Other Tracker")
        DBSession.add(tracker2)

        bug2 = StoryType(
            name=u"Bug",
            icon="bug",
            tracker=tracker2,
            fields={
                "requester": "User()",
                "owner": "User()",
            }
        )
        iced_bug2 = add_default_states(DBSession, bug)
        DBSession.add(bug2)

        s2 = Story(
            title=u"A Bug Story (in another tracker)",
            storytype=bug2,
            state=iced_bug2,
            tracker=tracker2,
            rank=3000,
            fields={
                "requester": u"shish",
            }
        )
        s2.comments.append(Comment(
            user=user,
            text=u"Comment on a bug",
        ))
        DBSession.add(s2)
