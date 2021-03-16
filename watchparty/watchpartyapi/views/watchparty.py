"""View module for handling requests about sport types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from watchpartyapi.models import WatchParty, Fan, Game
from watchpartyapi.views.game import GameSerializer


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
        # fan = Fan.objects.get(user=request.auth.user)

        watchparty = WatchParty()
        watchparty.name = request.data["name"]
        watchparty.scheduled_time = request.data["scheduled_time"]
        watchparty.location = request.data["location"]
        watchparty.number_of_fans = request.data["number_of_fans"]
        game = Game.objects.get(pk=request.data["gameId"])
        watchparty.game = game

        try:
            watchparty.save()
            serializer = WatchPartySerializer(
                watchparty, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a watch party
        Returns:
            Response -- Empty body with 204 status code
        """
        watchparty = WatchParty.objects.get(pk=pk)
        watchparty.name = request.data["name"]
        watchparty.scheduled_time = request.data["scheduled_time"]
        watchparty.location = request.data["location"]
        watchparty.number_of_fans = request.data["number_of_fans"]
        game = Game.objects.get(pk=request.data["gameId"])
        watchparty.game = game
        watchparty.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single watch party
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            watchparty = WatchParty.objects.get(pk=pk)
            watchparty.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    Arguments:
        serializers
    """
    class Meta:
        model = Game
        fields = ('sport_type', 'team_one', 'team_two', 'date', 'description')
        depth = 2


class WatchPartySerializer(serializers.ModelSerializer):
    """JSON serializer for watch parties
    Arguments:
        serializers
    """
    game = GameSerializer(many=False)

    class Meta:
        model = WatchParty
        fields = ('name', 'scheduled_time', 'game',
                  'location', 'number_of_fans')
        depth = 2
