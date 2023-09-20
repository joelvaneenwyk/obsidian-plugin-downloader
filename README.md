# 📩 Obsidian Repositories Downloader

<div align='center'>
  <img src="https://user-images.githubusercontent.com/61631665/132124154-58db4b3d-e19f-4f71-844c-5aefc0917b15.gif"/>
  <p>Learn, analyze and inspire from every <a href="https://obsidian.md">obsidian.md</a> plugin! Downloads every available Obsidian plugin (<1GB).</p>
  <img src="https://user-images.githubusercontent.com/61631665/131258921-9960bad9-4b76-434e-9b30-cd9cf14cb683.png"/>
  🔎 This allows to easily search and analyze other plugins. It's especially useful as Obsidian API isn't yet documented and GitHub search doesn't work as expected.

  <img src="https://user-images.githubusercontent.com/61631665/131258790-2499b1d7-50fe-4b9a-abde-0f00d6d08b17.png"/>
    🌳 Generates a nice tree structure!
</div>

<!-- toc -->
## Contents

  * [What?](#what)
  * [Why?](#why)
  * [Setup](#setup)
  * [Run](#run)
  * [Output Directories](#output-directories)
  * [Likely Questions](#likely-questions)
  * [Alternatives](#alternatives)
  * [🔨 Other Tools](#-other-tools)
  * [👾 Usage](#-usage)<!-- endToc -->

[![on-push-do-doco](https://github.com/joelvaneenwyk/obsidian-repos-downloader/actions/workflows/updateMarkdown.yml/badge.svg)](https://github.com/joelvaneenwyk/obsidian-repos-downloader/actions/workflows/updateMarkdown.yml)

## What?

Clone every approved Obsidian.md community Plugin and Theme - to read and search the source code and learn from the community.

This is a Python3 script to download a local copy of all the [published community Obsidian plugins and themes](https://github.com/obsidianmd/obsidian-releases), to be used as a large body of example code.

It inspects these files, and then downloads (clones) all the repos listed in them:

* [community-css-themes.json](https://github.com/obsidianmd/obsidian-releases/blob/master/community-css-themes.json)
* [community-plugins.json](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json)

## Why?

I cannot put it better than the author of the similar project [luckman212/**obsidian-plugin-downloader**](https://github.com/luckman212/obsidian-plugin-downloader):

> As an absolute beginner to TypeScript, and a lover of [Obsidian](https://obsidian.md/) I often want to take a look at how someone has achieved a certain feature, called on an API, etc. A quick way to do that is by searching through the existing codebase of the ever growing library of plugins out there.

## Setup

### Requirements

* Python 3.6 or above

### Download

1. Download the [Latest Release](https://github.com/joelvaneenwyk/obsidian-repos-downloader/releases).
   * Choose one of:
       * "Source code (zip)"
       * "Source code (tar.gz)"
   * If you can't see them, click to expand the "Assets"
2. Expand the downloaded Source Code file
   * This will give you a folder name such as "obsidian-repos-downloader-0.1.0"

## Run

### Getting Started

The script to run is `obsidian-repos-downloader.py`

Depending on your platform, here are some example ways you might need to run it:

```bash
obsidian-repos-downloader.py
./obsidian-repos-downloader.py
python3 obsidian-repos-downloader.py
```

### Usage - all the arguments

Running `obsidian-repos-downloader.py --help` gives this output:

<!-- snippet: usage.txt -->
```txt
usage: obsidian-repos-downloader.py [-h] [-o OUTPUT_DIRECTORY] [-l LIMIT] [-n]
                                    [-t [{plugins,themes,all}]]
                                    [--group-by-user] [--no-group-by-user]

Clone repos included in the obsidian-releases repo, to provide a body of
example plugins and CSS themes.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        The directory where repos will be downloaded. Must
                        already exist. (default: . which means "current
                        working directory")
  -l LIMIT, --limit LIMIT
                        Limit the number of plugin and theme repos that will
                        be downloaded. This is useful when testing the script.
                        0 (zero) means "no limit". Note: the count currently
                        includes any repos already downloaded.(default: 0)
  -n, --dry-run         Print out the commands to be executed, but do no run
                        them. This is useful for testing. Note: it does not
                        print the directory-creation commands, just the git
                        ones
  -t [{plugins,themes,all}], --type [{plugins,themes,all}]
                        The type of repositories to download: plugins, themes
                        or both. (default: all)
  --group-by-user       Put each repository in a sub-folder named for the
                        GitHub user. For example, the plugin
                        "https://github.com/phibr0/obsidian-tabout" would be
                        placed in "plugins/phibr0/obsidian-tabout"
  --no-group-by-user    Put each repository in the same folder, prefixed by
                        the user name. This is the default behaviour. For
                        example, the plugin
                        "https://github.com/phibr0/obsidian-tabout" would be
                        placed in "plugins/phibr0-obsidian-tabout"
```
<!-- endSnippet -->

## Output Directories

The script always creates a `plugins/` and `themes/` directories for its output.

There are the command-line arguments to determine the structure inside those directories.

### Flatter Structure

By default, or when the argument `--no-group-by-user` is supplied, all the downloaded repos are placed side-by-side.
They are prefixed with the username of the developer who wrote them.

For example, running this command (limiting the output to only 4 repositories, for brevity)....

```bash
obsidian-repos-downloader.py  --limit 4
```

... gives this directory structure:

<!-- snippet: tree-output-ungrouped.txt -->
```txt
plugins
├── agathauy-wikilinks-to-mdlinks-obsidian
├── aidenlx-alx-folder-note
├── aidenlx-better-fn
└── aidenlx-cm-chs-patch
themes
├── ArtexJay-Obsidian-CyberGlow
├── auroral-ui-aurora-obsidian-md
├── bcdavasconcelos-Obsidian-Ayu
└── bcdavasconcelos-Obsidian-Ayu_Mirage

8 directories
```
<!-- endSnippet -->

### Grouped by User name

When the argument `--group-by-user` is supplied, all the downloaded repos are placed in sub-directories
named with the username of the developer who wrote them.

For example, running this command (limiting the output to only 4 repositories, for brevity)....

```bash
obsidian-repos-downloader.py  --limit 4 --group-by-user
```

... gives this directory structure:

<!-- snippet: tree-output-grouped.txt -->
```txt
plugins
├── agathauy
│   └── wikilinks-to-mdlinks-obsidian
└── aidenlx
    ├── alx-folder-note
    ├── better-fn
    └── cm-chs-patch
themes
├── ArtexJay
│   └── Obsidian-CyberGlow
├── auroral-ui
│   └── aurora-obsidian-md
└── bcdavasconcelos
    ├── Obsidian-Ayu
    └── Obsidian-Ayu_Mirage

13 directories
```
<!-- endSnippet -->

## Likely Questions

### How do I update repos I have already downloaded?

This is now done automatically, via `git pull`, for repos that have already been cloned.

### What order are plugins and themes downloaded in?

They are downloaded in case-insensitive alphabetical order of the repository's GitHub URL, so effectively in order
of user name and then repo name.

### What if there is an error?

Sometimes it is not possible to update a repo, for example of there are edited files on the local machine, or the name of the remote branch has changed (such as from 'master' to 'main').

The script accumulates a list of errors, and prints them on completion.

The easiest way to deal with such errors is to delete the downloaded repo, and run the script again.

Example error output:

```
The following errors occurred:
updating Slowbad/obsidian-solarized
command:    git pull --quiet
in:         /Users/clare/obsidian-repos-downloader/themes/Slowbad-obsidian-solarized
exit code:  1
stdout:
stderr:     Your configuration specifies to merge with the ref 'refs/heads/master'
from the remote, but no such ref was fetched.

-------------------------------------------------------------------------------
```

## Alternatives

There is a growing number of alternative mechanisms for downloading Obsidian repos:

* [konhi/**obsidian-repositories-downloader**](https://github.com/konhi/obsidian-repositories-downloader):
  * Requires Node
  * Downloads plugins only
* [luckman212/**obsidian-plugin-downloader**](https://github.com/luckman212/obsidian-plugin-downloader)
  * Written in bash, and a number of other freely-downloadable tools
  * You use a console GUI each run, to search and control which repos to download
  * Downloads plugins only

## 🔨 Other Tools

* [Everything](https://www.voidtools.com/): advanced search
* [obsidian-plugin-downloader](https://github.com/luckman212/obsidian-plugin-downloader): similiar tool written in Shell

## 👾 Usage

```bash
git clone https://github.com/konhi/obsidian-repositories-downloader.git
cd obsidian-repositories-downloader
npm start
```

* Tested with `node v12.22.7`.
* In case of any problems, you may try updating your nodejs version to newest. ([see this issue](https://github.com/konhi/obsidian-repositories-downloader/issues/2)). You may also try using [this shell tool](https://github.com/luckman212/obsidian-plugin-downloader).
