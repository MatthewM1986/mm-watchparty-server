"""View module for handling requests about sport types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from watchpartyapi.models import WatchParty, Fan, Game


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

    def create(self, request):
        """Handle POST operations for watch parties
        Returns:
            Response -- JSON serialized event instance
        """
        fan = Fan.objects.get(user=request.auth.user)

        watchparty = WatchParty()
        watchparty.name = request.data["name"]
        watchparty.scheduled_time = request.data["scheduled_time"]
        watchparty.location = request.data["location"]
        watchparty.number_of_fans = request.data["number_of_fans"]

        watchparty = WatchParty.objects.get(pk=request.data["fanId"])
        watchparty.game = game

        try:
            watchparty.save()
            serializer = WatchPartySerializer(
                watchparty, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class WatchPartySerializer(serializers.ModelSerializer):
    """JSON serializer for watch parties
    Arguments:
        serializers
    """
    class Meta:
        model = WatchParty
        fields = ('name', 'scheduled_time', 'game',
                  'location', 'number_of_fans')
        depth = 2
