def get_authors_with_multiple_measures(meta_data):
    authors_list = []
    for i in range(len(meta_data["Authors"])):
        authors = meta_data["Authors"][i].split(", ")
        for author in authors:
            if author not in authors_list:
                authors_list.append(author)
    return authors_list
