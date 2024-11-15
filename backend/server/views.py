from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import uuid
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import twilio.rest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a Twilio client
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
api_key = os.environ["TWILIO_API_KEY_SID"]
api_secret = os.environ["TWILIO_API_KEY_SECRET"]
twilio_client = twilio.rest.Client(api_key, api_secret, account_sid)

def home(request):
    return render(request, "index.html")

def find_or_create_room(room_name):
    try:
        # try to fetch an in-progress room with this name
        twilio_client.video.rooms(room_name).fetch()
    except twilio.base.exceptions.TwilioRestException:
        # the room did not exist, so create it
        twilio_client.video.rooms.create(unique_name=room_name, type="go")

def get_access_token(room_name):
    # create the access token
    access_token = AccessToken(account_sid, api_key, api_secret, identity=uuid.uuid4().int)
    # create the video grant
    video_grant = VideoGrant(room=room_name)
    # Add the video grant to the access token
    access_token.add_grant(video_grant)
    return access_token

from django.http import JsonResponse


@api_view(["POST"])
def join_room(request):
    try:
        room_name = request.data.get("room_name")

        if not room_name:
            return JsonResponse({"error": "Room name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find an existing room with this room_name, or create one
        find_or_create_room(room_name)

        # Retrieve an access token for this room
        access_token = get_access_token(room_name)

        return JsonResponse({"token": access_token.to_jwt()})

    except Exception as e:
        print(f"Error in join_room: {e}")  # Log the error to the console (use proper logging in production)
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)