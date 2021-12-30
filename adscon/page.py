import quart

import config_manager

commands_page = quart.Blueprint('command', 'command', url_prefix='/command/')

config = config_manager.ConfigManager()


@commands_page.route('save/', methods=['POST'])
async def save_commands():
    form_data = await quart.request.form

    def found_in_data(index):
        key = f'{index}-ID'
        return key in form_data and form_data.get(key, "")

    values = []

    act_index = 0
    while found_in_data(act_index):
        values.append(
            {
                'identifier': form_data.get(f'{act_index}-ID'),
                'command': form_data.get(f'{act_index}-Command'),
                'group': form_data.get(f'{act_index}-Group'),
                'type': form_data.get(f'{act_index}-Type')
            }
        )
        act_index += 1

    await config.save_entry('commands', values)

    return quart.redirect('/')


@commands_page.route('check/<identifier>/')
async def check_command(identifier: str):
    return identifier
