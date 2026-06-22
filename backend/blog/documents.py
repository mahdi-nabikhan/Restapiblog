from  django_elasticsearch_dsl import Decument
from django_elasticsearch_dsl.registries import registry
from .models import *

@registry.register_document
class PostDocument (Decument):
    class Index:
        name = 'posts'
        settings = {
            'number_of_shards':1,
            'number_of_replicas':1
        }
    class Django:
        model=Post
        fields = ['title']
    