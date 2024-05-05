
# Django Chat App

This README provides an overview of the structure and features of a Django chat application built using Django Channels and WebSockets.



## Overview
This project demonstrates the creation of a real-time chat application using Django Channels and WebSockets. The app allows users to join chat rooms, send messages, and interact in real-time.

## Files

* **`room/`**: Contains the Django app for the chat functionality.
    * `models.py`: Defines models for chat rooms and messages.
    * `views.py`: Handles HTTP and WebSocket connections.
    * `consumers.py`: Implements WebSocket consumers for chat functionality.
    * `urls.py`: Defines URL routing for the app.
* **`templates/room/`**: Contains HTML templates for the chat application.
* **`settings.py`**: Includes configuration for Django Channels.

## Features
* **User Authentication**: Secure access with Django’s authentication system.
* **Chat Rooms**: Users can join rooms to chat in real-time.
* **Message History**: Messages stored in the database for retrieval and display.
* **Real-Time Notifications**: Users are notified in real-time of new messages and other events.
* **Responsive Design**: The UI is responsive and works well on various devices.

## How to use
1. **Clone the repository**: Clone the project repository to your local machine.
    ```bash
    git clone <repository_url>
    ```
2. **Set up a virtual environment**: Create a virtual environment and activate it.
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**: Install dependencies from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
4. **Apply migrations**: Create the necessary database tables.
    ```bash
    python manage.py migrate
    ```
5. **Run the server**: Start the development server.
    ```bash
    python manage.py runserver
    ```
6. **Access the app**: Open a web browser and navigate to `http://localhost:8000/` to interact with the app.

## Contributing

* Contributions are welcome! Feel free to fork the repository and submit a pull request for any improvements.

