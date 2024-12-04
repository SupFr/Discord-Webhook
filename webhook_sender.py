import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import ImageGrab
import pygetwindow as gw

def capture_screenshot(window_title="Roblox"):
    try:
        # Find the Roblox window
        window = gw.getWindowsWithTitle(window_title)[0]  # Assuming Roblox is the first window with this title
        screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
        
        # Save the screenshot
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error capturing Roblox window: {e}")
        return None

def send_webhook(webhook_url, text, discord_id=""):
    # Capture the screenshot of Roblox
    screenshot_path = capture_screenshot("Roblox")
    if screenshot_path is None:
        print("Failed to capture Roblox screenshot.")
        return
    
    # Create the embed
    mention = f"<@{discord_id}>" if discord_id else ""
    embed = DiscordEmbed(title='Roblox Update', description=f"{text} {mention}", color=5814783)
    embed.set_image(url='attachment://screenshot.png')

    # Send the webhook with the screenshot
    webhook = DiscordWebhook(url=webhook_url, content="Here is the Roblox screenshot:", embeds=[embed])
    webhook.add_file(file=open(screenshot_path, 'rb'), filename='screenshot.png')
    
    # Execute the webhook
    response = webhook.execute()

    # Clean up by removing the screenshot
    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print(f"Failed to send webhook: {response.status_code}")

    return response.status_code

# Example usage
if __name__ == "__main__":
    webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'
    send_webhook(webhook_url, "Roblox is running!", "123456789012345678")
