import requests
import json
import constants

class InvalidAPIException(Exception):
    pass


def test_tmdb_api_key(api_key : str) -> bool:
    """
    Checks whether The Movie Database API key is valid
    :param api_key: API key to test
    :returns: true if API key is valid
    :raises: `Exception` when testing goes wrong
    """
    r = requests.get('https://api.themoviedb.org/3/movie/550?api_key={api_key}')    
    if r.status_code == 401:
        return False
    elif r.status_code == 200:
        return True
    else:
        raise Exception('Test failure')    

def get_year(date: str) -> int:
    """
    Extracts year from given string
    :param date: date string
    :returns: year as integer
    """
    return int(date[:4])

class Movie:
    """Represents a movie"""
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.year = kwargs.get('year')
        self.language = kwargs.get('language')

    @staticmethod
    def get_results(name : str, year = None):
        """
        Gets search results for movies with matching title and year (optional)¨
        :param name: name of the movie
        :param year: year of the movie release
        :returns: list Movie objects matched with `name` and `year`
        """
        r = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={constants.TMDB_API_KEY}&query={name}&page=1')
        if r.status_code == 401:
            raise InvalidAPIException()
        js = json.loads(r.text)
        if js['total_results'] == 0:
            return list()
        else:
            results = list()
            if year:
                for result in js['results']:
                    if result['title'].lower() == name.lower():
                        movie = Movie(name=result['title'], id=result['id'], year=get_year(result['release_date']), language=result['original_language'])
                        if movie.year == year:                        
                            results.append(movie)
            else:
                for result in js['results']:
                    if result['title'].lower() == name.lower():
                        movie = Movie(name=result['title'], id=result['id'], year=get_year(result['release_date']), language=result['original_language'])                                             
                        results.append(movie)
                    
            return results   

    def get_filename(self, format='plex') -> str:
        """
        Gets normalized file name for movie using given format        
        :param format: formatting of file name
        :returns: normalized file name
        :raises: `Exception` when movie has no name loaded        
        """
        if not self.name:
            raise Exception('TV Show has no name loaded')        
        else:
            if format == 'plex':
                return f'{self.name} ({self.year})'