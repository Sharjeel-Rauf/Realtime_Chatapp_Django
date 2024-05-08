# Import required modules
from django.shortcuts import render, redirect
from .models import *
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
from .forms import *
# Create your views here.


@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def selenium(request):
    return render(request, 'room/selenium.html')




# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_required
def like_video(request):
    if request.method == 'POST':
        form = VideoURLForm(request.POST)
        if form.is_valid():
            # Retrieve the YouTube video URL from the form
            video_url = form.cleaned_data['video_url']
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
                return redirect('selenium')
                
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
                # Return redirection when not needed to sign in
                return redirect('selenium')

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
                # Properly close the WebDriver and redirect
                driver.quit()

            return redirect('selenium')
    else:
        form = VideoURLForm()
    
    # If request method is GET, render the form
    return render(request, 'room/selenium.html', {'form': form})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})