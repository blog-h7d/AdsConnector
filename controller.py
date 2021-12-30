import markupsafe
import pyads
import quart

import adscon
import config_manager

app = quart.Quart(__name__)
# TODO: Make this accessible from Docker
app.secret_key = "AppForPyADS_ChangeForUsage"
app.register_blueprint(adscon.page.commands_page)

connection = adscon.connector.AdsConnector()
config = config_manager.ConfigManager()


@app.template_filter('option')
def filter_option(value, data):
    return markupsafe.Markup(f'value="{value}" ' + ("selected" if value == data else ""))


@app.before_serving
async def start_server():
    adscon.page.connection.initialize(
        server_address=await config.get_config_value("adsserver"),
        server_amsnetid=await config.get_config_value("amsnetid"),
        port=await config.get_config_value("port")
    )


@app.route('/connection/check/')
async def check_connection():
    try:
        data = adscon.page.connection.check_connection()
    except pyads.ADSError as ads_error:
        data = ads_error
    return '{"data":"' + str(data) + '"}'


@app.route('/connection/save/', methods=['POST'])
async def save_connection():
    form = await quart.request.form

    server_ip = form.get('server_ip')
    await config.save_entry('adsserver', server_ip)

    amsnetid = form.get('amsnetid')
    await config.save_entry('amsnetid', amsnetid)

    port = form.get('port')
    await config.save_entry('port', port)

    adscon.page.connection.initialize(server_ip, amsnetid, port)

    return quart.redirect('/')




@app.route("/")
async def main():
    data = {
        'server_ip': await config.get_config_value('adsserver'),
        'amsnetid': await config.get_config_value('amsnetid'),
        'port': await config.get_config_value('port', default='851'),
        'commands': await config.get_config_value('commands', default=[]),
    }

    return await quart.render_template('main.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
