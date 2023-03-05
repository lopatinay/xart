import click
import uvicorn

from service_api.configs import RuntimeConfig
from service_api.repository.assets import populate_data
from service_api.repository.user import init_users


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


@cli.command("init_users")
def _init_users():
    init_users()


@cli.command("populate_data")
def _populate_data():
    populate_data()


if __name__ == "__main__":
    cli()
