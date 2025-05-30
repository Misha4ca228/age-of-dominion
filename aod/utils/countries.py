def filter_countries(country_ids, all_countries):

    return {cid: data for cid, data in all_countries.items() if cid in country_ids}