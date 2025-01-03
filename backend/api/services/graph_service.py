from neo4j import GraphDatabase

class KnowledgeGraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j://localhost:7687",
            auth=("neo4j", "password")
        )

    def process_topics(self, topics: list, conversation_id: int) -> dict:
        """
        Process topics and their relationships into Neo4j graph.
        
        Args:
            topics: List of topic dictionaries with format:
                [
                    {
                        "topic": "main topic",
                        "related_topics": ["related topic 1", "related topic 2"],
                        "relationship_type": "describes/contains/relates to/etc"
                    }
                ]
            conversation_id: ID of the conversation
            
        Returns:
            dict: Graph data summary
        """
        try:
            print(f"Processing {len(topics)} topics for conversation {conversation_id}")
            graph_data = {
                'nodes': [],
                'relationships': []
            }

            for topic_obj in topics:
                main_topic = topic_obj.get('topic')
                related_topics = topic_obj.get('related_topics', [])
                relationship_type = topic_obj.get('relationship_type', 'RELATES_TO')

                if not main_topic:  # Skip if no main topic
                    continue

                # Create main topic node
                self.create_topic_node(main_topic)
                graph_data['nodes'].append({
                    'id': main_topic,
                    'type': 'Topic'
                })

                # Process related topics
                for related_topic in related_topics:
                    # Create related topic node
                    self.create_topic_node(related_topic)
                    graph_data['nodes'].append({
                        'id': related_topic,
                        'type': 'Topic'
                    })

                    # Create relationship
                    self.create_relationship(main_topic, related_topic, relationship_type)
                    graph_data['relationships'].append({
                        'source': main_topic,
                        'target': related_topic,
                        'type': relationship_type
                    })

            # Add conversation reference
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (t:Topic)
                    WHERE t.name IN $topic_names
                    SET t.conversations = COALESCE(t.conversations, []) + $conv_id
                    """,
                    topic_names=[node['id'] for node in graph_data['nodes']],
                    conv_id=conversation_id
                )

            print(f"Successfully processed topics: {graph_data}")
            return graph_data

        except Exception as e:
            print(f"Error processing topics: {str(e)}")
            return {
                'nodes': [],
                'relationships': [],
                'error': str(e)
            }

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