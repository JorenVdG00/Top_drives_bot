# basics/find_coords_ss.py
import cv2

list_coords = []
coords = []
cropping = False

race_img_path = 'bot_screenshots/events/race.png'  # Path to your screenshot
home_img_path = 'bot_screenshots/events/home.png'
start_screen_img_path = 'bot_screenshots/events/start_screen.png'
accept_skip_img_path = 'bot_screenshots/events/accept_skip.png'
choose_car_img_path = 'bot_screenshots/events/choose_car.png'
event_page_img_path = 'bot_screenshots/events/event_page.png'
in_event_img_path = 'bot_screenshots/events/in_event.png'
play_event_img_path = 'bot_screenshots/events/play_event.png'
skip_match_img_path = 'bot_screenshots/events/skip_match.png'
prizes_img_path = 'bot_screenshots/events/prizes.png'
match_info_top_img_path = 'bot_screenshots/events/match_info_top.png'
match_info_bottom_img_path = 'bot_screenshots/events/match_info_bottom.png'
prizes_stars_img_path = 'bot_screenshots/events/prizes_stars.png'
upgrade_after_match_img_path = 'bot_screenshots/events/upgrade_after_match.png'
empty_ticket_img_path = 'bot_screenshots/events/empty_ticket.png'
cannot_play_img_path = 'bot_screenshots/events/cannot_play.png'
tst_img_path = 'bot_screenshots/events/tst.png'
selected_hand_fault_img_path = 'bot_screenshots/events/selected_hand_fault.png'
event_unavailable_img_path = 'bot_screenshots/events/event_unavailable.png'
event_not_possible_img_path = 'bot_screenshots/events/event_not_possible.png'

#CARS
maserati_img_path = '../ZZZZZ-TEST-IIIIIIIIMG/test_cropped_imgs/Maserati_Ghibli.png'

#CLUBS
click_clubs_img_path = 'bot_screenshots/clubs/click_clubs.png'
club_page_img_path = 'bot_screenshots/clubs/club_page.png'
clicked_event_img_path = 'bot_screenshots/clubs/clicked_event.png'
clicked_event_2_req_img_path = 'bot_screenshots/clubs/clicked_event_2_req.png'
club_available_img_path = 'bot_screenshots/clubs/club_available.png'
club_not_available_img_path = 'bot_screenshots/clubs/club_not_available.png'
event_exceed_rq_img_path = 'bot_screenshots/clubs/event_exceed_rq.png'
multi_req_img_path = 'bot_screenshots/clubs/multi_req.png'
multi_req_checked_img_path = 'bot_screenshots/clubs/multi_req_checked.png'
multi_req_unchecked_img_path = 'bot_screenshots/clubs/multi_req_unchecked.png'
not_req_met_img_path = 'bot_screenshots/clubs/not_req_met.png'
pick_cars_img_path = 'bot_screenshots/clubs/pick_cars.png'
req_checked_img_path = 'bot_screenshots/clubs/req_checked.png'
club_end_event_img_path = 'bot_screenshots/clubs/club_end_event.png'

#ADS
ads_img_path = 'bot_screenshots/adds/ads.png'
close_gift_img_path = 'bot_screenshots/adds/close_gift.png'
exit_img_path = 'bot_screenshots/adds/exit.png'
exit2_img_path = 'bot_screenshots/adds/exit2.png'
exit3_img_path = 'bot_screenshots/adds/exit3.png'
exit4_img_path = 'bot_screenshots/adds/exit4.png'
google_play_img_path = 'bot_screenshots/adds/google_play.png'
skip_ad_img_path = ('bot_screenshots/adds/skip_ad.png')
switch_screens_img_path = ('bot_screenshots/adds/switch_screens.png')
unavailable_ad_img_path = ('bot_screenshots/adds/unavailable_ad.png')

#EVENTS
event_types_1_2_img_path = '../ZZZZZ-TEST-IIIIIIIIMG/test/event_types1-2.png'
event_types_3_4_img_path = '../ZZZZZ-TEST-IIIIIIIIMG/test/event_types3-4.png'
in_game_event_img_path = '../image_reader/Failed_test/test_IMG/in_game_event.png'

event_img_coords_img_path = '../image_reader/Failed_test/event_test_V2_cropped/RACING_TRIALS_-_STAGE_2/1-1.png'


high_img_path = 'bot_screenshots/conditions/high.png'
sun_rolling_img_path = 'bot_screenshots/conditions/sun_rolling.png'
wet_img_path = 'bot_screenshots/conditions/wet2.png'

# img_path = sun_rolling_img_path
img_path = high_img_path



# standard_size = (2210, 1248)
# standard_size = (557, 343) #(cars)
# standard_size = (330, 220) #(events)
standard_size = (315, 85) #conditions


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
