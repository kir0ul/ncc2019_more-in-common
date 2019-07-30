import click

from process import get_tweets, read_json_tweets
from process.aggregate import Aggregate
from process.query_input import Query


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
    "--option",
    type=click.Choice(["rt_users", "fav_users", "gen_stats", "top_hashtags"]),
    help="Type of statistics to compute",
)
def stats(tweet_folder, option="gen_stats"):
    """Compute statistics on already saved data"""
    aggregate = Aggregate(tweet_folder)
    if option == "rt_users":
        aggregate.get_top_rt_users()
    elif option == "fav_users":
        aggregate.get_top_fav_users()
    elif option == "fav_users":
        aggregate.gen_stats()
    elif option == "top_hashtags":
        aggregate.top_hashtags()


@cli.command()
@click.argument("tweet-folder", type=click.Path())
@click.argument("query")
@click.option(
    "--option",
    type=click.Choice(["get_tweet_by", "get_related_hash_by"]),
    help="Type of statistics to compute",
)
def query(tweet_folder, query, option="get_tweet_by"):
    """Query on already saved data"""
    query = Query(tweet_folder)
    if option == "get_tweet_by":
        query.get_tweet_by(query)
    elif option == "get_related_hash_by":
        query.get_related_hash_by(query)


if __name__ == "__main__":
    cli()
