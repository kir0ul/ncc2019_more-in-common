import click

from process import populate_hashtag


@click.command()
@click.option("--populate", help="Populate tweets")
@click.option("--path", help="Path to folder where to save tweets")
def main(populate=None, path=None):
    if populate and path:
        populate_hashtag.main(populate, path)


if __name__ == "__main__":
    main()
