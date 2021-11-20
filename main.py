import typer

from app.controllers import MowerController

app = typer.Typer()


@app.command()
def process(request: str) -> None:
    controller = MowerController()
    try:
        response = controller.handle(request)
    except ValueError as e:
        typer.secho(e, fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code=1)

    typer.secho(response, fg=typer.colors.GREEN, bold=True)


if __name__ == '__main__':
    app()
