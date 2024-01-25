import pathlib
from string import Template


# Config

ideas_url = 'https://docs.google.com/spreadsheet/ccc?key=16H5Wtpu3-r9oHKHh8qTbaMemLOviVh1bz_CQ-2VMWwI&output=csv'


upvotes_url = 'https://docs.google.com/spreadsheet/ccc?key=1s4sFWqQIDfl8kRPQaxcpQpDfByomRwlYDUwVwAhNYRE&output=csv'


ideas_dir = pathlib.Path('ideas')

idea_filename_template = Template('$idea_key.yml')


template_main_page = pathlib.Path('templates/main-page.md')

template_idea_block = pathlib.Path('templates/idea-block.md')

csv_ideas_all = pathlib.Path('all-ideas.csv')

csv_votes_all = pathlib.Path('all-votes.csv')


