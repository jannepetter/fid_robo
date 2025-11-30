from robocorp.tasks import task

from test_app_hommat import TestStuff


@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    print("messa", message)
    t = TestStuff("oho")
    t.say()
