from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import ImageGrab
import pygetwindow as gw

def capture_screenshot(window_title=""):
    if window_title == "":
        screenshot = ImageGrab.grab()
    else:
        window = gw.getWindowsWithTitle(window_title)[0]
        screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
    
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

def send_webhook(webhook_url, text, discord_id="", window_title=""):
    screenshot_path = capture_screenshot(window_title)
    mention = f"<@{discord_id}>" if discord_id else ""
    
    embed = DiscordEmbed(title='Game Update', description=f"{text} {mention}", color=5814783)
    embed.set_image(url='attachment://screenshot.png')
    
    webhook = DiscordWebhook(url=webhook_url, content="Here is the screenshot:", embeds=[embed])
    webhook.add_file(file=open(screenshot_path, 'rb'), filename='screenshot.png')
    response = webhook.execute()

    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print(f"Failed to send webhook: {response.status_code}")
