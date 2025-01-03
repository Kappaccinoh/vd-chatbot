from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Conversation, KnowledgeGraph
from .services.stt_service import STTService
from .services.tts_service import TTSService
from .services.graph_service import KnowledgeGraphService
from .services.conversation_service import ConversationService
from .services.openai_service import OpenAIService
from .utils.validators import validate_audio_file

@api_view(['POST'])
def voice_input(request):
    """Handle voice input: STT → Save → Process → TTS"""
    try:
        # Validate audio input
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response(
                {'error': 'No audio file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        validate_audio_file(audio_file)

        # Initialize services
        stt_service = STTService()
        conv_service = ConversationService()
        openai_service = OpenAIService()
        tts_service = TTSService()
        graph_service = KnowledgeGraphService()

        # 1. Convert speech to text
        user_input = stt_service.transcribe(audio_file)
        if not user_input:
            return Response(
                {'error': 'Could not transcribe audio'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Save initial conversation
        conversation = conv_service.save_conversation(
            request.data.get('user_id'),
            f"User: {user_input}"
        )

        # 3. Generate AI response
        ai_response = openai_service.generate_response(user_input)
        
        # 4. Update conversation with AI response
        conversation = conv_service.update_conversation(
            conversation.id,
            f"AI: {ai_response}"
        )

        # 5. Process knowledge graph
        topics = openai_service.extract_topics(user_input + " " + ai_response)
        graph_data = graph_service.process_topics(topics, conversation.id)
        
        # 6. Save knowledge graph
        knowledge_graph = KnowledgeGraph.objects.create(
            conversation_id=conversation.id,
            graph_data=graph_data
        )

        # 7. Convert AI response to speech
        audio_response = tts_service.synthesize_speech(ai_response)

        return Response({
            'conversation_id': conversation.id,
            'transcript': user_input,
            'response': ai_response,
            'audio_response': audio_response,
            'graph_id': knowledge_graph.id
        }, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def chat_response(request):
    """Handle text input and generate response"""
    try:
        conversation_id = request.data.get('conversation_id')
        user_message = request.data.get('message')
        
        if not user_message:
            return Response(
                {'error': 'No message provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize services
        openai_service = OpenAIService()
        conv_service = ConversationService()
        graph_service = KnowledgeGraphService()

        # Generate AI response
        ai_response = openai_service.generate_response(user_message)

        # Update conversation
        conversation = conv_service.update_conversation(
            conversation_id,
            f"\nUser: {user_message}\nAI: {ai_response}"
        )

        # Update knowledge graph
        topics = openai_service.extract_topics(user_message + " " + ai_response)
        graph_data = graph_service.process_topics(topics, conversation_id)
        
        KnowledgeGraph.objects.create(
            conversation_id=conversation_id,
            graph_data=graph_data
        )

        return Response({
            'response': ai_response,
            'graph_data': graph_data
        })

    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def voice_output(request):
    """Convert text to speech"""
    try:
        text = request.data.get('text')
        if not text:
            return Response(
                {'error': 'No text provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        tts_service = TTSService()
        audio_data = tts_service.synthesize_speech(text)

        return Response({
            'audio_data': audio_data
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_conversation_history(request, user_id):
    """Get conversation history for a user"""
    try:
        conv_service = ConversationService()
        history = conv_service.get_conversation_history(user_id)
        
        return Response({
            'conversations': [{
                'id': conv.id,
                'transcript': conv.transcript,
                'created_at': conv.created_at,
                'knowledge_graphs': [{
                    'id': graph.id,
                    'graph_data': graph.graph_data
                } for graph in conv.knowledgegraph_set.all()]
            } for conv in history]
        })

    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_knowledge_graph(request, conversation_id):
    """Get knowledge graph for a specific conversation"""
    try:
        graphs = KnowledgeGraph.objects.filter(conversation_id=conversation_id)
        
        return Response({
            'graphs': [{
                'id': graph.id,
                'graph_data': graph.graph_data,
                'created_at': graph.created_at
            } for graph in graphs]
        })

    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def delete_conversation(request, conversation_id):
    """Delete a conversation and its associated graphs"""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )