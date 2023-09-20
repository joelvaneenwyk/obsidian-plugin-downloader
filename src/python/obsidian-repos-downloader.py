#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

from utils.json import (
    get_json_from_github, PLUGINS_JSON_FILE, THEMES_JSON_FILE)
from utils.directories import use_directory, readable_dir


class DownloaderOptions:
    def __init__(self):
        self.parser = self.make_parser()
        self.args = None

    def make_parser(self):
        parser = argparse.ArgumentParser(
            description="Clone repos included in the obsidian-releases repo, "
                        "to provide a body of example plugins and CSS themes."
        )
        parser.add_argument('-o', '--output_directory', default='.', type=readable_dir,
                            help='The directory where repos will be downloaded. Must already exist. '
                                 '(default: %(default)s which means "current working directory")'
                            )

        parser.add_argument('-l', '--limit', type=int, default=0,
                            help='Limit the number of plugin and theme repos that will be downloaded. '
                                 'This is useful when testing the script. '
                                 '0 (zero) means "no limit". '
                                 'Note: the count currently includes any repos already downloaded.'
                                 '(default: %(default)s)')

        parser.add_argument('-n', '--dry-run', action="store_true",
                            help='Print out the commands to be executed, but do no run them. '
                                 'This is useful for testing. '
                                 'Note: it does not print the directory-creation commands, '
                                 'just the git ones')

        parser.add_argument('-t', '--type',
                            default='all',
                            const='all',
                            nargs='?',
                            choices=['plugins', 'themes', 'all'],
                            help='The type of repositories to download: plugins, themes or both. '
                                 '(default: %(default)s)')

        parser.add_argument('--group-by-user', dest='group_by_user', action='store_true',
                            help='Put each repository in a sub-folder named for the GitHub user. '
                                 'For example, the plugin "https://github.com/phibr0/obsidian-tabout" would be placed '
                                 'in "plugins/phibr0/obsidian-tabout"')
        parser.add_argument('--no-group-by-user', dest='group_by_user', action='store_false',
                            help='Put each repository in the same folder, prefixed by the user name. '
                                 'This is the default behaviour. '
                                 'For example, the plugin "https://github.com/phibr0/obsidian-tabout" would be placed '
                                 'in "plugins/phibr0-obsidian-tabout"')
        parser.set_defaults(group_by_user=False)

        return parser

    def parse_args(self, argv):
        self.args = self.parser.parse_args(argv)

    def limit(self):
        return self.args.limit

    def dry_run(self):
        return self.args.dry_run

    def need_to_download_type(self, type):
        return self.args.type in ["all", type]

    def root_output_directory(self):
        return self.args.output_directory

    def repo_output_directory(self, user):
        if self.args.group_by_user:
            return user
        else:
            return '.'

    def repo_output_name(self, user, repo):
        if self.args.group_by_user:
            return repo
        else:
            # Prefix with username, in case there are any duplicated repo names
            return f"{user}-{repo}"


class Downloader:
    def __init__(self, options):
        self.options = options
        self.errors = ""

    def download(self):
        with use_directory(self.options.root_output_directory(), create_if_missing=False):
            print(f"Working directory: {os.getcwd()}")
            self.process_released_plugins()
            self.process_released_themes()

        self.print_any_errors()

    def process_released_plugins(self):
        self.process_released_repos("plugins", PLUGINS_JSON_FILE)

    def process_released_themes(self):
        self.process_released_repos("themes", THEMES_JSON_FILE)

    def process_released_repos(self, type, json_file):
        if not self.options.need_to_download_type(type):
            return

        print(f"-----\nProcessing {type}....\n")
        with use_directory(type, create_if_missing=True):
            plugin_list = get_json_from_github(json_file)
            sorted_list = sorted(plugin_list, key=lambda d: d['repo'].lower())
            self.clone_or_update_repos(sorted_list)

    def clone_or_update_repos(self, plugin_list):
        count = 0
        limit = self.options.limit()
        for plugin in plugin_list:
            self.clone_or_update_repo(plugin)
            count += 1
            if limit > 0 and count >= limit:
                print("Maximum number of new repos exceeded. Stopping.")
                return

    def clone_or_update_repo(self, plugin):
        repo = plugin.get("repo")
        branch = plugin.get("branch", "master")
        user, repo_name = repo.split("/")
        directory_for_repo = self.options.repo_output_directory(user)
        with use_directory(directory_for_repo, create_if_missing=True):
            repo_output_name = self.options.repo_output_name(user, repo_name)
            if not os.path.isdir(repo_output_name):
                command = self.get_download_command(repo, repo_output_name)
                self.run_or_log("cloning", command, repo)
            else:
                with use_directory(repo_output_name, create_if_missing=False):
                    command = self.get_clone_command()
                    self.run_or_log(f"updating", command, repo)

    def run_or_log(self, verb, command, repo):
        message = f"{verb} {repo}"
        print(message)
        if self.options.dry_run():
            self.log_dry_run(command)
        else:
            result = subprocess.run(command, shell=True, check=False, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_error(result, message, command)

    def log_dry_run(self, command):
        print(f'Dry run mode: {command}')

    def get_download_command(self, repo, repo_output_name):
        url = f'https://github.com/{repo}'
        print(url)
        command = f"git clone --recurse-submodules -j8 --quiet {url}.git {repo_output_name}"
        return command

    def get_clone_command(self):
        command = 'git pull --quiet'
        return command

    def log_error(self, result, message2, command):
        message = f"""{message2}
command:    {command}
in:         {os.getcwd()}
exit code:  {result.returncode}
stdout:     {result.stdout}
stderr:     {result.stderr}
-------------------------------------------------------------------------------
"""
        print(message)
        self.errors += message

    def print_any_errors(self):
        if self.errors != "":
            print("The following errors occurred:")
            print(self.errors)


def download_repos(argv=sys.argv[1:]):
    options = DownloaderOptions()
    options.parse_args(argv)

    downloader = Downloader(options)
    downloader.download()


if __name__ == "__main__":
    download_repos()
