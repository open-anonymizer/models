import re

import pandas
import requests


### functions to send query to wikidata and get list of elements
# send query
def send_query(query, url="https://query.wikidata.org/sparql"):
    r = requests.get(url, params={"format": "json", "query": query})
    queryobject = r.json()
    return queryobject


# get actual values
def get_content_from_queryobj(queryobject, columnname):
    res_list = []
    for item in queryobject["results"]["bindings"]:
        try:
            res_list.append(item[columnname]["value"])
        except:
            None
    # res_list = []
    # for item in data['results']['bindings']:
    # try:
    #     res_list.append(item['FamiliennameLabel']['value'])
    # except:
    #     None
    return res_list


### create csv for LOC

query_LOC = """
    # all German settlements
    SELECT 
    #?item 
    ?itemLabel
    #?coord
    WHERE
    {
        ?item wdt:P31/wdt:P279* wd:Q486972;
                wdt:P17 wd:Q183;
                rdfs:label ?itemLabel;
                wdt:P625 ?coord;
            FILTER (lang(?itemLabel) = "de"). 
    }
    """


LOC_queryobj = send_query(query_LOC)
german_LOC = get_content_from_queryobj(LOC_queryobj, columnname="itemLabel")

# cleaning (filter out irrelevant locations)
def remove_obj_that_startwith(list, start_of_string_to_remove):
    content = [x for x in list if not x.startswith(start_of_string_to_remove)]
    print(f"pre: {len(list)}, post: {len(content)}")
    return content


# remove all irrelevant elements
for irrelevant_element in [
    "Baudenkmal ",
    "Siedlung ",
    "Teil ",
    "Wohnanlage ",
    "Wohnblock ",
    "Bodendenkmal ",
]:
    print(irrelevant_element)
    german_LOC = remove_obj_that_startwith(german_LOC, irrelevant_element)

# remove long names (very likely errors30
german_LOC = [x for x in german_LOC if len(x) < 25]
# remove all quotes
german_LOC = [x.replace('"', "") for x in german_LOC]
# remove all brackets + their content
german_LOC = [re.sub(r" ?\([^)]+\)", "", x) for x in german_LOC]
# remove duplicates
german_LOC = list(set(german_LOC))

len(german_LOC[0])

## write as file
df = pandas.DataFrame(data={"loc": german_LOC})
df.to_csv(r"C:/projects/master/thesis/lexical_approach/german_loc.csv", sep=",", index=False)
