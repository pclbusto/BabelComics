from Publishers import Publisher,Publishers



publishers = Publishers()
publishers.searchInComicVine("Marvel")
for publisher in publishers.listaComicVineSearch:
    print(publisher.name,publisher.id)
publishers.close()