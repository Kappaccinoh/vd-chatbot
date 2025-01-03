from django.contrib import admin
from .models import Conversation, KnowledgeGraph

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'created_at')
    list_filter = ('user_id', 'created_at')
    search_fields = ('transcript',)
    readonly_fields = ('created_at',)

@admin.register(KnowledgeGraph)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('graph_data',)
    readonly_fields = ('created_at',)