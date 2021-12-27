import quart

import config_manager

app = quart.Quart(__name__)
# TODO: Make this accessible from Docker
app.secret_key = "AppForPyADS_ChangeForUsage"


@app.route('/connection/check/')
async def check_connection():
    return ''


@app.route('/command/check/<id>/')
async def check_command(id: str):
    return ''


@app.route("/")
async def main():
    data = {
        'adsserver': await config_manager.get_config_value('adsserver'),
        'amsnetid': await config_manager.get_config_value('amsnetid'),
        'port': await config_manager.get_config_value('port', default='851'),
    }
    return await quart.render_template('main.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
