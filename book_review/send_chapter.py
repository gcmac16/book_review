import argparse
import os
from pathlib import (
    Path,
)
from typing import (
    Dict,
    List,
)

import yaml
from markdown2 import (
    markdown,
)

from fastmail import FastMail


DATA_PATH = Path('.')


def build_email_body(metadata: Dict, chapter_notes: List[str]) -> str:
    notes_as_html = ' '.join(
        [markdown(chapter_note) for chapter_note in chapter_notes]
    )

    title_html = f"<H1>{metadata['title']}</H1>"
    author_html = f"<H2>by {metadata['author']}</H2>"
    
    return f'<html><body>{title_html}{author_html}\n{notes_as_html}</body></html>'


def send_book_review(book: str, chapter: int):
    book_path = DATA_PATH/'books'/book
    book_metadata = yaml.safe_load(open(book_path/'meta.yaml')) 
    
    chapter_path = book_path/f'chapter_{chapter}.md'
    chapter_notes_list = open(chapter_path).readlines()

    email_body = build_email_body(book_metadata, chapter_notes_list)
    
    fm = FastMail('gcmac@fastmail.com', os.environ['FASTMAIL_PASSWORD'])
    fm.send_message('gcmac@fastmail.com', ['gcmac@fastmail.com'], email_body, 'Chapter test', 'html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--book')
    parser.add_argument('--chapter')

    args = parser.parse_args()
    send_book_review(args.book, args.chapter)

