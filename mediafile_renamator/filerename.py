import os
import pathlib
import logger
import re
import constants
import tvshow
from unidecode import unidecode

tv_show_pattern = re.compile(r'(.*?)s(\d+)e(\d+)|(.*?)season(\d+)e(\d+)|(.*?)s(\d+)episode(\d+)|(.*?)season(\d+)episode(\d+)')

def normalize_name(name):
    name = unidecode(name)
    norm_name = ''
    for chr in name:
        if chr not in 'abcdefghijklmnopqrstuvwxyz01123456789':
            norm_name += ' '
        else:
            norm_name += chr
    norm_name = norm_name.strip()        
    return re.sub(r'\s+', ' ', norm_name)

def get_files(dir):    
    result = list()
    try:
        content = os.listdir(dir)        
    except:
        logger.log_error()

    for item in content:
        fullname = os.path.join(dir, item)
        if os.path.isfile(fullname):
            result.append(pathlib.Path(fullname))
    return result

def get_movie_info(filename: str):
    pass

def get_tv_show_info(filename : str):
    filename = filename.lower()
    match = tv_show_pattern.match(filename)
    return (normalize_name(match[1]), int(match[2]), int(match[3]))

def get_video_type(filename : str):
    filename = filename.lower()
    if tv_show_pattern.match(filename):
        return 'tv_show'
    else:
        return 'movie'

def analyze_files(files):
    analyzed_files = dict()
    for file in files:        
        filename = file.stem
        ext = file.suffix        
        if ext in constants.video_ext or ext in constants.subtitles_ext:
            video_type = get_video_type(filename)
            if video_type == 'tv_show':      
                file_info = get_tv_show_info(filename)
                if not analyzed_files.get(file_info[0]):
                    analyzed_files[file_info[0]] = list()
                analyzed_files[file_info[0]].append(('tv_show', file, file_info[1], file_info[2]))                    
            elif video_type == 'movie':
                file_info = get_movie_info(filename)
                if not analyzed_files.get(file_info[0]):
                    analyzed_files[file_info[0]] = list()
                analyzed_files[file_info[0]].append(('movie', file, file_info[1]))
    return analyzed_files

def get_renamed_files(dir):
    files = get_files(dir)    
    analyzed_files = analyze_files(files)
    result = list()
    for title in analyzed_files.keys():
        if analyzed_files[title][0][0] == 'tv_show':
            tv_show = tvshow.TVShow()
            tv_show.load_info(title)
            for file_info in analyzed_files[title]:
                new_name = tv_show.get_episode_filename(file_info[2], file_info[3])
                ext = file_info[1].suffix
                if ext in constants.subtitles_ext:
                    new_name += '.' + constants.DEFAULT_SUBTITLES_LANG
                new_name += ext
                result.append((file_info[1].name, new_name))
    return result

def rename_files(dir, files):
    for file in files:
        os.rename(os.path.join(dir, file[0]), os.path.join(dir, file[1]))
