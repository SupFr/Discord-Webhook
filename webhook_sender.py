import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import ImageGrab
import pygetwindow as gw
import sys

def capture_screenshot():
    # Find the Roblox window by title
    window_title = "Roblox"
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
    except IndexError:
        print("Roblox window not found.")
        return None
    
    # Save the screenshot
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

def send_webhook(webhook_url, title, text, discord_id=""):
    # Capture the screenshot
    screenshot_path = capture_screenshot()
    if not screenshot_path:
        print("Failed to capture screenshot.")
        return
    
    # Create the embed
    mention = f"<@{discord_id}>" if discord_id else ""
    embed_description = f"{text}"  # Title and text combined in description
    embed = DiscordEmbed(title=title, description=embed_description, color=5814783)
    embed.set_image(url='attachment://screenshot.png')

    # Send the webhook with the screenshot
    webhook = DiscordWebhook(url=webhook_url, content=" {mention} ", embeds=[embed])
    webhook.add_file(file=open(screenshot_path, 'rb'), filename='screenshot.png')
    
    # Execute the webhook
    response = webhook.execute()

    # Clean up by removing the screenshot
    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print(f"Failed to send webhook: {response.status_code}")
    return response.status_code

# Get arguments from AHK (webhook_url, title, text, discord_id)
if len(sys.argv) < 4:
    print("Missing arguments.")
else:
    webhook_url = sys.argv[1]
    title = sys.argv[2]
    text = sys.argv[3]
    discord_id = sys.argv[4] if len(sys.argv) > 4 else ""
    send_webhook(webhook_url, title, text, discord_id)
