"""View module for handling requests about sport types"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from watchpartyapi.models import WatchParty, Fan, Game, WatchPartyFan
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
        fan = Fan.objects.get(user=request.auth.user)

        watchparty = WatchParty()
        watchparty.name = request.data["name"]
        watchparty.scheduled_time = request.data["scheduled_time"]
        watchparty.location = request.data["location"]
        watchparty.number_of_fans = request.data["number_of_fans"]
        watchparty.game = Game.objects.get(name=request.data["game"])

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

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing fans signing up for watch parties"""

        # A fan wants to sign up for a watchparty
        if request.method == "POST":

            watchparty = WatchParty.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            fan = Fan.objects.get(user=request.auth.user)

            try:
                # Determine if the user is already signed up
                registration = WatchPartyFan.objects.get(
                    watchparty=watchparty, fan=fan)
                return Response(
                    {'message': 'Fan has already signed up for this watch party.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except WatchPartyFan.DoesNotExist:
                # The user is not signed up.
                registration = WatchPartyFan()
                registration.watchparty = watchparty
                registration.fan = fan
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to leave a previously joined watch party
        elif request.method == "DELETE":
            # Handle the case if the client specifies a watch party
            # that doesn't exist
            try:
                watchparty = WatchParty.objects.get(pk=pk)
            except WatchParty.DoesNotExist:
                return Response(
                    {'message': 'Watch Party does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authenticated user
            fan = Fan.objects.get(user=request.auth.user)

            try:
                # Try to delete the signup
                registration = WatchPartyFan.objects.get(
                    watchparty=watchparty, fan=fan)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except WatchPartyFan.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for Watch Party.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class WatchPartyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Watch Party organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class WatchPartyFanSerializer(serializers.ModelSerializer):
    """JSON serializer for Watch Party organizer"""
    fan = WatchPartyUserSerializer(many=False)

    class Meta:
        model = WatchPartyFan
        fields = ['fan']


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    Arguments:
        serializers
    """
    class Meta:
        model = Game
        fields = ('name', 'sport_type', 'team_one',
                  'team_two', 'date', 'description')
        depth = 2


class WatchPartySerializer(serializers.ModelSerializer):
    """JSON serializer for watch parties
    Arguments:
        serializers
    """
    game = GameSerializer(many=False)

    class Meta:
        model = WatchParty
        fields = ('id', 'name', 'scheduled_time', 'game',
                  'location', 'number_of_fans')
        depth = 2
