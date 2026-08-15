"""
=========================================================
GSIS INSTITUTIONAL

KNOWLEDGE GRAPH INTELLIGENCE ENGINE

Version 1.0

Institutional Knowledge Relationship Layer

=========================================================
"""


from datetime import datetime
import uuid



class KnowledgeGraphEngine:


    def __init__(self):

        self.name = "Knowledge Graph Engine"

        self.status = "CREATED"

        self.nodes = []

        self.relationships = []





    def initialize(self):

        self.status = "ONLINE"


        print("==============================")
        print("KNOWLEDGE GRAPH ENGINE ONLINE")
        print("==============================")





    def create_node(
            self,
            category,
            name,
            data):


        node = {


            "id":

            str(uuid.uuid4()),


            "category":

            category,


            "name":

            name,


            "data":

            data,


            "created":

            str(datetime.utcnow())

        }



        self.nodes.append(node)


        return node






    def create_relationship(
            self,
            source,
            target,
            relationship):


        link = {


            "source":

            source,


            "target":

            target,


            "relationship":

            relationship,


            "created":

            str(datetime.utcnow())

        }



        self.relationships.append(link)


        return link






    def search_nodes(
            self,
            category):


        return [

            node

            for node in self.nodes

            if node["category"] == category

        ]






    def graph_report(self):


        return {


            "status":

            self.status,


            "nodes":

            len(self.nodes),


            "relationships":

            len(self.relationships)

        }
