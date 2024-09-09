from ImageTools.Clubs.club_reader import extract_club_info
from ImageTools.Clubs.clean_clubs import fix_extracted_data


def evaluate_club_pick(fixed_data):
    # Ensure the conditions to join are met
    if fixed_data['req_status'] != 'MET':
        return None  # Skip if requirements are not met

    left_score = fixed_data['score-left_x']
    right_score = fixed_data['score-right_x']
    player_amount_left = fixed_data['player_amount-left_x']
    player_amount_right = fixed_data['player_amount-right_x']

    if left_score < 1000 and right_score < 1000:
        return 1

    # Check if the max player count is not exceeded
    if player_amount_left + player_amount_right >= 300:
        return None  # Skip if the player limit is exceeded

    weight_team = fixed_data['weight_team']
    left_team = fixed_data['name'].split(' ')[0]
    weight = fixed_data['weight']

    winning_team = ['right' if left_team != weight_team else 'left']

    if (left_score < 1000 and weight > 300 and winning_team == 'right') or \
            (right_score < 1000 and weight > 300 and winning_team == 'left'):
        return 1

    # urgency = min(left_score, right_score)
    pick_score = 0

    if weight > 300:
        if (winning_team == 'right' and left_score < 1000) or (winning_team == 'left' and right_score < 1000):
            return 1
        elif (winning_team == 'right' and left_score < 2500) or (winning_team == 'left' and right_score < 2500):
            return 25

        if winning_team == 'right':
            pick_score += right_score
        else:
            pick_score += left_score
    else:
        pick_score = (right_score + left_score) // 2
    return pick_score


def get_club_pick_score(club_dir_path):
    extracted_data = extract_club_info(club_dir_path)
    fixed_data = fix_extracted_data(extracted_data, club_dir_path)
    pick_score = evaluate_club_pick(fixed_data)
    return pick_score, fixed_data