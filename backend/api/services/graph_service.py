from neo4j import GraphDatabase

class KnowledgeGraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j://localhost:7687",
            auth=("neo4j", "password")
        )

    def process_topics(self, topics: list, conversation_id: int) -> dict:
        if not topics:
            print("❌ No topics to process")
            return {'nodes': [], 'relationships': []}

        print(f"\nProcessing topics for conversation {conversation_id}:")
        print(f"Received topics: {topics}")
        
        try:
            graph_data = {
                'nodes': set(),
                'relationships': []
            }

            for topic_obj in topics:
                main_topic = topic_obj.get('topic')
                if not main_topic:
                    print(f"⚠️ Skipping invalid topic object: {topic_obj}")
                    continue

                print(f"\nProcessing main topic: {main_topic}")
                graph_data['nodes'].add(main_topic)
                self.create_topic_node(main_topic)

                for related_topic in topic_obj.get('related_topics', []):
                    if not related_topic:
                        continue

                    print(f"Creating relationship: {main_topic} -> {related_topic}")
                    graph_data['nodes'].add(related_topic)
                    self.create_topic_node(related_topic)
                    
                    relationship_type = topic_obj.get('relationship_type', 'RELATES_TO')
                    self.create_relationship(main_topic, related_topic, relationship_type)
                    
                    graph_data['relationships'].append({
                        'source': main_topic,
                        'target': related_topic,
                        'type': relationship_type
                    })

            return {
                'nodes': list(graph_data['nodes']),
                'relationships': graph_data['relationships']
            }

        except Exception as e:
            print(f"❌ Error in process_topics: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'nodes': [], 'relationships': [], 'error': str(e)}

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