from enum import unique, Enum


@unique
class FeedType(Enum):
    rss = 'rss'
    atom = 'atom'
