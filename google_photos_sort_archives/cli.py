import click

from google_photos_sort_archives import utils
from google_photos_sort_archives.sort_photos import SortPhotos


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
    "--by-month",
    default=False,
    help="Sort photos & videos by month",
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
def main(source, dest, by_month, clean, verbose):
    """Sort Google Photos Archives"""
    # Setup logging
    utils.initialize_logging(verbose)

    # Instantiate SortPhotos object
    sort_photos = SortPhotos(source, dest, by_month, clean)

    # Sort photos
    sort_photos.sort()
