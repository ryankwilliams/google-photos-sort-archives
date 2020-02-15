import click


@click.command()
@click.option(
    "-s", "--source",
    required=True,
    help="Source folder containing photos to sort"
)
@click.option(
    "-d", "--dest",
    default=".",
    help="Destination folder to save sorted photos"
)
@click.option(
    "-ym", "--year-month",
    default=False,
    help="Sort photos & videos by year/month",
    is_flag=True
)
@click.option(
    "-c", "--clean",
    default=False,
    help="Clean up unsorted files in source directory",
    is_flag=True
)
@click.option(
    "-v", "--verbose",
    default=False,
    help="Enable verbose logging",
    is_flag=True
)
def main(source, dest, year_month, clean, verbose):
    """Sort Google Photos Archives"""
    pass
