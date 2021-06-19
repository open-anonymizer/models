import re

# from pandas import ExcelWriter
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


# Definition
def get_info(i):
    b = re.search("[0-9]{1,20}", str(i))
    if b:
        return b[0]
    else:
        None


# Gesamtnamenliste
link_gesamt = (
    "https://www.namenforschung.net/dfd/woerterbuch/gesamtliste-veroeffentlichter-namenartikel/"
)
page = requests.get(link_gesamt)
soup = bs(page.text)

a = soup.select("#maincontent li")

lastnames = [each.text for each in a]
# ids = [get_info(each) for each in a]

df_lastnames = pd.DataFrame({"per": lastnames})
# df_lastnames.head()

df_lastnames.to_csv(
    r"C:/projects/master/thesis/lexical_approach/res/german_lastnames.csv", sep=",", index=False
)


# vornamen
firstnames = []
for i in range(99):
    print(i)
    link_gesamt = f"https://www.vorname.com/deutsche,vornamen,{i+1}.html"  # 1-99
    page = requests.get(link_gesamt)
    soup = bs(page.text)

    # get names from current site i
    # female
    nameobjects = soup.find_all("a", {"class": "w-text"})
    vorname_seite_i = [each.text for each in nameobjects]
    # append names to list
    firstnames.extend(vorname_seite_i)

    # male
    nameobjects = soup.find_all("a", {"class": "m-text"})
    vorname_seite_i = [each.text for each in nameobjects]
    # append names to list
    firstnames.extend(vorname_seite_i)


# store as DF and csv
df_firstnames = pd.DataFrame({"per": firstnames})
df_firstnames.to_csv(
    r"C:/projects/master/thesis/lexical_approach/res/german_firstnames.csv", sep=",", index=False
)


# combine to sinngle CSV with first and lastname
full_df = df_firstnames.append(df_lastnames)
full_df.to_csv(r"C:/projects/master/thesis/lexical_approach/german_per.csv", sep=",", index=False)
