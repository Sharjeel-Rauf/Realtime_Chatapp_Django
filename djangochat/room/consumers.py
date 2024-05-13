import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.http import HttpResponseForbidden
from room.views import like_video
from room.forms import VideoURLForm
from django.http import HttpRequest
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import logging

import re

from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)

logger = logging.getLogger(__name__)

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.video_group_name = 'video_%s' % self.video_id

        await self.channel_layer.group_add(
            self.video_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.video_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.like_video()

    async def like_video(self):
        # Construct the YouTube video URL using the video ID
        video_url = f"https://www.youtube.com/watch?v={self.video_id}"
        
        # Chrome options setup
        chrome_options = Options()
        profile_path = r"C:/Users/ehsan/AppData/Local/Google/Chrome/User Data/Default"
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)
        service = Service(executable_path="C:\\Program Files (x86)\\chromedriver.exe")

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logger.error(f"Error initializing Chrome WebDriver: {e}")
            return
                
        driver.get(video_url)
        time.sleep(5)  # Allow time for the page to load

        try:
            # Define the CSS selector for the "Sign in" button
            sign_in_css_selector = (
                ".yt-spec-button-shape-next.yt-spec-button-shape-next--outline"
                ".yt-spec-button-shape-next--call-to-action"
                ".yt-spec-button-shape-next--size-m"
                ".yt-spec-button-shape-next--icon-leading"
            )

            # Check for the "Sign in" button
            signin_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sign_in_css_selector))
            )
            
            # Click the "Sign in" button
            signin_button.click()
            logger.info("Successfully clicked the Sign In button.")

            # Enter email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_address = "sharjeel03317840080@gmail.com"  # Replace with your email
            email_input.send_keys(email_address)
            email_input.send_keys(Keys.ENTER)

            # Allow time for the next page to load
            time.sleep(5)

            # Enter password
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password = "SHETAAN1234"  # Replace with your password
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)

        except Exception as e:
            logger.error("User is already logged in or not required to sign in.", exc_info=True)

        # Locate and click the "Like" button
        try:
            # Define the CSS selector for the "Like" button
            like_css_selector = (
                ".yt-spec-button-shape-next--tonal"
                ".yt-spec-button-shape-next--size-m"
                ".yt-spec-button-shape-next--icon-leading"
                ".yt-spec-button-shape-next--segmented-start"
            )

            # Locate the "Like" button and click it
            like_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, like_css_selector))
            )
            like_button.click()
            logger.info("Successfully clicked the Like button.")
            # Allow time for the next page to load
            time.sleep(10)

        except Exception as e:
            logger.error(f"Error clicking Like button: {e}")

        finally:
            # Properly close the WebDriver
            driver.quit()
        
        
