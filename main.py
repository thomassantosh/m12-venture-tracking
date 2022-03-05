import re
import json
import subprocess
import logging
logging.basicConfig(level=logging.INFO,filename='history.log', format='%(asctime)s:%(levelname)s:%(message)s')

def retrieve_data():
    """Retrieve new data"""

    # Retrieve current data through subprocess
    output = str(subprocess.run(['curl','-k','https://m12.vc/portfolio'],\
            check=True, stdout=subprocess.PIPE,universal_newlines=True))

    # Parse out the company names, and descriptions
    name_reg = r"&quot;name&quot;:&quot;(.*?)&quot"
    name_list = re.findall(name_reg, output)

    desc_reg = r"&quot;description&quot;:&quot;(.*?)&quot"
    desc_list = re.findall(desc_reg, output)

    assert len(name_list) == len(desc_list)
    logging.info(f'Total company list : {len(desc_list)}')

    # Create dictionary from lists, and sort based on key
    company_dict = dict(zip(name_list, desc_list))
    company_dict = {k: company_dict[k] for k in sorted(company_dict)}
    #logging.info(f'Company dictionary: {company_dict}')

    ## Save to json file
    #with open('company_list.json', 'w') as f:
    #    f.write(json.dumps(company_dict))
    return company_dict

def compare_dictionaries(new_dict=None, source=None):
    """Compare the new pull and the old pull"""

    # Load the baseline dictionary
    with open(source, 'r') as f:
        old_dict = json.load(f)

    # Get their individual keys into a list for comparison
    old_dict_keys = sorted(old_dict)
    new_dict_keys = sorted(new_dict)

    # Compare and if different, save the new data
    if old_dict_keys == new_dict_keys:
        logging.info('No change. No update needed.')
    else:
        logging.info('Change in dictionary.')
        original_list = list( set(old_dict_keys) - set(new_dict_keys) )
        if len(original_list):
            logging.info(f'Companies in baseline list no longer in M12 list:{original_list}')
        else:
            logging.info(f'No change in baseline list.')
        logging.info(f'Companies in M12 list, new from baseline list:{list( set(new_dict_keys) - set(old_dict_keys) )}')


def main():
    """Main operational function"""
    company_dict = retrieve_data()

    compare_dictionaries(
            new_dict=company_dict, 
            source='./company_list_nov21.json'
            )

if __name__ == "__main__":
    main()
