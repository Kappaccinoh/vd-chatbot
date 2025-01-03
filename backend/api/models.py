from django.db import models

class Conversation(models.Model):
    user_id = models.IntegerField()
    transcript = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'

    def __str__(self):
        return f"Conversation {self.id} - User {self.user_id}"


class KnowledgeGraph(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    graph_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'knowledge_graphs'

    def __str__(self):
        return f"Knowledge Graph {self.id} for Conversation {self.conversation_id}"