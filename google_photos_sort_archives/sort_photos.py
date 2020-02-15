import json
import logging
import os
import re
import shutil
import time
import uuid

from google_photos_sort_archives import constants
from google_photos_sort_archives import utils

log = logging.getLogger(__name__)


class SortPhotos(object):
    """Class containing various methods for sorting Google Photos archives."""

    def __init__(self, src, dest, by_month, clean):
        """Constructor.

        :param str src: directory containing archive files
        :param str dest: directory to store sorted google photos files
        :param bool by_month: flag controlling if sorting by year/month or
            just by year
        :param bool clean: flag controlling if unsorted files are removed on
            completion
        """
        self.src = src
        self.dest = dest
        self.by_month = by_month
        self.clean = clean

        self.dest_dir = os.path.join(dest, "photos")
        self.sorted_dir = self.dest_dir
        self.sorted_meta_dir = os.path.join(self.sorted_dir, "metadata")

        self.dup_dest_dir = os.path.join(self.dest_dir, "duplicates")
        self.sorted_dup_dir = self.dup_dest_dir
        self.sorted_dup_meta_dir = os.path.join(self.sorted_dup_dir, "metadata")

        self.sorted = 0
        self.skipped = 0
        self.sorted_files = {"metadata": {}, "files": {}}
        self.skipped_files = {"metadata": {}, "files": {}}

        # Verify provided directories exist
        for dirname in [src, dest]:
            utils.directory_exist(dirname)

        # Make sorted photos directories
        for dirname in [self.dest_dir, self.dup_dest_dir]:
            utils.make_directory(dirname)

    @classmethod
    def get_files(cls, dirname):
        """Get all files for the provided archive.

        :param str dirname: directory name
        :return: archive files
        """
        files = []

        for item in sorted(os.listdir(dirname)):
            path = os.path.join(dirname, item)
            if os.path.isdir(path):
                files += cls.get_files(path)
            else:
                files.append(
                    {
                        "dir": os.path.dirname(path),
                        "file": os.path.basename(path)
                    }
                )
        return files

    def record_result(self, src, dest, file_type):
        """Record photo sort result.

        :param str src: source file
        :param str dest: destination directory where file exists
        :param str file_type: the file type (photo file/metadata file)
        """
        if file_type == "file":
            self.sorted += 1
            filename = os.path.basename(src)
            self.sorted_files[file_type][filename] = {
                "src": src,
                "dest": dest,
                "dest_src": os.path.join(dest, src)
            }
        elif file_type == "meta":
            filename = os.path.basename(src)
            if filename not in self.skipped_files[file_type]:
                self.skipped += 1
                self.skipped_files[file_type][filename] = {
                    "src": src,
                    "dest": dest,
                    "dest_src": os.path.join(dest, filename),
                    "reason": "Filename already exists"
                }

    def save_results(self):
        """Save photo sorting results to disk."""
        for item in ["sorted", "skipped"]:
            filename = os.path.join(self.dest, f"{self.src}_{item}.json")
            with open(filename, "w") as f:
                json.dump(getattr(self, f"{item}_files"), f, indent=4)

    def move_file(self, src, dest, file_type, dup_dest):
        """Move photo file.

        :param str src: source file
        :param str dest: destination directory to move file into
        :param str file_type: the file type (photo file/metadata file)
        :param str dup_dest: destintation directory to move duplicate files
            into
        """
        utils.make_directory(dest)

        try:
            shutil.move(src, dest)
        except shutil.Error as e:
            if "already exists" in e.args[-1]:
                utils.make_directory(dup_dest)
                filename = os.path.basename(src)
                if os.path.exists(os.path.join(dup_dest, filename)):
                    dup_dest = os.path.join(
                        dup_dest, f"{str(uuid.uuid4())[0:4]}_{filename}")
                shutil.move(src, dup_dest)
        finally:
            self.record_result(src, dest, file_type)

    def move_photo_file(self, filename):
        """Move photo file.

        :param str filename: photo file
        """
        self.move_file(
            filename,
            self.sorted_meta_dir,
            "meta",
            self.sorted_dup_meta_dir
        )

    def move_photo_meta_file(self, filename):
        """Move photos metadata file.

        :param filename: photos metadata file
        """
        self.move_file(
            filename,
            self.sorted_dir,
            "file",
            self.sorted_dup_dir
        )

    def _sort(self):
        """The actual method performing sorting actions."""
        for item in self.get_files(self.src):
            path = item['dir']
            filename = item['file']
            dirname = os.path.basename(path)
            filepath = os.path.join(path, filename)

            # Skip directories not following naming convention %Y-%m-%d
            if re.search("([0-9][0-9][0-9][0-9]-)", dirname) is None:
                continue

            dir_split = dirname.split("-")
            year, month = dir_split[0], dir_split[1]
            self.sorted_dir += f"/{year}"
            self.sorted_dup_dir += f"/{year}"

            if self.by_month:
                self.sorted_dir += f"/{month}"
                self.sorted_dup_dir += f"/{month}"

            if filename.endswith(".json") and "metadata" in filename:
                self.move_photo_meta_file(filepath)
            elif utils.file_ext(filename) in constants.FILE_TYPES:
                self.move_photo_file(filepath)

    def sort(self):
        """Sort photos 'entry point'."""
        start_time = time.time()

        for i in range(1, 3):
            log.info(f"Pass #{i}")
            self._sort()
            log.info(f"Pass #{i} complete")

        self.save_results()

        end_time = time.time()
        hours, minutes, seconds = utils.calculate_time_diff(
            start_time, end_time)

        log.info("-+ Google Photo Archive 'Takeout' Results +-")
        log.info(f"    Unsorted directory   : {self.src}")
        log.info(f"    Sorted directory     : {self.dest_dir}")
        log.info(f"    Total files sorted   : {self.sorted}")
        log.info(f"    Total files skipped  : {self.skipped}")
        log.info(f"    Result files (.json) : {self.dest_dir}")
        log.info(f"    Total time           : %dh:%dm:%ds" % (hours, minutes,
                                                              seconds))
