import logging
from functools import partial

from opsdroid.matchers import match_always, match_crontab
from opsdroid.message import Message


async def reminder(opsdroid, config, message, specs):
    # Get the default connector
    connector = opsdroid.default_connector

    # Get the default room for that connector
    room = connector.default_room

    # Create an empty message to respond to
    message = Message("", None, room, connector)

    # Remind the player
    await message.respond(specs['message'])


def setup(opsdroid):
    logging.debug("Loaded reminder module")
    for skill in opsdroid.config['skills']:
        if skill['name'] == 'remind':
            for (funcname, specs) in skill['reminders'].items():
                logging.debug(f"Creating reminder {funcname} for {specs['crontime']}.")
                this_reminder = partial(reminder, specs=specs)
                cron_decorator = match_crontab(specs['crontime'],
                                               timezone="Europe/London")
                this_reminder = cron_decorator(this_reminder)


@match_always
async def last_speaker(opsdroid, config, message):
    # Keep track of the last person in the room to speak.
    await opsdroid.memory.put("last_speaker", message.user)


@match_crontab('0 * * * *', timezone="Europe/London")
async def remind(opsdroid, config, message):
    # Get the default connector
    connector = opsdroid.default_connector

    # Get the default room for that connector
    room = connector.default_room

    # Create an empty message to respond to
    message = Message("", None, room, connector)

    last_speaker = await opsdroid.memory.get("last_speaker")
    if last_speaker == None:
        return

    # Remind the player
    await message.respond(f"Hey {last_speaker}, don't forget to tell the DM you're finished.")
