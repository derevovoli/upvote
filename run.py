from string import Template
import utils
import config
import pathlib

def write_ideas(ideas):
    for key, values in ideas.items():
        idea_path = config.ideas_dir.joinpath(config.idea_filename_template.substitute(idea_key=key))
        if idea_path.exists():
            continue
            
        utils.write_yaml(
            idea_path,
            {
                'title': values[1].strip(),
                'description': values[2].strip(),
                'contacts': values[3].strip(),
                'date': values[0]
            }
        )


def update_ideas():
    ideas_csv = utils.download_csv(config.ideas_url)

    ideas = {str(idx): row for idx, row in enumerate(ideas_csv[1:])}
    print(ideas)
    
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


def get_ideas_rank(ideas_dict):
    upvotes_csv = utils.download_csv(config.upvotes_url)

    collections = [row[1] for row in upvotes_csv[1:]]
    
    ranks_sorted = {i: collections.count(i) for i in collections}
    ranks_keys = list(ranks_sorted.keys())
    
    unranked_keys = []
    for idea_key in ideas_dict.keys():
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
    ideas_all = update_ideas()
    ideas_ranked = get_ideas_rank(ideas_all)
    ideas_blocks_text = generator_ideas_blocks_text(ideas_ranked)


    idea_main_page_template = utils.read_file(config.template_main_page)
    main_page_text = Template(idea_main_page_template).substitute(
        idea_blocks=ideas_blocks_text
    )
    utils.write_file('readme.md', main_page_text)

