import click

from process import get_tweets


@click.command()
@click.option(
    "--method",
    help="Use 'populate' to get already existing tweets"
    " or 'track' to get new tweets published from now on",
)
@click.option("--hashtags", help="Hashtags to get from Twitter")
@click.option("--path", help="Path to folder where to save tweets")
def main(method=None, hashtags=None, path=None):
    if method and hashtags and path:
        get_tweets.main(
            get_method=method, input_hashtags=hashtags, storage_location=path
        )


if __name__ == "__main__":
    main()
