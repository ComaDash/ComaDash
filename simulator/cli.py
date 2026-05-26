import typer

from publisher import run


app = typer.Typer(help="COMASA MQTT digital twin")


@app.command()
def publish() -> None:
    run()


if __name__ == "__main__":
    app()
