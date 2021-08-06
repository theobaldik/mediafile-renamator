# Mediafile Renamator

Mediafile Renamator is a basic application for renaming media files like movies, TV shows and songs. Works with subtitles too.

## Features

- detects TV shows, movies, music and subtitles by file name
- renaming TV show files and its subtitles using [TVmaze](https://www.tvmaze.com) API
- renaming movie files and its subtitles using [The Movie Database (TMDb)](https://www.themoviedb.org) API
- renaming music files *(not implemented yet)*

## Installing MFR

The easiest way to install MFR on your computer is just download the executable file matching your OS in [Releases](https://gitlab.com/Theobaldik/mediafile-renamator/-/releases).
You can also use these download links for latest version of MFR:

- **Windows**: **[mfr_0_0_2.exe](https://gitlab.com/Theobaldik/mediafile-renamator/uploads/885446693f756ce0d824e6cdbbe412ec/mfr_0_0_2.exe)**
- **Linux**: not available yet
- **Mac OS**: not available yet

If you have [python 3.6](https://www.python.org/) and above with [pip](https://pypi.org/) installed on your computer, you can of course use the source code to run the program. First install all requied packages listed in [requirements.txt](/requirements.txt) file using `pip install -r requirements.txt` command. Then just run `python .` within the *ft_converter* directory.

You can also use pip to install MFR to your comuputer using [setup.py](/setup.py) file. Note that for this option you need to download the whole repository except the *bin* folder. Then within the repository folder run `pip install .` command. This will automatically install all requied packages and the *mediafile-renamator* package into your *site-packages* folder.

## Usage


Make sure you are in MFR directory or you added the directory to system path. Rename the executable (e.g. *mfr_0_0_2.exe*) to *mfr*.

Run `mfr <DIRECTORY>` in command line or terminal to rename all files within this directory.

For renaming movie files MFR needs TMDb API key. To optain the key, please follow [TMDb](https://www.themoviedb.org/documentation/api) instructions.

## Examples

Renaming all TV show files in *C:\Users\FatCamel\TV Shows\Black Mirror\Season 01* directory:

```bash
mfr "C:\Users\FatCamel\TV Shows\Black Mirror\Season 01"
```

Setting up TMDb API key (API key used in example is not valid)

```bash
mfr config --tmdbapi ae991c097cc046639a47f38f2c1765c5
```

Changing formating to *plex*

```bash
mfr config --format plex
```
