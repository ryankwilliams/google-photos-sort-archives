import logging
import os

from google_photos_sort_archives import constants

__all__ = [
    "calculate_time_diff",
    "directory_exist",
    "file_ext",
    "initialize_logging",
    "make_directory"
]

log = logging.getLogger(__name__)


def initialize_logging(verbose):
    """Initialize logging.

    :param bool verbose: flag determining if verbose logging should be used
    """
    logging.basicConfig(
        level=getattr(logging, "DEBUG" if verbose else "INFO"),
        format=constants.LOG_FORMAT
    )


def directory_exist(dirname):
    """Determine if the provided directory exists.

    :param dirname: directory name to check existence
    :raises: SystemExit (exit_code=2) when directory not found
    """
    if not os.path.exists(dirname):
        log.error(f"Directory {dirname} does not exist.")
        raise SystemExit(2)


def make_directory(dirname):
    """Make a directory using the provided directory name.

    :param dirname: directory name
    :raises: SystemExit (exit_code=2) when unable to make directory
    """
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass
    except OSError as e:
        log.error(f"Failed to make directory {dirname}.")
        raise SystemExit(2)


def calculate_time_diff(start_time, end_time):
    """Calculate time difference between two points.

    :param start_time: starting time
    :param end_time: ending time
    :return: the time difference
    """
    elapsed = end_time - start_time
    hours = elapsed // 3600
    elapsed = elapsed - 3600 * hours
    minutes = elapsed // 60
    seconds = elapsed - 60 * minutes

    return hours, minutes, seconds


def file_ext(filename):
    """Get the file extension for the provided file.

    :param filename: filename
    :return: the files extension 'lowercase'
    """
    return os.path.splitext(filename)[-1].lower()
