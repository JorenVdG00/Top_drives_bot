from PIL import Image
import cv2
standard_size = (2210, 1248)

def get_pixel_color(img_path, x, y):
    img = Image.open(img_path)
    resized_img = img.resize(standard_size)
    return resized_img.getpixel((x, y))


ticket_img = './bot_screenshots/in_event.png'
accept_skip_img = './bot_screenshots/accept_skip.png'
prize_stars_img = './bot_screenshots/prizes_stars.png'
upgrade_after_match_img = './bot_screenshots/upgrade_after_match.png'
empty_ticket_img = './bot_screenshots/empty_ticket.png'
cannot_play_img = './bot_screenshots/cannot_play.png'
selected_hand_fault_img_path = './bot_screenshots/selected_hand_fault.png'
event_unavailable_img_path = './bot_screenshots/event_unavailable.png'

img = event_unavailable_img_path
# x, y = 890, 1150 # ticket
# x, y = 1290, 830 # accept skip
# x, y = 2000, 200 # stars
# x, y = 195, 413 # available_prizecard
# x, y = 1031, 178 # Upgrade_after_match
# x, y = 840, 1300 # cannot_play
# x,y= 490, 815 # selected_hand_fault
x,y = 1978, 285 # event_unavailable
color = get_pixel_color(img, x, y)
print(color)
