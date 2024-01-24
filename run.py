from string import Template
import utils
import config
import pathlib

def update_ideas():
    ideas_csv = utils.download_csv(config.ideas_url)    
    
    local_ideas_csv = read_csv(config.csv_ideas_all)

    if ideas_csv != local_ideas_csv:
        write_csv(config.csv_ideas_all, ideas_csv)
    
    ideas = {str(idx): row for idx, row in enumerate(ideas_csv[1:], start=1)}
 
    for key, values in ideas.items():
        idea_path = config.ideas_dir.joinpath(config.idea_filename_template.substitute(idea_key=key))
        if not idea_path.exists():
            utils.write_yaml(
                idea_path,
                {
                    'title': values[1].strip(),
                    'description': values[2].strip(),
                    'contacts': values[3].strip(),
                    'date': values[0]
                }
            )
            
    return ideas


def update_votes():
    votes_csv = utils.download_csv(config.upvotes_url)    
    
    local_votes_csv = read_csv(config.csv_votes_all)

    if votes_csv != local_votes_csv:
        write_csv(config.csv_votes_all, votes_csv)


def get_ideas_rank():
    votes_csv = read_csv(config.csv_votes_all)

    votes = [vote[1] for vote in votes_csv[1:]]
    
    ranks_sorted = {i: votes.count(i) for i in votes}
    ranks_keys = list(ranks_sorted.keys())
    
    unranked_keys = []

    idea_keys = [file_idea.stem for file_idea in config.ideas_dir.iterdir() if file_idea.suffix in ['.yml']]
    for idea_key in idea_keys:
        if idea_key not in ranks_keys:
            unranked_keys.append(idea_key)
    
    return ranks_keys + unranked_keys


def generator_ideas_blocks_text(total_rank):
    text = ''
    for key in total_rank:
        idea_path = config.ideas_dir.joinpath(f'{key}.yml')
        if not idea_path.exists():
            continue
    
        idea_block_template = utils.read_file(config.template_idea_block)
        
        idea_data = utils.read_yaml(idea_path)
        idea_text = Template(idea_block_template).substitute(
            idea_key=key,
            idea_title=idea_data.get('title'),
            idea_description=idea_data.get('description'),
            idea_contacts=idea_data.get('contacts'),
            idea_date=idea_data.get('date')
        )
        text += idea_text
    return text


def run():
    update_ideas()
    update_votes()
    ideas_ranked = get_ideas_rank()
    ideas_blocks_text = generator_ideas_blocks_text(ideas_ranked)


    idea_main_page_template = utils.read_file(config.template_main_page)
    main_page_text = Template(idea_main_page_template).substitute(
        idea_blocks=ideas_blocks_text
    )
    utils.write_file('readme.md', main_page_text)



run()
