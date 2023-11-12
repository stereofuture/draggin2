import thumby
import time
import random

# Game states
ON_START_SCREEN = 0
COUNTDOWN = 1
RUNNING = 2
DISQUALIFIED = 3
SHOWING_RESULTS = 4
OPTIONS = 5

# Game Finals
course_length = thumby.display.width * 4

# State that doesn't reset
session_best = 0

# Initialize circle sprites for tree
light_on = bytearray([60,126,255,255,255,255,126,60])
light_off = bytearray([60,66,129,129,129,129,66,60])

big_light_on = bytearray([224,248,252,254,254,255,255,255,255,255,255,254,254,252,248,224,
           7,31,63,127,127,255,255,255,255,255,255,127,127,63,31,7]) 
big_light_off = bytearray([224,56,12,6,2,3,1,1,1,1,3,2,6,4,56,224,
           7,28,48,96,64,192,128,128,128,128,192,64,96,48,28,7])

thumby.display.setFPS(30)
thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

def reset_game():
    print("")
    global game_state, random_first_light_1_set, random_second_light_1_set, random_first_light_2_set, random_second_light_2_set
    global staged, countdown_timer, accumulating_variable, time_in_running_state, results_time, shift_needed, accumulating_timer, start_time
    global stage_1_sprite, stage_2_sprite, stage_3_sprite, stage_4_sprite
    global countdown3_2_sprite, countdown3_3_sprite, countdown2_2_sprite, countdown2_3_sprite, countdown1_2_sprite, countdown1_3_sprite
    global go_2_sprite, go_3_sprite, accumulating_variable_drawn
    
    game_state = ON_START_SCREEN
    random_first_light_1_set = 0
    random_second_light_1_set = 0
    random_first_light_2_set = 0
    random_second_light_2_set = 0
    staged = False
    countdown_timer = 4  # Initial countdown timer
    accumulating_variable = 0
    accumulating_variable_drawn = 0
    time_in_running_state = 0
    results_time = 0
    shift_needed = False
    accumulating_timer = 0
    start_time = 0
    
    # PLAIN MODE SPRITES
    # stage
    stage_1_sprite = thumby.Sprite(8, 8, light_off, 8, 0)
    stage_2_sprite = thumby.Sprite(8, 8, light_off, 18, 0)
    stage_3_sprite = thumby.Sprite(8, 8, light_off, 42, 0)
    stage_4_sprite = thumby.Sprite(8, 8, light_off, 52, 0)
    
    # countdown
    countdown3_2_sprite = thumby.Sprite(8, 8, light_off, 18, 10)
    countdown3_3_sprite = thumby.Sprite(8, 8, light_off, 42, 10)
    countdown2_2_sprite = thumby.Sprite(8, 8, light_off, 18, 20)
    countdown2_3_sprite = thumby.Sprite(8, 8, light_off, 42, 20)
    countdown1_2_sprite = thumby.Sprite(8, 8, light_off, 18, 30)
    countdown1_3_sprite = thumby.Sprite(8, 8, light_off, 42, 30)
    
    # go
    go_2_sprite = thumby.Sprite(16, 16, big_light_off, 0, 22)
    go_3_sprite = thumby.Sprite(16, 16, big_light_off, 52, 22)

reset_game()
# Main game loop
while True:
    thumby.display.fill(0)
    if game_state == ON_START_SCREEN:
        # Display "Press Start" on the screen
        thumby.display.drawText("Press", 15, 12, 1)
        thumby.display.drawText("Start", 15, 22, 1)

        if thumby.buttonA.pressed():
            random_first_light_1_set = random.randint(0,6)
            random_second_light_1_set = random.randint(0,6)
            random_first_light_2_set = random.randint(0,6)
            random_second_light_2_set = random.randint(0,6)
            game_state = COUNTDOWN

    elif game_state == COUNTDOWN:
        # Display countdown_timer on the screen
        # Tree involves random lighting of top sets of two, then counts down three yellows before lighting final green

        #PLAIN MODE
        # Tree Trunk
        thumby.display.drawFilledRectangle(29, 0, 10, 40, 1)
        
        thumby.display.drawSprite(stage_1_sprite)
        thumby.display.drawSprite(stage_2_sprite)
        thumby.display.drawSprite(stage_3_sprite)
        thumby.display.drawSprite(stage_4_sprite)
        
        thumby.display.drawSprite(countdown3_2_sprite)
        thumby.display.drawSprite(countdown3_3_sprite)
        thumby.display.drawSprite(countdown2_2_sprite)
        thumby.display.drawSprite(countdown2_3_sprite)
        thumby.display.drawSprite(countdown1_2_sprite)
        thumby.display.drawSprite(countdown1_3_sprite)

        thumby.display.drawSprite(go_2_sprite)
        thumby.display.drawSprite(go_3_sprite)

        # DQs can be a setting, maybe just reset the tree on false start
        # Countdown timer logic
        
        time.sleep(1)
        if random_second_light_2_set > 0 or random_second_light_1_set > 0:
            random_second_light_2_set -= 1
            random_second_light_1_set -= 1
            if random_second_light_1_set <= 0:
                stage_1_sprite = thumby.Sprite(8, 8, light_on, 8, 0)
                stage_2_sprite = thumby.Sprite(8, 8, light_on, 18, 0)
            if random_second_light_2_set <= 0:
                stage_3_sprite = thumby.Sprite(8, 8, light_on, 42, 0)
                stage_4_sprite = thumby.Sprite(8, 8, light_on, 52, 0)
        else:
            staged = True
        
        if staged and countdown_timer >= 0:
            # Update countdown timer
            # thumby.display.drawText(str(countdown_timer), 15, 16, 1)
            countdown_timer -= 1
            if countdown_timer == 3:
                countdown3_2_sprite = thumby.Sprite(8, 8, light_on, 18, 10)
                countdown3_3_sprite = thumby.Sprite(8, 8, light_on, 42, 10)
            if countdown_timer == 2:
                countdown3_2_sprite = thumby.Sprite(8, 8, light_off, 18, 10)
                countdown3_3_sprite = thumby.Sprite(8, 8, light_off, 42, 10)

                countdown2_2_sprite = thumby.Sprite(8, 8, light_on, 18, 20)
                countdown2_3_sprite = thumby.Sprite(8, 8, light_on, 42, 20)
            if countdown_timer == 1:
                countdown2_2_sprite = thumby.Sprite(8, 8, light_off, 18, 20)
                countdown2_3_sprite = thumby.Sprite(8, 8, light_off, 42, 20)

                countdown1_2_sprite = thumby.Sprite(8, 8, light_on, 18, 30)
                countdown1_3_sprite = thumby.Sprite(8, 8, light_on, 42, 30)
            if countdown_timer == 0:
                countdown1_2_sprite = thumby.Sprite(8, 8, light_off, 18, 30)
                countdown1_3_sprite = thumby.Sprite(8, 8, light_off, 42, 30)
                
                go_2_sprite = thumby.Sprite(16, 16, big_light_on, 0, 22)
                go_3_sprite = thumby.Sprite(16, 16, big_light_on, 52, 22)
        elif staged:
            # thumby.display.drawText("GO", 15, 16, 1)
            thumby.display.update()
            # Transition to RUNNING state when countdown is done
            game_state = RUNNING
            accumulating_timer = 0
        
    elif game_state == RUNNING:
        accumulating_timer += 1
        thumby.display.drawFilledRectangle(0, 0, accumulating_variable_drawn, 10, 1)
        if shift_needed:
            thumby.display.drawText(str("SHIFT!"), 10, 20, 1)
        # For debugging
        # thumby.display.drawText(str(accumulating_variable), 15, 16, 1)
        if thumby.buttonB.pressed() and not thumby.buttonA.pressed() and not thumby.buttonU.pressed() :
            # Player is holding the B button and nothing else
            if not shift_needed:
                accumulating_variable += 1
                if accumulating_variable % 4 == 0:
                    accumulating_variable_drawn += 1
            if accumulating_variable % 50 == 0:
                shift_needed = True
                
                # Stop accumulating until the A button is pressed
        if thumby.buttonA.pressed() and thumby.buttonU.pressed() and not thumby.buttonB.pressed():
            shift_needed = False
        if accumulating_variable >= course_length:
            game_state = SHOWING_RESULTS

    elif game_state == SHOWING_RESULTS:
        # Display results_time on the screen
        thumby.display.drawText("Run", 0, 0, 1)
        thumby.display.drawText("Best", 0, 10, 1)
        thumby.display.drawText(str(accumulating_timer), 30, 0, 1)
        thumby.display.drawText(str(session_best), 38, 10, 1)
        thumby.display.drawText("Push L", 8, 22, 1)
        thumby.display.drawText("To Reset", 0, 32, 1)
        if thumby.buttonL.pressed():
            if session_best > accumulating_timer or session_best == 0:
                session_best = accumulating_timer
            reset_game()
    thumby.display.update()
    
    # TODO:
    # Handle other game states (DISQUALIFIED, additional gameplay features, etc.)
    # Create unique shift points (first is usually shorter, etc)
    # Have progress be based on "speed", which means missed shifts still allow progress but slower
    # Create two player
    # Create DRAMA Mode, with zoomed in and accurate recreation of staging
    # Transition to using actual time
    # Fix 'Best' Bug
