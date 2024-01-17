# free5GC Website

This repository contains the source code of free5GC's website available at [https://free5gc.org/](https://free5gc.org/)

## Prerequisites

It's required to install the dependencies below:

- pymdown-extensions (mkdocs requirement)
- mkdocs-callouts (mkdocs requirement)
- mkdocs-material (theme)
- For more dependencies, please, check the [requirements](requirements.txt) file

Install the dependencies using the below command

    pip install pymdown-extensions mkdocs-callouts

To install the theme use

    pip install mkdocs-material

[Optional] To load the packages into a Python virtual environment, use the command below

    pip install -r requirements.txt

## Deploying a Development Environment

1. Clone this repository

        git clone https://github.com/free5gc/free5gc.github.io.git

2. Enter the project folder

        cd free5gc.github.io

3. If not already done, install the requirements using

        pip install pymdown-extensions mkdocs-callouts mkdocs-material

    Or (to install the full environment)
    
        pip install -r requirements.txt

4. Deploy an instace of the website

        mkdocs serve

**Note:** If the command is successful, a service should be running on port 5000 on your localhost.

## Using Dev Env

1. Go to the repo folder

2. Deploy the local instance of the website using:

        mkdocs serve

## Other Useful Information

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

### Commands

<!-- * `mkdocs new [dir-name]` - Create a new project. -->
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

### Project layout

    mkdocs.yml    # The configuration file.
    ...           # Other webserver related files
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
