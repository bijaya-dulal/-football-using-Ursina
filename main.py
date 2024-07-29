from ursina import *

app = Ursina()

# Setup the playing field
ground = Entity(model='plane', scale=(10, 0.1, 20), texture='white_cube', texture_scale=(10, 20), color=color.green)

# Setup the goals
goal1 = Entity(model='cube', scale=(3, 2, 0.5), position=(0, 1, -9.5), color=color.red)
goal2 = Entity(model='cube', scale=(3, 2, 0.5), position=(0, 1, 9.5), color=color.blue)

# Setup the players
player1 = Entity(model='cube', scale=(1, 1, 1), position=(-2, 1, 0), color=color.red)
player2 = Entity(model='cube', scale=(1, 1, 1), position=(2, 1, 0), color=color.blue)

# Setup the football
ball = Entity(model='sphere', scale=(0.5, 0.5, 0.5), position=(0, 0.26, 0), color=color.white)
ball_speed = Vec3(0, 0, 0)

# Player speed
player_speed = 5

# Ball speed and friction
ball_friction = 0.98
ball_max_speed = 10

# Create stadium walls with textures
stadium_walls = [
    Entity(model='quad', scale=(30, 10), position=(0, 5, 15), texture='brick', color=color.white, rotation_y=180),  # Front wall
    Entity(model='quad', scale=(40, 10), position=(-15, 5, 0), texture='brick', color=color.white, rotation_y=90),  # Left wall
    Entity(model='quad', scale=(40, 10), position=(15, 5, 0), texture='brick', color=color.white, rotation_y=-90)   # Right wall
]

def update():
    global ball_speed

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

    # Check if the ball is in goal1 or goal2
    if ball.intersects(goal1).hit:
        print("Player 2 scores!")
        ball.position = (0, 0.26, 0)
        ball_speed = Vec3(0, 0, 0)
    if ball.intersects(goal2).hit:
        print("Player 1 scores!")
        ball.position = (0, 0.26, 0)
        ball_speed = Vec3(0, 0, 0)

    # Debugging output to check positions and ball speed
    print(f"Player 1 Position: {player1.position}")
    print(f"Player 2 Position: {player2.position}")
    print(f"Ball Position: {ball.position}")
    print(f"Ball Speed: {ball_speed}")

# Camera setup
camera.position = (0, 15, -30)
camera.rotation_x = 30

app.run()
