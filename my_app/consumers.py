import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        print("WebSocket connection initiated...")
        await self.accept()  # Accept the WebSocket connection

        # Check if the client is already in the group
        if not hasattr(self, "added_to_group"):
            await self.channel_layer.group_add("video_feed_group", self.channel_name)  # Add to group
            self.added_to_group = True  # Mark the client as added to the group
            print("WebSocket connection established and added to group.")
        else:
            print("WebSocket connection already established.")

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        print(f"WebSocket disconnected with close code: {close_code}")
        if hasattr(self, "added_to_group"):
            await self.channel_layer.group_discard("video_feed_group", self.channel_name)  # Remove from group
            del self.added_to_group  # Remove the marker
            print("WebSocket removed from group.")

    async def receive(self, text_data):
        """
        Called when the WebSocket receives a message from the client.
        """
        print(f"Received message from client: {text_data}")
        await self.channel_layer.group_send(
            "video_feed_group",
            {
                "type": "send_detection_message",  # This should match the method name
                "message": text_data,  # Fixed: Changed "text" to "message"
            },
        )

    async def send_detection_message(self, event):
        """
        Send a detection message to the frontend.
        """
        message = event["message"]
        print(f"Sending detection message to client: {message}")
        await self.send(text_data=json.dumps({"message": message}))