# Spotify Ad Skipper

Spotify Ad Skipper is a Python script that automatically closes the Spotify desktop player on Windows whenever an ad plays and then reopens it, effectively skipping the ad.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and usage purposes.

### Prerequisites

You will need the following Python libraries installed on your machine:

- spotipy
- pygetwindow
- pynput
- python-dotenv

You can install these libraries using pip:

```bash
pip install spotipy pygetwindow pynput python-dotenv
```
## Installation

1. Clone the repository or download the ZIP file and extract it.
2. Change the working directory to the location of the script.
3. Run the script using `python spotify_ad_skipper.py` (or `python3 spotify_ad_skipper.py` on some systems).

## Configuration

You need to create a `.env` file in the same directory as the script, containing your Spotify developer app credentials. Register your app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to get these credentials.

Add the following variables to the `.env` file:

```makefile
SPOTIPY_CLIENT_ID=<your_client_id>
SPOTIPY_CLIENT_SECRET=<your_client_secret>
SPOTIPY_REDIRECT_URI=<your_redirect_uri>
```

## Usage

1. Run the script using python spotify_ad_skipper.py (or python3 spotify_ad_skipper.py on some systems).
2. Follow the on-screen instructions to configure the Spotify desktop app directory path (if not already configured).
3. Choose the "Block Ads" option from the menu.
4. The script will now monitor the currently playing track and automatically restart the Spotify desktop player whenever an ad starts playing.

## Notes

- This script is for educational purposes only. Use it at your own risk.
- The script may not work if Spotify updates their desktop app or API, as it relies on specific behaviors of both.
- It is recommended to support the artists and Spotify by subscribing to Spotify Premium if you find their service valuable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
