from elasticsearch_dsl import connections, Index, Mapping, Document, Date
import time


# init
es_endpoint = 'https://search-couchpotato-xxxx.eu-west-2.es.amazonaws.com/'

# create connection
conn = connections.create_connection(hosts=[es_endpoint])
index = 'couchpotato'

# create an index for our couchpotato documents ingestion
i = Index(index)
i.settings(number_of_shards=1, number_of_replicas=0)
i.save()
i.get()

m = Mapping()
m.field('event_dt', Date(format='epoch_second'))
m.save(index)

# write a sample document
class Person(Document):
    pass


doc = Person()
doc.event_dt = time.time()
doc.person = 'daddy'
doc.confidence = .9
doc.save(index=index)
