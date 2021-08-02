import requests
import json


def get_year(date: str) -> int:
    """
    Extracts year from given string
    :param date: date string
    :returns: year as integer
    """
    return int(date[:4])


class Episode:
    """Represents TV Show episode"""
    def __init__(self, number: int, title: str):
        self.number = number
        self.title = title

    def normalized_title(self) ->  str:
        """
        Normalized title name for NTFS file system
        :returns: normalized title as string
        """
        norm = self.title.replace(':', '-')
        result = ''
        for chr in norm:
            result += ' ' if chr in '<>"/\\|?*' else chr
        return result


class Season:
    """Represents season of TV Show"""
    def __init__(self, number: int, year: int):
        """
        :param number: order number of season
        :param year: year of premiere
        """
        self.number = number        
        self.year = year
        self.episodes = dict()

    def __len__(self) -> int:
        return len(self.episodes)

    def __getitem__(self, index: int) -> Episode:
        return self.episodes[index]

    def __setitem__(self, index: int, episode: Episode) -> None:
        self.episodes[index] = episode


class TVShow:
    """Represents a TV Show"""
    def __init__(self):
        self.name = None
        self.id = None
        self.year = None
        self.language = None
        self.seasons = dict()

    def __len__(self) -> int:
        return len(self.seasons)

    def __getitem__(self, index: int) -> Season:
        return self.seasons[index]

    def __setitem__(self, index: int, season: Season) -> None:
        self.seasons[index] = season

    def _load_attributes(self, name: str) -> None:
        """
        Fetches attributes of TV Show using search name
        :param name: name of TV Show used for fetching
        :raises: `Exception` when `name` is not found
        """
        r = requests.get(f'https://api.tvmaze.com/singlesearch/shows?q={name}')
        if r.status_code != 200:
            raise Exception(f'TV Show {name} was not found')
        else:
            js = json.loads(r.text)
            self.name = js['name']
            self.id = js['id']
            self.year = get_year(js['premiered'])
            self.language = js['language']

    def _load_episodes(self) -> None:
        """
        Fetches episodes of TV Show
        :raises: `Exception` when `id` of TV Show is not valid
        """
        r = requests.get(f'https://api.tvmaze.com/shows/{self.id}/episodes')
        if r.status_code != 200:
            raise Exception(f'Episodes of TV Show {self.id} was not found')
        else:
            js = json.loads(r.text)
            for episode in js:
                season = episode['season']
                if not self.seasons.get(season):
                    self[season] = Season(season, get_year(episode['airdate']))
                self[season][episode['number']] = Episode(
                    episode['number'], episode['name'])

    def load_info(self, name: str) -> None:
        """
        Fetches attributes and episode list of TV Show
        :param name: name of TV Show used for fetching
        :raises: `Exception` when `name` is not found
        :raises: `Exception` when `id` of TV Show is not valid
        """
        self._load_attributes(name)
        self._load_episodes()

    def get_episode_filename(self, season: int, episode: int, format='plex') -> str:
        """
        Gets normalized file name for episode using given format
        :param season: number of season
        :param episode: number of episode
        :param format: formatting of file name
        :returns: normalized file name
        :raises: `Exception` when given wrong `season`, `episode` or TV Show has no name loaded        
        """
        if not self.name:
            raise Exception('TV Show has no name loaded')
        elif len(self) < 1:
            raise Exception('TV Show has no seasons loaded')
        elif season not in self.seasons.keys():
            raise Exception(f'Season {season} is not valid season number')
        elif episode not in self[season].episodes.keys():
            raise Exception(
                f'Episode {episode} is not valid episode number for season {season}')
        else:
            if format == 'plex':
                return self.name + ' - s' + str(season).zfill(2) + 'e' + \
                    str(episode).zfill(2) + ' - ' + self[season][episode].normalized_title()


def main():
    show = TVShow()
    show.load_info('ordinace v ruzove zahrade')
    print(show.id, show.name, show.year)
    print(show.get_episode_filename(2, 4))


if __name__ == '__main__':
    main()
