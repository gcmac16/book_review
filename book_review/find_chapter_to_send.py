import argparse
from pathlib import Path

import yaml

from send_chapter import (
   send_book_review,
)


DATA_PATH = Path('.')

def load_config():
    with open(DATA_PATH/'config.yaml', 'r') as config_file :
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    
    return config


def get_book_metadata(book_name):
    book_metadata_path = DATA_PATH/'books'/book_name/'meta.yaml'
    with open(book_metadata_path, 'r') as metadata_file:
        metadata = yaml.load(metadata_file, Loader=yaml.FullLoader)

    return metadata


def get_next_chapter(config):
    book_metadata = get_book_metadata(config['current_book']) 
    next_chapter = config['chapter_to_send'] + 1

    if next_chapter <= book_metadata['chapters']:
        chapter_num = config['chapter_to_send'] + 1
        return config['current_book'], chapter_num
    else:
        next_book = find_next_book(current_book, previous_book)
        return next_book, 1


def update_config(config, book, chapter_num): 
    config['chapter_to_send'] = chapter_num
    if book != config['current_book']:
        config['previous_book'] = config['current_book']
        config['current_book'] = book

    with open(DATA_PATH/'config.yaml', 'w') as config_file:
        yaml.dump(config, config_file)


def main():
    config = load_config()
    current_book, current_chapter = config['current_book'], config['chapter_to_send']
    send_book_review(current_book, current_chapter)
    next_book, next_chapter = get_next_chapter(config)    
    update_config(config, next_book, next_chapter)


if __name__ == '__main__':
    main()
