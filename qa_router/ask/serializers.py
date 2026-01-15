from rest_framework import serializers

class QuestionRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True,
        min_length=1,
        max_length=500
    )
class AnswerResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    source = serializers.ChoiceField(
        choices=["geo", "regulation", "unknown"]
    )