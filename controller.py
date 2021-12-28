import quart

import adscon
import config_manager

app = quart.Quart(__name__)
# TODO: Make this accessible from Docker
app.secret_key = "AppForPyADS_ChangeForUsage"

connection = adscon.AdsConnector()


@app.before_serving
async def start_server():
    connection.initialize(await config_manager.get_config_value("adsserver"),
                          await config_manager.get_config_value("amsnetid"),
                          await config_manager.get_config_value("port")
                          )


@app.route('/connection/check/')
async def check_connection():
    data = connection.check_connection()
    return '{"data":"' + str(data) + '"}'


@app.route('/command/check/<id>/')
async def check_command(id: str):
    return ''


@app.route("/")
async def main():
    data = {
        'server_ip': await config_manager.get_config_value('adsserver'),
        'amsnetid': await config_manager.get_config_value('amsnetid'),
        'port': await config_manager.get_config_value('port', default='851'),
        'commands': await config_manager.get_config_value('commands'),
    }

    return await quart.render_template('main.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
