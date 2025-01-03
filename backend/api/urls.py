from django.urls import path
from . import views

urlpatterns = [
    path('voice-input/', views.voice_input, name='voice-input'),
    path('chat-response/', views.chat_response, name='chat-response'),
    path('voice-output/', views.voice_output, name='voice-output'),
    path('knowledge-graph/', views.knowledge_graph, name='knowledge-graph'),
]