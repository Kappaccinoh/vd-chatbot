from neo4j import GraphDatabase

class KnowledgeGraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j://localhost:7687",
            auth=("neo4j", "password")
        )

    def create_topic_node(self, topic):
        with self.driver.session() as session:
            session.run(
                "MERGE (t:Topic {name: $topic})",
                topic=topic
            )

    def create_relationship(self, topic1, topic2, relationship_type):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (t1:Topic {name: $topic1})
                MATCH (t2:Topic {name: $topic2})
                MERGE (t1)-[r:RELATES_TO {type: $rel_type}]->(t2)
                """,
                topic1=topic1,
                topic2=topic2,
                rel_type=relationship_type
            )