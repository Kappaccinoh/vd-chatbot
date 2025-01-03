from ..models import Conversation, KnowledgeGraph

class ConversationService:
    @staticmethod
    def save_conversation(user_id, transcript):
        return Conversation.objects.create(
            user_id=user_id,
            transcript=transcript
        )
    
    @staticmethod
    def update_conversation(conversation_id, new_content):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.transcript += f"\n{new_content}"
            conversation.save()
            return conversation
        except Conversation.DoesNotExist:
            raise Exception(f"Conversation {conversation_id} not found")

    
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