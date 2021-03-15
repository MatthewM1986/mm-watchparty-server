"""View module for handling requests about sport types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from watchpartyapi.models import WatchParty


class WatchParties(ViewSet):
    """watch party event"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single watch party
        Returns:
            Response -- JSON serialized watch party
        """
        try:
            watch_party = WatchParty.objects.get(pk=pk)
            serializer = WatchPartySerializer(
                watch_party, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all watch parties
        Returns:
            Response -- JSON serialized list of watch parties
        """
        watchparties = WatchParty.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = WatchPartySerializer(
            watchparties, many=True, context={'request': request})
        return Response(serializer.data)


class WatchPartySerializer(serializers.ModelSerializer):
    """JSON serializer for watch parties
    Arguments:
        serializers
    """
    class Meta:
        model = WatchParty
        fields = ('name', 'scheduled_time', 'game',
                  'location', 'number_of_fans')
