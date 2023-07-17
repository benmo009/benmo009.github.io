from jinja2 import Environment, FileSystemLoader
import logging

from site_builder import utils
from site_builder.SiteBuilder import SiteBuilder


def main():
    """ Main function """
    args = utils.parse_arguments()
    logger = utils.init_log(level=logging.DEBUG)

    try:
        builder = SiteBuilder(args, logger)
        builder.build_site()
    except Exception as exp:
        logger.error(f"{exp.__class__.__name__}: {exp}")

if __name__ == "__main__":
    main()