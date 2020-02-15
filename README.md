# Google Photos Sort Archives

A program to easily sort Google Photos archives created when using
Google Takeout.

## Install

```
# Create a new Python virtual environment
$ virtualenv --python /usr/bin/python3.6 venv

# Activate the newly created virtual environment
$ source venv/bin/activate

# Install program
(venv) $ pip install git+https://github.com/ryankwilliams/google-photos-sort-archives
```

## Run

Once installed, you can run the program by issuing the following command:

```
(venv) $ google-photos-sort-archives
```

The help option can be passed to view all options:

```
(venv) $ google-photos-sort-archives --help
```

The following command below demonstrates an example run:

```
(venv) $ google-photos-sort-archives -s ./archive-dir --clean
```
