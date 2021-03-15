"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from watchpartyapi.models import Game


class Games(ViewSet):
    """watch party games"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(
                game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all games
        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    Arguments:
        serializers
    """
    class Meta:
        model = Game
        fields = ('sport_type', 'team_one', 'team_two', 'date', 'description')
        depth = 2
