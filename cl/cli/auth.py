import click
import webbrowser

import cl
from cl.client.auth import AuthClient
from cl.manager.auth_config import AuthConfigManager
from cl.model.access_token import AccessToken
from cl.log import logger as russell_logger
from cl.client.common import get_basic_token

@click.command()
@click.option('--token', is_flag=True, default=False, help='Just enter token')
def login(token):
    """
    Log into CodingLife via Auth0.
    """
    if not token:
        cli_info_url = cl.russell_web_host + "/welcome"
        click.confirm('Authentication token page will now open in your browser. Continue?', abort=True, default=True)
        webbrowser.open(cli_info_url)
        token = str(click.prompt('Please copy and paste the token here', type=str, hide_input=True))

    if not token:
        russell_logger.info("Empty token received. Make sure your shell is handling the token appropriately.")
        russell_logger.info("See FAQ for help: http://docs.russellcloud.cn/")
        return

    access_code = get_basic_token(token)

    user = AuthClient().get_user(access_code)
    access_token = AccessToken(username=user.username,
                               token=access_code)
    AuthConfigManager.set_access_token(access_token)
    russell_logger.info("Login Successful as " + user.username)


@click.command()
def logout():
    """
    Logout of CodingLife.
    """
    AuthConfigManager.purge_access_token()
