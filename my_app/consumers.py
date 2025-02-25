import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        print("WebSocket connection initiated...")
        await self.accept()  # Accept the WebSocket connection
        await self.channel_layer.group_add("video_feed_group", self.channel_name)  # Add to group
        print("WebSocket connection established and added to group.")

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        print(f"WebSocket disconnected with close code: {close_code}")
        await self.channel_layer.group_discard("video_feed_group", self.channel_name)  # Remove from group

    async def receive(self, text_data):
        """
        Called when the WebSocket receives a message from the client.
        """
        print(f"Received message from client: {text_data}")
        await self.channel_layer.group_send(
            "video_feed_group",
            {
                "type": "send_detection_message",  # This should match the method name
                "text": text_data,
            },
        )

    async def send_detection_message(self, event):
        """
        Send a detection message to the frontend.
        """
        message = event["message"]
        print(f"Sending detection message to client: {message}")
        await self.send(text_data=json.dumps({"message": message}))