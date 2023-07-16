import os

import country_converter as coco
import pandas as pd

CURR_FILEPATH = os.path.dirname(__file__)

artists_path = os.path.join(CURR_FILEPATH, "../Artists.csv")
artists = pd.read_csv(artists_path)

artists_with_nationalities = artists.query(
    "`Nationality`.notnull() & `Nationality` != 'Nationality unknown'"
)

# manual cleaning for demonyms not in demonyms.csv,
# but can be mapped to an appropriate country in demonyms.csv
# to make counting of **countries** accurate

artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Beninese", "Nationality"
] = "Beninois"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Canadian Inuit", "Nationality"
] = "Canadian"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Coptic", "Nationality"
] = "Egyptian"  # this is a best guess
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Korean", "Nationality"
] = "South Korean"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Native American", "Nationality"
] = "American"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Catalan", "Nationality"
] = "Spanish"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Yugoslav", "Nationality"
] = "Serbian"  # serbia is the largest country today that used to form yugoslavia
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Scottish", "Nationality"
] = "Uk"
artists_with_nationalities.loc[
    artists_with_nationalities["Nationality"] == "Welsh", "Nationality"
] = "Uk"

nationality_count = (
    artists_with_nationalities.groupby(by="Nationality")["Nationality"]
    .count()
    .reset_index(name="count")
)


# https://github.com/knowitall/chunkedextractor/blob/master/src/main/resources/edu/knowitall/chunkedextractor/demonyms.csv
demonyms_path = os.path.join(CURR_FILEPATH, "demonyms.csv")
demonyms = pd.read_csv(demonyms_path, names=["demonym", "country"])

country_count = nationality_count.merge(
    demonyms, how="left", left_on="Nationality", right_on="demonym"
)

cc = coco.CountryConverter()

country_count["iso3_codes"] = cc.pandas_convert(
    series=country_count["country"], to="ISO3"
)

country_count_path = os.path.join(CURR_FILEPATH, "CountryCount.csv")
country_count.to_csv(country_count_path, index=False)

single_artists = country_count.query("`count` == 1")["Nationality"].tolist()
solo_representations = artists[artists['Nationality'].isin(single_artists)]

solo_representations_path = os.path.join(CURR_FILEPATH, "SoloRepresentations.csv")
solo_representations.to_csv(solo_representations_path, index=False)
