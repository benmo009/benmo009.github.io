import os
import shutil
import logging
import argparse
import jinja2 as jinja

from site_builder import utils

class SiteBuilder:
    def __init__(self, args: argparse.Namespace, logger: logging.Logger):
        self._args = args
        self._logger = logger
        self._template_path = os.path.abspath(args.template_path)
        self._output_path = os.path.abspath(args.output_path)
        self._skip_paths = set([os.path.abspath(p) for p in args.skip_paths])
        self._copy_paths = [os.path.abspath(p) for p in args.copy_paths]

        self.check_template_path()
        self.check_output_path()
        self.get_template_files()

        self._logger.debug("Successfully initialized SiteBuilder.")

    @property
    def logger(self):
        return self._logger
    @property
    def template_path(self):
        return self._template_path
    @property
    def output_path(self):
        return self._output_path
    @property
    def skip_paths(self):
        return self._skip_paths
    @property
    def copy_paths(self):
        return self._copy_paths
    @property
    def template_files(self):
        return self._template_files

    def check_template_path(self):
        """ Checks that a valid template path was given.

        Raises an Exception if template path does not exist or if it is not a directory.
        """
        if not os.path.exists(self.template_path):
            raise Exception(f"Template path: {self.template_path} does not exist.")
        if not os.path.isdir(self.template_path):
            raise Exception(f"Template path: {self.template_path} is not a directory.")

    def check_output_path(self):
        """ Checks that a valid site path was given, removing any pre-existing files.

        Raises an Exception if output path is a file.
        """
        if os.path.isfile(self.output_path):
            raise Exception(f"Output path: {self.output_path} already exists and is a file. Either rename it or change site path.")

        if os.path.isdir(self.output_path):
            count = utils.recurse_path_remove(self.output_path)
            self.logger.info(f"Deleted {count} pre-existing files in output path: {self.output_path}")

        os.makedirs(self.output_path)

    def get_template_files(self):
        self._template_files = []
        utils.recurse_path_search(self.template_path, self._template_files, skip_dirs=self.skip_paths)
        for i in range(len(self._template_files)):
            self._template_files[i] = os.path.relpath(self._template_files[i], self.template_path)

        self.logger.info(f"Found {len(self._template_files)} templates.")

    def render(self):
        env = jinja.Environment(
            loader = jinja.FileSystemLoader(self.template_path)
        )
        for file in self.template_files:
            full_path = os.path.join(self.output_path, file)
            file_head, file_tail = os.path.split(full_path)
            self.logger.info(f"Rendering to {full_path}")

            if not os.path.isdir(file_head):
                os.makedirs(file_head)

            template = env.get_template(file.replace('\\', '/'))
            with open(full_path, 'w') as f:
                f.write(template.render())

    def copy_necessary_files(self):
        for path in self.copy_paths:
            out_path = os.path.join(self.output_path, os.path.basename(path))
            dest = shutil.copytree(path, out_path)
            self.logger.info(f"Copied {path} to {dest}")

    def build_site(self):
        self.logger.info("Building website")
        self.render()
        self.copy_necessary_files()