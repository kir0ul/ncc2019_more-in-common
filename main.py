import click

from process import get_tweets, read_json_tweets
from process.aggregate import Aggregate


@click.group()
def cli():
    pass


@cli.command()
@click.argument("hashtags")
@click.argument("path", type=click.Path())
@click.option(
    "--method",
    type=click.Choice(["populate", "track"]),
    help="Use 'populate' to get already existing tweets"
    " or 'track' to get new tweets published from now on",
)
def get(hashtags, path, method="populate"):
    """Get tweets from Twitter according to the specified HASHTAGS.
    Save them in JSON format in the specified PATH"""
    get_tweets.main(input_hashtags=hashtags, storage_location=path, get_method=method)


@cli.command()
@click.argument("import-folder", type=click.Path())
@click.argument("export-folder", type=click.Path())
def read(import_folder, export_folder):
    """Read already saved tweets from IMPORT_FOLDER and
    export them to EXPORT_FOLDER as CSV tables"""
    read_json_tweets.main(import_folder, export_folder)


@cli.command()
@click.argument("tweet-folder", type=click.Path())
@click.option(
    "--infos",
    type=click.Choice(["rt_users", "fav_users", "gen_stats", "top_hashtags"]),
    help="Type of statistics to compute",
)
def stats(tweet_folder, infos="gen_stats"):
    """Compute statistics on already saved data"""
    aggregate = Aggregate(tweet_folder)
    if infos == "rt_users":
        aggregate.get_top_rt_users()
    elif infos == "fav_users":
        aggregate.get_top_fav_users()
    elif infos == "fav_users":
        aggregate.gen_stats()
    elif infos == "top_hashtags":
        aggregate.top_hashtags()


if __name__ == "__main__":
    cli()
