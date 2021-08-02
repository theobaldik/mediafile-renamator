import click
import constants
import filerename
import logger

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option('-v', '--version', is_flag=True, help='Show MFR version and exit.')
@click.option('--show-log', is_flag=True, help='Shows log file content and exit.')
@click.option('--clear-log', is_flag=True, help='Clear log file content and exit.')
@click.argument('directory', nargs=1, type=click.Path(exists=True, readable=True))
def cli(version, show_log, clear_log, directory):
    """
    Mediafile Renamator renames all your media files as you wish \n
    Simply run mfr <DIRECTORY> for rename all your media files.
    """
    if version:
        click.echo(f'Fat Text Converter version {constants.VERSION}')
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
        return    
    if directory:
        result = filerename.get_renamed_files(directory)
        click.echo(f'{len(result)} files was found for rename:')
        for file in result:
            click.echo(f'{file[0]}\t->\t{file[1]}')
        click.echo('\n')
        confirmation = 'x'
        while confirmation not in 'yn':
            confirmation = str(click.prompt('Do you agree with these changes? Y/n', default='y')).lower()
        if confirmation == 'y':
            filerename.rename_files(directory, result)
            click.echo('Renaming was completed!')
        else:
            click.echo('Renaming was aborted.')   

@cli.command(no_args_is_help=True)
# @click.option('-o', '--out', type=click.Choice(constants.outfile_modes), help='how to save output file')
@click.option('-f', '--format',  help='default formatting of filenames')
@click.option('-s', '--sublang', help='default subtitle language code')
@click.option('--reset', is_flag=True, help='Reset to default setting and exit.')
def config(format, sublang, reset):
    """Configure MFR settings."""
    if reset:
        constants.reset_config()
        return
    if format:
        if format not in constants.formats:
            click.echo(f'{format} is not valid encoding. Run `ftc --clist` to show all valid encodings.')
            return
        constants.DEFAULT_FORMATTING = format
    if sublang:                
        constants.DEFAULT_SUBTITLES_LANG = sublang    
    if format or sublang:
        constants.create_default_config()    

if __name__ == '__main__':
    pass
