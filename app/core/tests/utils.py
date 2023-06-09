from core import models


def sample_create_thread(user_1: models.User, user_2: models.User) -> models.Thread:
    """Create Thread model object"""
    thread = models.Thread.objects.create(
        name="new_thread",
    )

    thread.users.add(user_1)
    thread.users.add(user_2)

    return thread


def sample_create_message(user_1: models.User, user_2: models.User) -> models.Thread:
    """Create Thread model object"""
    thread = sample_create_thread(user_1=user_1, user_2=user_2)

    return models.Message.objects.create(thread=thread, sender=user_1, text="hello")
