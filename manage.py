import click
import uvicorn

from service_api.configs import RuntimeConfig
# from service_api.domain.user_account.use_cases import create_super_admin


@click.group()
def cli():
    pass


@cli.command("runserver")
@click.option("-h", "--host", default="0.0.0.0")
@click.option("-p", "--port", default=9000)
@click.option("--debug", default=RuntimeConfig.debug)
def _runserver(host, port, debug):
    conf = {
        "host": host,
        "port": port,
        "access_log": debug,
    }
    uvicorn.run("service_api.app:fast_app", **conf)


# @cli.command("create_super_admin")
# @click.option("-p", "--password", default="john@wick.cont")
# def _create_super_admin(password):
#     create_super_admin(password)


if __name__ == "__main__":
    cli()
