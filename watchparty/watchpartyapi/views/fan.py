"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from watchpartyapi.models import Fan


class Fans(ViewSet):
    """watch party fans"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single fan
        Returns:
            Response -- JSON serialized fan
        """
        try:
            fan = Fan.objects.get(pk=pk)
            serializer = FanSerializer(
                fan, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all fans
        Returns:
            Response -- JSON serialized list of fans
        """
        fans = Fan.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = FanSerializer(
            fans, many=True, context={'request': request})
        return Response(serializer.data)


class FanSerializer(serializers.ModelSerializer):
    """JSON serializer for fans
    Arguments:
        serializers
    """
    class Meta:
        model = Fan
        fields = ('user', 'fav_sport', 'fav_team')
