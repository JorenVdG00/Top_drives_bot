# basics/find_coords_ss.py
import cv2

list_coords = []
coords = []
cropping = False

race_img_path = './bot_screenshots/race.png'  # Path to your screenshot
home_img_path = './bot_screenshots/home.png'
start_screen_img_path = './bot_screenshots/start_screen.png'
accept_skip_img_path = './bot_screenshots/accept_skip.png'
choose_car_img_path = './bot_screenshots/choose_car.png'
event_page_img_path = './bot_screenshots/event_page.png'
in_event_img_path = './bot_screenshots/in_event.png'
play_event_img_path = './bot_screenshots/play_event.png'
skip_match_img_path = './bot_screenshots/skip_match.png'
prizes_img_path = './bot_screenshots/prizes.png'
match_info_top_img_path = './bot_screenshots/match_info_top.png'
match_info_bottom_img_path = './bot_screenshots/match_info_bottom.png'
prizes_stars_img_path = './bot_screenshots/prizes_stars.png'
upgrade_after_match_img_path = './bot_screenshots/upgrade_after_match.png'
empty_ticket_img_path = './bot_screenshots/empty_ticket.png'
cannot_play_img_path = './bot_screenshots/cannot_play.png'
tst_img_path = './bot_screenshots/tst.png'
selected_hand_fault_img_path = './bot_screenshots/selected_hand_fault.png'
event_unavailable_img_path = './bot_screenshots/event_unavailable.png'

img_path = event_unavailable_img_path
standard_size = (2210, 1248)


def click_and_get_coords(event, x, y, flags, param):
    global coords, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        coords = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        coords.append((x, y))
        cropping = False
        cv2.rectangle(resized_img, coords[0], coords[1], (0, 255, 0), 2)
        cv2.imshow('image', resized_img)
        list_coords.append(coords)


img = cv2.imread(img_path)
resized_img = cv2.resize(img, standard_size, interpolation=cv2.INTER_AREA)
clone = resized_img.copy()
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_and_get_coords)

while True:
    cv2.imshow("image", resized_img)
    key = cv2.waitKey(1) & 0xFF

    # Press 'r' to reset the window
    if key == ord("r"):
        resized_img = clone.copy()
        list_coords = []
        coords = []

    # If the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break

cv2.destroyAllWindows()

print(list_coords)
