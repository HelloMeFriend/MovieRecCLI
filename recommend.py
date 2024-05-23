import typer
from messages import display_menu, getfilePath
from main import search, recommendations

app = typer.Typer()


@app.command()
def main():
    while True:
        choice = display_menu()
        
        if choice == 'get_recommendations':
            movie_title = typer.prompt("Enter the movie title")
            results = search(movie_title)
            movie_id = results["movieId"].values[0]
            recs = recommendations(movie_id)
            typer.echo(recs)
            typer.echo("")
            # file_path = getfilePath()
            # # Add logic to get movie recommendations based on the file_path
            # typer.echo(f"Getting movie recommendations based on file: {file_path}\n")

        elif choice == 'exit':
            typer.echo("Exiting the program.")
            break

if __name__ == "__main__":
    app()

