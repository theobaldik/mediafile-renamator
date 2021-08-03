import click
from click.utils import echo
import constants
import renamer
import logger
import movie

def print_table(header, values):
    def print_hline(lengths):
        print('+', end='')
        for length in lengths:        
            print("".ljust(length + 2, '-'), end='+')
        print()

    cols = len(header)
    lengths = [0] * cols
    for i in range(cols):        
        lengths[i] = len(header[i])
    for value in values:
        for i in range(cols):
            if len(value[i]) > lengths[i]:
                lengths[i] = len(value[i])
    print_hline(lengths)    
    print('| ', end='')
    for i in range(cols):
        print(header[i].ljust(lengths[i], ' '), end=' | ')
    print()
    print_hline(lengths)
    for value in values:
        print('| ', end='')
        for i in range(cols):
            print(value[i].ljust(lengths[i], ' '), end=' | ')
        print()
    print_hline(lengths)

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("-v", "--version", is_flag=True, help="Show MFR version and exit.")
@click.option("--show-log", is_flag=True, help="Shows log file content and exit.")
@click.option("--clear-log", is_flag=True, help="Clear log file content and exit.")
@click.option("--flist", is_flag=True, help="Shows supported formats and exit.")
@click.argument("directory", nargs=1, type=click.Path(exists=True, readable=True), required=False)
def cli(version, show_log, clear_log, flist, directory):
    """
    Mediafile Renamator renames all your media files using your format as you wish. \n
    Simply run mfr <DIRECTORY> for rename all your media files in directory.
    """
    if version:
        click.echo(f"Mediafile Renamator version {constants.VERSION}")
        return
    if show_log:
        content = logger.get_log()
        if content:
            click.echo(content)
        else:
            click.echo("Log file is empty.")
        return
    if clear_log:
        logger.clear_log()
        click.echo("Log file was cleared.")
        return
    if flist:
        for format in constants.formats:
            print(format, end=" ")
    if directory:
        analyzer = renamer.Analyzer(directory)
        file_count = analyzer.get_file_count()
        if file_count == 0:
            click.echo(f'MFR did not recognize any files for renaming in {directory} folder.')
            return
        click.echo(f'{file_count} files was recognized for renaming in {directory} folder.')
        if len(analyzer.movie_files) and constants.TMDB_API_KEY == '':
            click.echo(f'{len(analyzer.movie_files)} movie files was found. MFR needs The Movie Database API key for renaming movie files.')
            click.echo("Please run 'mfr config --tmdbapi <YOUR_API_KEY>' to set the API key. See https://www.themoviedb.org/documentation/api for more info.")
            return
        analyzer.analyze_media()
        duplicities = analyzer.get_duplicities()
        if duplicities:
            click.echo(f'{len(duplicities)} files have alternative search results, plese choose one of alternatives.')
            for duplicity in duplicities:
                click.echo(f'\nAlternatives for {duplicity.name}')
                dup_lst = list()
                dup_temp = list()
                dup_index = 0
                for dup in duplicities[duplicity]:
                    dup_lst.append((str(dup_index), dup.name, str(dup.year), dup.language))
                    dup_temp.append(dup)
                    dup_index += 1
                print_table(('No', 'Title', 'Year', 'Language'), dup_lst)
                alt_num = -1
                while alt_num < 0 or alt_num > dup_index - 1:
                    alt_num = click.prompt(f'Which alternative shall be used (0 - {dup_index - 1})', type=int)
                analyzer.remove_duplicities(duplicity, dup_temp[alt_num])
        renamerr = renamer.Renamer(directory, tv_shows=analyzer.tv_shows, movies=analyzer.movies)
        click.echo('\nRenaming table preview:')
        print_table(('Old file name', 'New file name'), renamerr.filenames)
        confirm = 'x'
        while str(confirm).lower() not in 'yn':
            confirm = click.prompt('Do you agree with these changes? (y/n)', default='y')        
        if confirm == "y":
            renamerr.rename_files()
            click.echo("Renaming was completed!")
        else:
            click.echo("Renaming was aborted.")

@cli.command(no_args_is_help=True)
@click.option("-f", "--format", help="default formatting of filenames")
@click.option("-s", "--sublang", help="default subtitle language code")
@click.option("--tmdbapi", help="API key for The Movie Database")
@click.option("--reset", is_flag=True, help="Reset to default setting and exit.")
def config(format, sublang, reset, tmdbapi):
    """Configure MFR settings."""
    if reset:
        constants.reset_config()        
    if format:
        if format not in constants.formats:
            click.echo(f"{format} is not valid format. Run `mfr --flist` to show all valid formats.")
            return
        constants.DEFAULT_FORMATTING = format
    if sublang:
        constants.DEFAULT_SUBTITLES_LANG = sublang
    if tmdbapi:
        if movie.test_tmdb_api_key(tmdbapi):
            constants.TMDB_API_KEY = tmdbapi
            click.echo(f'The Movie Database API key was succesfuly set to {tmdbapi}')
        else:
            click.echo(f'The Movie Databae API key {tmdbapi} is not valid.')
            return
    if format or sublang or tmdbapi:
        constants.create_default_config()

if __name__ == "__main__":
    cli()
