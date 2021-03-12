"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from watchpartyapi.models import SportType


class SportTypes(ViewSet):
    """watch party sport types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single sport type
        Returns:
            Response -- JSON serialized sport type
        """
        try:
            sport_type = SportType.objects.get(pk=pk)
            serializer = SportTypeSerializer(
                sport_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all sport types
        Returns:
            Response -- JSON serialized list of game types
        """
        sporttypes = SportType.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = SportTypeSerializer(
            sporttypes, many=True, context={'request': request})
        return Response(serializer.data)


class SportTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    Arguments:
        serializers
    """
    class Meta:
        model = SportType
        fields = ('id', 'type')
