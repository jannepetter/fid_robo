from robocorp.tasks import task

from hello_private import say_hello


@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    print("messa", message)
    hello = say_hello()
    print(hello)
