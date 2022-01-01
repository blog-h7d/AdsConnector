import quart

import adscon
import config_manager

config = config_manager.ConfigManager()
connection = adscon.connector.AdsConnector()

commands_page = quart.Blueprint('command', 'command', url_prefix='/command/')


def _found_in_data(form_data, index):
    key = f'{index}-ID'
    return key in form_data and form_data.get(key, "")


@commands_page.route('save/', methods=['POST'])
async def save_commands():
    form_data = await quart.request.form

    values = []
    act_index = 0
    while _found_in_data(form_data, act_index):
        values.append(
            {
                'identifier': form_data.get(f'{act_index}-ID'),
                'command': form_data.get(f'{act_index}-Command'),
                'group': form_data.get(f'{act_index}-Group'),
                'default': form_data.get(f'{act_index}-Default'),
                'type': form_data.get(f'{act_index}-Type')
            }
        )
        act_index += 1

    await config.save_entry('commands', values)

    return quart.redirect('/')


@commands_page.route('check/<identifier>/')
async def check_command(identifier: str):
    commands = await config.get_config_value('commands')
    for command in commands:
        if command['identifier'] == identifier:
            if command['group'] == 'default':
                command['group'] = command['default']
            data = connection.send_ads_read_command(command['command'], command['group'], command['type'])
            return {'data': data}

    quart.abort(404)


@commands_page.route('run/<identifier>/', methods=['GET'])
async def run_command(identifier: str):
    commands = await config.get_config_value('commands')
    results = {}
    for command in commands:
        if command['identifier'] == identifier:
            groups = [command['group'], ]
            if groups[0] == 'default':
                groups = quart.request.args.get("groups").split(",")

            for group in groups:
                data = connection.send_ads_read_command(command['command'], group, command['type'])
                results[group] = data

            return results

    quart.abort(404)


exec_commands_page = quart.Blueprint('exec_commands', 'exec_commands', url_prefix='/command/exec/')


@exec_commands_page.route('save/', methods=['POST'])
async def save_exec_commands():
    form_data = await quart.request.form

    values = []
    act_index = 0
    while _found_in_data(form_data, act_index):
        values.append(
            {
                'identifier': form_data.get(f'{act_index}-ID'),
                'command': form_data.get(f'{act_index}-Command'),
                'group': form_data.get(f'{act_index}-Group'),
                'default': form_data.get(f'{act_index}-Default'),
                'type': form_data.get(f'{act_index}-Type'),
                'defaultValue': form_data.get(f'{act_index}-DefaultValue'),
            }
        )
        act_index += 1

    await config.save_entry('writecommands', values)

    return quart.redirect('/')


@exec_commands_page.route('check/<identifier>/')
async def check_exec_command(identifier: str):
    commands = await config.get_config_value('writecommands')
    for command in commands:
        if command['identifier'] == identifier:
            data = connection.send_ads_write_command(command['command'],
                                                     command['group'],
                                                     command['type'],
                                                     command['defaultValue'])
            return {'data': data}

    quart.abort(404)
