from ..models import Conversation, KnowledgeGraph

class ConversationService:
    @staticmethod
    def save_conversation(user_id, transcript):
        return Conversation.objects.create(
            user_id=user_id,
            transcript=transcript
        )

    @staticmethod
    def save_knowledge_graph(conversation_id, graph_data):
        return KnowledgeGraph.objects.create(
            conversation_id=conversation_id,
            graph_data=graph_data
        )

    @staticmethod
    def get_conversation_history(user_id):
        return Conversation.objects.filter(
            user_id=user_id
        ).order_by('-created_at')