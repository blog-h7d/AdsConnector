import quart

commands_page = quart.Blueprint('commands', 'commands', url_prefix='/command/')


@commands_page.route('check/<identifier>/')
async def check_command(identifier: str):
    return identifier
