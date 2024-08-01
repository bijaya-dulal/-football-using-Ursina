from ursina import *

app = Ursina()

# Setup the playing field
ground = Entity(model='plane', scale=(15, 0.1, 20), color=color.rgb(34, 255, 34))

# Setup for goal post
goal1 = Entity(model='cube', scale=(3, 2, 0.5), position=(0, 1, -9.5), color=color.rgba(255, 0, 0, 100), collider='box')
goal2 = Entity(model='cube', scale=(3, 2, 0.5), position=(0, 1, 9.5), color=color.rgba(0, 0, 255, 100), collider='box')

# Setup the players
player1 = Entity(model='cube', scale=(1, 1, 1), position=(-2, 1, -1), color=color.rgba(255, 0, 0, 100), collider='box')
player2 = Entity(model='cube', scale=(1, 1, 1), position=(2, 1, 2), color=color.rgba(0, 0, 255, 100), collider='box')

# Setup the football
ball = Entity(model='sphere', scale=(0.5, 0.5, 0.5), position=(0, 0.26, 0), color=color.white, collider='sphere')
ball_speed = Vec3(0, 0, 0)

# Add stands
stand2 = Entity(model='cube', scale=(16, 3, 2), position=(0, 2.5, 11), color=color.gray) # back
stand3 = Entity(model='cube', scale=(2, 3, 20), position=(-9, 2.5, 0), color=color.gray) # left
stand4 = Entity(model='cube', scale=(2, 3, 20), position=(9, 2.5, 0), color=color.gray) # right

# Player speed
player_speed = 2

# Ball speed and friction
ball_friction = 0.98
ball_max_speed = 4

# Scoreboard
player1_score = 0
player2_score = 0
scoreboard = Text(text=f"P1: {player1_score} - P2: {player2_score}", position=(-0.85, 0.45), scale=2, color=color.white)

def reset_ball():
    ball.position = Vec3(0, 0.26, 0)
    ball_speed = Vec3(0, 0, 0)

def update_scoreboard():
    scoreboard.text = f"P1 : {player1_score} - P2: {player2_score}"

def update():
    global ball_speed, player1_score, player2_score

    # Player 1 controls (WASD)
    if held_keys['w']:
        player1.z -= time.dt * player_speed
    if held_keys['s']:
        player1.z += time.dt * player_speed
    if held_keys['a']:
        player1.x -= time.dt * player_speed
    if held_keys['d']:
        player1.x += time.dt * player_speed

    # Player 2 controls (Arrow keys)
    if held_keys['up arrow']:
        player2.z -= time.dt * player_speed
    if held_keys['down arrow']:
        player2.z += time.dt * player_speed
    if held_keys['left arrow']:
        player2.x -= time.dt * player_speed
    if held_keys['right arrow']:
        player2.x += time.dt * player_speed

    # Restrict players to stay within the stands
    player1.x = clamp(player1.x, -8,8)
    player1.z = clamp(player1.z, -10, 10)
    player2.x = clamp(player2.x, -8,8)
    player2.z = clamp(player2.z, -10, 10)

    # Check collision between players and ball
    if player1.intersects(ball).hit:
        print("Player 1 hit the ball")
        direction = (ball.position - player1.position).normalized()
        ball_speed = direction * ball_max_speed
        print(f"Player 1 hits ball in direction: {direction}, Ball speed: {ball_speed}")

    if player2.intersects(ball).hit:
        print("Player 2 hit the ball")
        direction = (ball.position - player2.position).normalized()
        ball_speed = direction * ball_max_speed
        print(f"Player 2 hits ball in direction: {direction}, Ball speed: {ball_speed}")

    # Apply ball speed and friction
    ball.position += ball_speed * time.dt
    ball_speed *= ball_friction

    # Restrict the ball from going below the ground
    if ball.position.y < 0.26:
        ball.position = Vec3(ball.position.x, 0.26, ball.position.z)

    # Check if the ball is in goal1 or goal2
    if ball.intersects(goal1).hit:
        print("Player 2 scores!")
        player2_score += 1
        update_scoreboard()
        reset_ball()
        player1.position = Vec3(-2, 1, 0)
        player2.position = Vec3(2, 1, 0)
        ball.color = color.white  # Reset ball color after goal

    if ball.intersects(goal2).hit:
        print("Player 1 scores!")
        player1_score += 1
        update_scoreboard()
        reset_ball()
        player1.position = Vec3(-2, 1, 0)
        player2.position = Vec3(2, 1, 0)
        ball.color = color.white  # Reset ball color after goal

    # Reset ball if it goes out of bounds
    if abs(ball.position.x) > 7.5 or abs(ball.position.z) > 10:
        print("Ball went out of bounds! Resetting...")
        reset_ball()

# Camera setup
camera.position = (0, 15, -30)
camera.rotation_x = 28

app.run()
