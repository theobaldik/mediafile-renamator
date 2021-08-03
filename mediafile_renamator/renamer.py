import os
import pathlib
import logger
import re
import constants
import tvshow
import movie
from unidecode import unidecode


tv_show_pattern = re.compile(r'(.*?)s(\d+)e(\d+)|(.*?)season(\d+)e(\d+)|(.*?)s(\d+)episode(\d+)|(.*?)season(\d+)episode(\d+)')
movie_pattern_res_p = re.compile(r'\d{3,4}p')
movie_pattern_res = re.compile(r'\d{3,4}')
movie_pattern_year = re.compile(r'\d{4}')

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

def is_resolution(resolution : int) -> bool:
    return resolution in [720, 1080, 1440, 2160, 4320]

class Analyzer:    
    @staticmethod
    def _get_video_type(filename : str) -> str:
        filename = filename.lower()
        if tv_show_pattern.match(filename):
            return 'tv_show'
        else:
            return 'movie'

    def __init__(self, dir : str) -> None:
        self.dir = dir
        self.files = list()
        self.movie_files = list()
        self.tv_show_files = list()
        self.music_files = list()
        self.tv_shows = dict()          # { TVShow : list((Path, season_num, episode_num)) }
        self.movies = dict()            # { Path : list(Movie) }
        self.music = dict()             # { Song : list(Path) }
        self._list_files()
        self._analyze_files()

    def _list_files(self) -> None:
        """
        Search all files within `dir` directory and stores them in `files` attribute
        """
        try:
            content = os.listdir(self.dir)
        except:
            logger.log_error()
        for item in content:
            fullname = os.path.join(self.dir, item)
            if os.path.isfile(fullname):
                self.files.append(pathlib.Path(fullname))

    def _analyze_files(self) -> None:
        """
        Analyzes type of files and stores them in object attributes
        """
        for file in self.files:
            filename = file.stem
            ext = file.suffix
            if ext in constants.video_ext or ext in constants.subtitles_ext:
                video_type = Analyzer._get_video_type(filename)
                if video_type == 'movie':
                    self.movie_files.append(file)
                elif video_type == 'tv_show':
                    self.tv_show_files.append(file)               
            elif ext in constants.audio_ext:
                self.music_files.append(file)

    def _analyze_tv_shows(self):
        title_show_dict = dict()        # { title : TVShow }
        for file in self.tv_show_files:
            filename = file.stem.lower()
            match = tv_show_pattern.match(filename)
            title = normalize_name(match[1])
            if title not in title_show_dict:
                tv_show = tvshow.TVShow()
                tv_show.load_info(title)
                title_show_dict[title] = tv_show
            tv_show = title_show_dict[title]
            if tv_show not in self.tv_shows:
                self.tv_shows[tv_show] = list()
            self.tv_shows[tv_show].append((file, int(match[2]), int(match[3])))
    
    def _analyze_movies(self):
        for file in self.movie_files:
            filename = file.stem.lower()
            filename_without_res = filename
            filename_without_year = filename
            for match in movie_pattern_res_p.finditer(filename):
                res = int(match[0][:-1])
                if is_resolution(res):
                    filename_without_res = filename[:match.start()]
                    break
            for match in movie_pattern_res.finditer(filename_without_res):
                res = int(match[0])
                if is_resolution(res):
                    filename_without_res = filename_without_res[:match.start()]
                    break
            match = None
            for match in movie_pattern_res.finditer(filename_without_res):
                pass
            if match:
                filename_without_year = filename_without_res[:match.start()]
                results = movie.Movie.get_results(normalize_name(filename_without_year), int(match[0]))
                if results:
                    self.movies[file] = results
                    continue            
            results = movie.Movie.get_results(normalize_name(filename_without_res))
            if results:
                self.movies[file] = results            

    def get_file_count(self):
        return len(self.movie_files) + len(self.tv_show_files) + len(self.music_files)

    def analyze_media(self) -> None:
        self._analyze_tv_shows()
        self._analyze_movies()

    def get_duplicities(self) -> dict:
        path_movies_dict = dict()
        for path in self.movies:
            if len(self.movies[path]) > 1:
                path_movies_dict[path] = self.movies[path]
        return path_movies_dict

    def remove_duplicities(self, path, movie):
        self.movies[path] = [movie,]

class Renamer:
    def __init__(self, dir, **kwargs) -> None:
        self.dir = dir
        self.tv_shows = kwargs.get('tv_shows')
        self.movies = kwargs.get('movies')
        self.music = kwargs.get('music')

        self.filenames = list()         # list((old_name, new_name))
        self._get_new_names()
        
    def _get_new_names(self):        
        for tv_show in self.tv_shows:            
            for info in self.tv_shows[tv_show]:
                new_name = tv_show.get_episode_filename(info[1], info[2], constants.DEFAULT_FORMATTING)
                if info[0].suffix in constants.subtitles_ext:
                    new_name += '.' + constants.DEFAULT_SUBTITLES_LANG
                new_name += info[0].suffix
                self.filenames.append((info[0].name, new_name))
        for movie_path in self.movies:
            movie = self.movies[movie_path][0]
            new_name = movie.get_filename(constants.DEFAULT_FORMATTING)
            if movie_path.suffix in constants.subtitles_ext:
                new_name += '.' + constants.DEFAULT_SUBTITLES_LANG
            new_name += movie_path.suffix
            self.filenames.append((movie_path.name, new_name))
    
    def rename_files(self):
        for filename in self.filenames:
            os.rename(os.path.join(self.dir, filename[0]), os.path.join(self.dir, filename[1]))
            