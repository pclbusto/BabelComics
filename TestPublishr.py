from PublishersModule import *

publishers = Publishers()
publishers.searchInComicVineComicVine("Marvel")
for publisher in publishers.listaComicVineSearch:
    print(publisher.name, publisher.id)
publishers.close()
