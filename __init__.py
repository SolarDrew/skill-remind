import logging
from functools import partial

from opsdroid.matchers import match_always, match_crontab
from opsdroid.message import Message


async def reminder(opsdroid, config, message, text):
    # Get the default connector
    connector = opsdroid.default_connector

    # Get the default room for that connector
    room = connector.default_room

    # Create an empty message to respond to
    message = Message("", None, room, connector)

    # Remind the player
    await message.respond(text)


def setup(opsdroid):
    logging.debug("Loaded reminder module")
    for skill in opsdroid.config['skills']:
        if skill['name'] == 'remind':
            logging.debug(skill['reminders'])
            reminders = {}
            for confentry in skill['reminders']:
                reminders.update(confentry)
            for (remindercron, remindertext) in reminders.items():
                logging.debug(f"Creating reminder {remindercron}: '{remindertext}'.")
                this_reminder = partial(reminder, text=remindertext)
                cron_decorator = match_crontab(remindercron, timezone="Europe/London")
                this_reminder = cron_decorator(this_reminder)
