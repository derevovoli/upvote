import pathlib
from string import Template


# Config

ideas_url = 'https://docs.google.com/spreadsheet/ccc?key=1Jd64aeV5uyW4C1EFTqc4womkSwG-3nyzujXPdms-drs&output=csv'


upvotes_url = 'https://docs.google.com/spreadsheet/ccc?key=1Y2gY4kBg2oYufDYuMXkGGpWDF1_hQhTVtX9Dj8oA55I&output=csv'


ideas_dir = pathlib.Path('ideas')

idea_filename_template = Template('$idea_key.yml')


template_main_page = pathlib.Path('templates/main-page.md')

template_idea_block = pathlib.Path('templates/idea-block.md')

csv_ideas_all = pathlib.Path('all-ideas.csv')

csv_votes_all = pathlib.Path('all-votes.csv')


