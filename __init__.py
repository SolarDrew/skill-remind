import logging

from opsdroid.matchers import match_always, match_crontab
from opsdroid.message import Message


def setup(opsdroid):
    logging.debug("Loaded reminder module")


@match_always
async def last_speaker(opsdroid, config, message):
    # Keep track of the last person in the room to speak.
    await opsdroid.memory.put("last_speaker", message.user)


@match_crontab('* * * * *', timezone="Europe/London")
async def remind(opsdroid, config, message):
    # Get the default connector
    connector = opsdroid.default_connector
    logging.debug(f"Selected {} as default connector")

    # Get the default room for that connector
    room = connector.default_room
    logging.debug(f"Selected {} as default room")

    # Create an empty message to respond to
    message = Message("", None, room, connector)

    last_speaker = await opsdroid.memory.get("last_speaker")

    # Remind the player
    await message.respond(f"Hey {last_speaker}, don't forget to tell the DM you're finished.")
