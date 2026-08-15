"""
=========================================================
GSIS INSTITUTIONAL

KNOWLEDGE GRAPH INTELLIGENCE ENGINE

Version 1.0

Relationship Intelligence Layer

=========================================================
"""


from datetime import datetime
import uuid



class KnowledgeGraphEngine:


    def __init__(self):

        self.name = "Knowledge Graph Engine"

        self.status = "CREATED"

        self.entities = []

        self.relationships = []

        self.patterns = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("KNOWLEDGE GRAPH ENGINE ONLINE")
        print("==============================")





    def add_entity(
            self,
            entity_type,
            name):


        entity = {


            "id":

            str(uuid.uuid4()),


            "type":

            entity_type,


            "name":

            name,


            "time":

            str(datetime.utcnow())

        }



        self.entities.append(entity)


        return entity






    def create_relationship(
            self,
            source,
            relation,
            target):


        link = {


            "source":

            source,


            "relation":

            relation,


            "target":

            target,


            "time":

            str(datetime.utcnow())

        }



        self.relationships.append(link)


        return link






    def store_pattern(
            self,
            pattern,
            description):


        data = {


            "pattern":

            pattern,


            "description":

            description,


            "time":

            str(datetime.utcnow())

        }



        self.patterns.append(data)


        return data






    def knowledge_report(self):


        return {


            "status":

            self.status,


            "entities":

            len(self.entities),


            "relationships":

            len(self.relationships),


            "patterns":

            len(self.patterns)

        }
