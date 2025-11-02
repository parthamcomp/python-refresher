import pygame
import random
import math
import sys,os

pygame.init()

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # temporary folder for bundled files
else:
    base_path = os.path.dirname(__file__)

# --- Screen Setup ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Rock Paper Scissors")

# --- Fonts ---
FONT_NAME = os.path.join(base_path, "assets", "fonts", "Satoshi-Variable.ttf")
font = pygame.font.Font(FONT_NAME, 100)
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 120)
emoji_font_small = pygame.font.SysFont("Segoe UI Emoji", 60)  # smaller emoji font for top-right quit

# --- Game Variables ---
choices = ["rock", "paper", "scissors"]
emojis = {"rock": "✊", "paper": "🫳", "scissors": "✌️"}
player_choice = None
computer_choice = None
result_text = ""
result_color = (255, 255, 255)
fade_alpha = 0

# Default background: purple
bg_color = [90, 0, 150]        # starting purple tone
target_color = [90, 0, 150]
clock = pygame.time.Clock()
running = True

# --- Score Tracking ---
rounds = 0
max_rounds = 5
player_score = 0
cpu_score = 0
ties = 0
game_over = False

# --- Animation States ---
pop_scale = 0
pop_active = False
transitioning = False
transition_alpha = 0

# --- Quit Button ---
quit_emoji = "❌"
quit_surface_small = emoji_font_small.render(quit_emoji, True, (255, 255, 255))
quit_rect_small = quit_surface_small.get_rect(topright=(WIDTH - 30, 20))


# --- Functions ---------------------------------------------------------

def get_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "win"
    else:
        return "lose"


def draw_text_center(text, y, color, alpha=255, size=None):
    """Draw text centered horizontally"""
    fnt = font if size is None else pygame.font.Font(FONT_NAME, size)
    surface = fnt.render(text, True, color)
    surface.set_alpha(alpha)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_text_with_emoji(label, emoji, y, label_color=(255, 255, 255)):
    """Draw a label and emoji side by side"""
    label_surface = font.render(label, True, label_color)
    emoji_surface = emoji_font.render(emoji, True, (255, 255, 255))
    spacing = 60
    total_width = label_surface.get_width() + emoji_surface.get_width() + spacing
    start_x = (WIDTH - total_width) // 2
    label_rect = label_surface.get_rect(topleft=(start_x, y))
    emoji_rect = emoji_surface.get_rect(midleft=(label_rect.right + spacing, label_rect.centery))

    # Pop animation
    if pop_active:
        scaled_size = (
            int(emoji_surface.get_width() * pop_scale),
            int(emoji_surface.get_height() * pop_scale)
        )
        emoji_surface = pygame.transform.smoothscale(emoji_surface, scaled_size)
        emoji_rect = emoji_surface.get_rect(midleft=(label_rect.right + spacing, label_rect.centery))

    screen.blit(label_surface, label_rect)
    screen.blit(emoji_surface, emoji_rect)


def draw_choices():
    """Draw bottom emoji choices"""
    x_positions = [WIDTH // 4, WIDTH // 2, 3 * WIDTH // 4]
    for i, choice in enumerate(choices):
        emoji = emojis[choice]
        text_surface = emoji_font.render(emoji, True, (255, 255, 255))
        rect = text_surface.get_rect(center=(x_positions[i], HEIGHT - 100))
        screen.blit(text_surface, rect)


def lerp_color(current, target, speed=0.1):
    """Smoothly transition between colors"""
    for i in range(3):
        current[i] += (target[i] - current[i]) * speed
    return current


def animate_pop():
    """Handle emoji pop-in animation"""
    global pop_scale, pop_active
    if pop_active:
        pop_scale += 0.2
        if pop_scale >= 1.0:
            pop_scale = 1.0
            pop_active = False


def draw_quit_button():
    """Always show small quit emoji top-right"""
    screen.blit(quit_surface_small, quit_rect_small)


def fade_transition(next_screen_callback):
    """Smooth fade-out and fade-in transition"""
    global transition_alpha, transitioning
    transitioning = True
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((90, 0, 150))

    # Fade out
    for alpha in range(0, 256, 10):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

    next_screen_callback()

    # Fade in
    for alpha in range(255, -1, -10):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

    transitioning = False


def draw_game_over_screen():
    """Display scores after 5 rounds"""
    screen.fill((90, 0, 150))
    draw_text_center("Game Over", HEIGHT // 4, (255, 255, 255))

    summary = [
        f"You: {player_score}",
        f"Computer: {cpu_score}",
        f"Ties: {ties}",
    ]
    y = HEIGHT // 2 - 100
    for line in summary:
        draw_text_center(line, y, (200, 200, 200), 255, size=60)
        y += 80

    restart_emoji = "🔁"
    restart_surface = emoji_font.render(restart_emoji, True, (0, 255, 0))
    restart_rect = restart_surface.get_rect(center=(WIDTH // 2 - 100, HEIGHT - 150))

    quit_surface_big = emoji_font.render("❌", True, (255, 0, 0))
    quit_rect_big = quit_surface_big.get_rect(center=(WIDTH // 2 + 100, HEIGHT - 150))

    screen.blit(restart_surface, restart_rect)
    screen.blit(quit_surface_big, quit_rect_big)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_rect.collidepoint(x, y):
                    fade_transition(reset_game)
                    waiting = False
                elif quit_rect_big.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()


def reset_game():
    """Restart all variables"""
    global rounds, player_score, cpu_score, ties, player_choice, computer_choice, game_over, bg_color, target_color
    rounds = 0
    player_score = 0
    cpu_score = 0
    ties = 0
    player_choice = None
    computer_choice = None
    game_over = False
    bg_color = [90, 0, 150]      # reset to purple
    target_color = [90, 0, 150]


# --- Main Loop ---------------------------------------------------------

while running:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Quit button
            if quit_rect_small.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

            # Gameplay buttons
            if not game_over and event.pos[1] > HEIGHT - 150:
                idx = event.pos[0] // (WIDTH // 3)
                player_choice = choices[idx]
                computer_choice = random.choice(choices)
                result = get_winner(player_choice, computer_choice)
                fade_alpha = 0
                pop_scale = 0.3
                pop_active = True
                rounds += 1

                if result == "win":
                    result_text = "You Win!"
                    result_color = (0, 255, 0)
                    target_color = [0, 120, 0]
                    player_score += 1
                elif result == "lose":
                    result_text = "You Lose!"
                    result_color = (255, 0, 0)
                    target_color = [120, 0, 0]
                    cpu_score += 1
                else:
                    result_text = "It's a Tie!"
                    result_color = (255, 215, 0)
                    target_color = [150, 100, 0]
                    ties += 1

                if rounds >= max_rounds:
                    game_over = True

    # Background and animations
    bg_color = lerp_color(bg_color, target_color)
    animate_pop()

    # Idle "Make your move" with stronger pulse
    if not player_choice and not computer_choice and not game_over:
        t = pygame.time.get_ticks() / 1000
        pulse = (math.sin(t * 2) + 1) / 2
        alpha = 100 + int(155 * pulse)
        size = 90 + int(20 * pulse)
        color = (255, int(100 + 155 * pulse), 255)  # shifting magenta-pink glow
        draw_text_center("Make your move", HEIGHT // 2 - 150, color, alpha, size=size)

    # Results display
    if player_choice and computer_choice and not game_over:
        draw_text_with_emoji("You:", emojis[player_choice], HEIGHT // 2 - 300)
        draw_text_with_emoji("Computer:", emojis[computer_choice], HEIGHT // 2 - 180)
        if fade_alpha < 255:
            fade_alpha += 5
        draw_text_center(result_text, HEIGHT // 2 + 120, result_color, fade_alpha)

    draw_choices()
    draw_quit_button()
    pygame.display.flip()
    clock.tick(60)

    if game_over and not transitioning:
        pygame.time.wait(800)
        fade_transition(draw_game_over_screen)

pygame.quit()
sys.exit()
