import thumby
import time
import random

# Game states
ON_START_SCREEN = 0
COUNTDOWN = 1
RUNNING = 2
DISQUALIFIED = 3
SHOWING_RESULTS = 4
ON_OPTIONS_SCREEN = 5

# Game Finals
course_length = thumby.display.width * 4
light_interval = 0.75

# State that doesn't reset
session_best = 0
drama_mode = False
disqualifications = False

# Initialize circle sprites for tree
light_on = bytearray([60,126,255,255,255,255,126,60])
light_off = bytearray([60,66,129,129,129,129,66,60])

medium_light_on = bytearray([240,252,254,254,255,255,255,255,254,254,252,240,
           0,3,7,7,15,15,15,15,7,7,3,0])
medium_light_off = bytearray([240,156,6,2,3,1,1,3,2,6,156,240,
           0,3,6,4,12,8,8,12,4,6,3,0])

big_light_on = bytearray([224,248,252,254,254,255,255,255,255,255,255,254,254,252,248,224,
           7,31,63,127,127,255,255,255,255,255,255,127,127,63,31,7]) 
big_light_off = bytearray([224,56,12,6,2,3,1,1,1,1,3,2,6,4,56,224,
           7,28,48,96,64,192,128,128,128,128,192,64,96,48,28,7])

thumby.display.setFPS(60)
thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

option_1_sprite = thumby.Sprite(8, 8, light_off, 8, 0)
option_2_sprite = thumby.Sprite(8, 8, light_off, 18, 0)

def reset_game():
    global game_state, random_first_light_1_set, random_second_light_1_set, random_first_light_2_set, random_second_light_2_set
    global staged, accumulating_variable, shift_needed, disqualified, prestaged
    global stage_1_sprite, stage_2_sprite, stage_3_sprite, stage_4_sprite
    global countdown3_2_sprite, countdown3_3_sprite, countdown2_2_sprite, countdown2_3_sprite, countdown1_2_sprite, countdown1_3_sprite
    global go_2_sprite, go_3_sprite, accumulating_variable_drawn, t_phase_start, t_phase_elapsed
    global prestage_1_sprite, prestage_2_sprite, prestage_3_sprite, prestage_4_sprite
    
    game_state = ON_START_SCREEN
    random_first_light_1_set = random.random() * 5.0 + 1.0
    random_second_light_1_set = random.random() * 5.0 + 1.0
    random_first_light_2_set = random.random() * 5.0 + 1.0
    random_second_light_2_set = random.random() * 5.0 + 1.0
    staged = False
    prestaged = False
    accumulating_variable = 0
    accumulating_variable_drawn = 0
    shift_needed = False
    t_phase_start = 0
    t_phase_elapsed = 0
    disqualified = False
    
    # DRAMA MODE SPRITES
    prestage_1_sprite = thumby.Sprite(16, 16, big_light_off, 0, 4)
    prestage_2_sprite = thumby.Sprite(16, 16, big_light_off, 18, 4)
    prestage_3_sprite = thumby.Sprite(16, 16, big_light_off, 38, 4)
    prestage_4_sprite = thumby.Sprite(16, 16, big_light_off, 56, 4)
    
    stage_1_sprite = thumby.Sprite(16, 16, big_light_off, 0, 24)
    stage_2_sprite = thumby.Sprite(16, 16, big_light_off, 18, 24)
    stage_3_sprite = thumby.Sprite(16, 16, big_light_off, 38, 24)
    stage_4_sprite = thumby.Sprite(16, 16, big_light_off, 56, 24)
    
    countdown3_2_sprite = thumby.Sprite(12, 12, medium_light_off, 18, 0)
    countdown3_3_sprite = thumby.Sprite(12, 12, medium_light_off, 42, 0)
    countdown2_2_sprite = thumby.Sprite(12, 12, medium_light_off, 18, 14)
    countdown2_3_sprite = thumby.Sprite(12, 12, medium_light_off, 42, 14)
    countdown1_2_sprite = thumby.Sprite(12, 12, medium_light_off, 18, 28)
    countdown1_3_sprite = thumby.Sprite(12, 12, medium_light_off, 42, 28)
    
    go_2_sprite = thumby.Sprite(16, 16, big_light_off, 0, 22)
    go_3_sprite = thumby.Sprite(16, 16, big_light_off, 52, 22)
    
    # PLAIN MODE SPRITES
    # # stage
    # stage_1_sprite = thumby.Sprite(8, 8, light_off, 8, 0)
    # stage_2_sprite = thumby.Sprite(8, 8, light_off, 18, 0)
    # stage_3_sprite = thumby.Sprite(8, 8, light_off, 42, 0)
    # stage_4_sprite = thumby.Sprite(8, 8, light_off, 52, 0)
    
    # # countdown
    # countdown3_2_sprite = thumby.Sprite(8, 8, light_off, 18, 10)
    # countdown3_3_sprite = thumby.Sprite(8, 8, light_off, 42, 10)
    # countdown2_2_sprite = thumby.Sprite(8, 8, light_off, 18, 20)
    # countdown2_3_sprite = thumby.Sprite(8, 8, light_off, 42, 20)
    # countdown1_2_sprite = thumby.Sprite(8, 8, light_off, 18, 30)
    # countdown1_3_sprite = thumby.Sprite(8, 8, light_off, 42, 30)
    
    # # go
    # go_2_sprite = thumby.Sprite(16, 16, big_light_off, 0, 22)
    # go_3_sprite = thumby.Sprite(16, 16, big_light_off, 52, 22)

reset_game()
# Main game loop
while True:
    thumby.display.fill(0)
    if game_state == ON_START_SCREEN:
        # thumby.display.drawText("A Start", 5, 12, 1)
        # thumby.display.drawText("B Opts", 5, 22, 1)
        thumby.display.drawSprite(go_2_sprite)
        thumby.display.drawSprite(go_3_sprite)

        if thumby.buttonA.pressed():
            t_phase_start = time.ticks_ms()
            game_state = COUNTDOWN
        
        if thumby.buttonB.pressed():
            game_state = ON_OPTIONS_SCREEN

    elif game_state == ON_OPTIONS_SCREEN:
        
        if(drama_mode):
            option_1_sprite = thumby.Sprite(8, 8, light_on, 56, 12)
        else:
            option_1_sprite = thumby.Sprite(8, 8, light_off, 56, 12)
        
        if(disqualifications):
            option_2_sprite = thumby.Sprite(8, 8, light_on, 56, 22)
        else:
            option_2_sprite = thumby.Sprite(8, 8, light_off, 56, 22)
        
        thumby.display.drawText("Options", 5, 2, 1)
        thumby.display.drawText("Drama", 5, 12, 1)
        thumby.display.drawText("DQs", 5, 22, 1)
        thumby.display.drawSprite(option_1_sprite)
        thumby.display.drawSprite(option_2_sprite)

        if thumby.buttonU.pressed() and thumby.buttonA.justPressed():
            drama_mode = not drama_mode
        
        if thumby.buttonD.pressed() and thumby.buttonA.justPressed():
            disqualifications = not disqualifications

        if thumby.buttonL.pressed():
            game_state = ON_START_SCREEN

    elif game_state == COUNTDOWN:
        # Tree involves random lighting of top sets of two, then counts down three yellows before lighting final green

        #PLAIN MODE
        # Tree Trunk
        if drama_mode:
            if not staged:
                thumby.display.drawSprite(prestage_1_sprite)
                thumby.display.drawSprite(prestage_2_sprite)
                thumby.display.drawSprite(prestage_3_sprite)
                thumby.display.drawSprite(prestage_4_sprite)
                
                thumby.display.drawSprite(stage_1_sprite)
                thumby.display.drawSprite(stage_2_sprite)
                thumby.display.drawSprite(stage_3_sprite)
                thumby.display.drawSprite(stage_4_sprite)
            else:
                thumby.display.drawSprite(countdown3_2_sprite)
                thumby.display.drawSprite(countdown3_3_sprite)
                thumby.display.drawSprite(countdown2_2_sprite)
                thumby.display.drawSprite(countdown2_3_sprite)
                thumby.display.drawSprite(countdown1_2_sprite)
                thumby.display.drawSprite(countdown1_3_sprite)
        else:
            prestaged = True
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

        t_current = time.ticks_ms()
        t_phase_elapsed = time.ticks_diff(t_current, t_phase_start)/1000.0

        if not prestaged:
            if random_first_light_1_set <= t_phase_elapsed:
                stage_1_sprite = thumby.Sprite(8, 8, light_on, 8, 0)
                stage_2_sprite = thumby.Sprite(8, 8, light_on, 18, 0)
            if random_first_light_2_set <= t_phase_elapsed:
                stage_3_sprite = thumby.Sprite(8, 8, light_on, 42, 0)
                stage_4_sprite = thumby.Sprite(8, 8, light_on, 52, 0)
            
            if random_first_light_2_set <= t_phase_elapsed and random_first_light_1_set <= t_phase_elapsed:
                prestaged = True
                t_phase_start = time.ticks_ms()
        elif not staged:
            if random_second_light_1_set <= t_phase_elapsed:
                stage_1_sprite = thumby.Sprite(8, 8, light_on, 8, 0)
                stage_2_sprite = thumby.Sprite(8, 8, light_on, 18, 0)
            if random_second_light_2_set <= t_phase_elapsed:
                stage_3_sprite = thumby.Sprite(8, 8, light_on, 42, 0)
                stage_4_sprite = thumby.Sprite(8, 8, light_on, 52, 0)
            
            if random_second_light_2_set <= t_phase_elapsed and random_second_light_1_set <= t_phase_elapsed:
                staged = True
                t_phase_start = time.ticks_ms()
        else:
            if t_phase_elapsed <= light_interval:
                countdown3_2_sprite = thumby.Sprite(8, 8, light_on, 18, 10)
                countdown3_3_sprite = thumby.Sprite(8, 8, light_on, 42, 10)
            if light_interval < t_phase_elapsed <= (light_interval*2.0):
                countdown3_2_sprite = thumby.Sprite(8, 8, light_off, 18, 10)
                countdown3_3_sprite = thumby.Sprite(8, 8, light_off, 42, 10)

                countdown2_2_sprite = thumby.Sprite(8, 8, light_on, 18, 20)
                countdown2_3_sprite = thumby.Sprite(8, 8, light_on, 42, 20)
            if (light_interval*2.0) < t_phase_elapsed <= (light_interval*3.0):
                countdown2_2_sprite = thumby.Sprite(8, 8, light_off, 18, 20)
                countdown2_3_sprite = thumby.Sprite(8, 8, light_off, 42, 20)

                countdown1_2_sprite = thumby.Sprite(8, 8, light_on, 18, 30)
                countdown1_3_sprite = thumby.Sprite(8, 8, light_on, 42, 30)
            if (light_interval*3.0) < t_phase_elapsed <= (light_interval*4.0):
                countdown1_2_sprite = thumby.Sprite(8, 8, light_off, 18, 30)
                countdown1_3_sprite = thumby.Sprite(8, 8, light_off, 42, 30)
                
                go_2_sprite = thumby.Sprite(16, 16, big_light_on, 0, 22)
                go_3_sprite = thumby.Sprite(16, 16, big_light_on, 52, 22)
            if (light_interval*4.0) < t_phase_elapsed <= (light_interval*5.0):
                thumby.display.update()
                game_state = RUNNING
                t_phase_start = time.ticks_ms()
            if thumby.buttonB.pressed() and t_phase_elapsed < (light_interval*3.0) and disqualifications:
                disqualified = True
                game_state = SHOWING_RESULTS
        
    elif game_state == RUNNING:
        thumby.display.drawFilledRectangle(0, 0, accumulating_variable_drawn, 10, 1)
        if shift_needed:
            thumby.display.drawText(str("SHIFT!"), 10, 20, 1)
        # For debugging
        # thumby.display.drawText(str(accumulating_variable), 15, 16, 1)
        if thumby.buttonB.pressed() and not thumby.buttonA.pressed() and not thumby.buttonU.pressed() :
            if not shift_needed:
                accumulating_variable += 1
                if accumulating_variable % 4 == 0:
                    accumulating_variable_drawn += 1
            if accumulating_variable % 50 == 0:
                shift_needed = True

        if thumby.buttonA.pressed() and thumby.buttonU.pressed() and not thumby.buttonB.pressed():
            shift_needed = False
        if accumulating_variable >= course_length:
            t_current = time.ticks_ms()
            t_phase_elapsed = time.ticks_diff(t_current, t_phase_start)
            game_state = SHOWING_RESULTS

    elif game_state == SHOWING_RESULTS:
        if disqualified:
            formatted_run_time = "DQ'd"
        else:
            t_phase_elapsed_sec = t_phase_elapsed / 1000.0
            formatted_run_time = "{:.3f}".format(t_phase_elapsed_sec)


        thumby.display.drawText("Run", 22, 0, 1)
        thumby.display.drawText(formatted_run_time, 10, 10, 1)
        thumby.display.drawText("Best",18, 20, 1)
        session_best_sec = session_best / 1000.0
        formatted_session_best = "{:.3f}".format(session_best_sec)
        thumby.display.drawText(formatted_session_best, 10, 30, 1)
        
        if thumby.buttonL.pressed():
            if t_phase_elapsed != 0 and session_best > t_phase_elapsed or session_best == 0:
                session_best = t_phase_elapsed
            reset_game()
    thumby.display.update()
    
    # TODO:
    # Create unique shift points (first is usually shorter, etc)
    # Have progress be based on "speed", which means missed shifts still allow progress but slower
    # Create two player
    # Create DRAMA Mode, with zoomed in and accurate recreation of staging
    ## Implement "stage" drifting
    # Fix centering on results based on time second digits
    # Implement option highlighting
