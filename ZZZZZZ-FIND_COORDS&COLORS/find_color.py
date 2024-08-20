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
selected_hand_fault_img_path = 'bot_screenshots/events/selected_hand_fault.png'
event_unavailable_img_path = 'bot_screenshots/events/event_unavailable.png'
race_img_path = 'bot_screenshots/events/race.png'
clicked_event_img_path = 'bot_screenshots/clubs/clicked_event_2_req.png'
club_available_img_path = 'bot_screenshots/clubs/club_available.png'
club_not_available_img_path = 'bot_screenshots/clubs/club_not_available.png'
skip_ad_img_path = 'bot_screenshots/adds/skip_ad.png'
ads_img_path = 'bot_screenshots/adds/ads.png'
unavailable_ad_img_path = ('bot_screenshots/adds/unavailable_ad.png')
google_play_img_path = 'bot_screenshots/adds/google_play.png'
home_img_path = 'bot_screenshots/events/home.png'
event_not_possible_img_path = 'bot_screenshots/events/event_not_possible.png'



img = home_img_path
# x, y = 890, 1150 # ticket
# x, y = 1290, 830 # accept skip
# x, y = 2000, 200 # stars
# x, y = 195, 413 # available_prizecard
# x, y = 1031, 178 # Upgrade_after_match
# x, y = 840, 1300 # cannot_play
# x,y= 490, 815 # selected_hand_fault
# x,y = 1978, 285 # event_unavailable
# x,y = 2107, 44 # race_refreshing
# x, y = 2140, 1150  # final event
# x,y = 1853, 48
x,y = 639, 293
color = get_pixel_color(img, x, y)

print(color)
