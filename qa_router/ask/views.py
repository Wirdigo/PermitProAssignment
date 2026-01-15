from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import QuestionRequestSerializer, AnswerResponseSerializer
from .services import process_question


@api_view(['Post'])
def ask(request):
    request_serializer = QuestionRequestSerializer(data=request.data)
    if not request_serializer.is_valid():
        print(request_serializer.errors)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    question = request_serializer.data['question']
    result  = process_question(question)
    response_serializer = AnswerResponseSerializer(result)
    return Response(response_serializer.data)
