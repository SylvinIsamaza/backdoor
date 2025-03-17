# CarMovementGame - Educational Backdoor Example

This project demonstrates a simple car movement game built with Pygame, which also includes educational examples of how a backdoor might be implemented. It is designed for educational purposes only to illustrate potential security risks.

**Disclaimer:** This game includes features that simulate backdoor-like behavior, such as logging commands and adding persistence. Use responsibly and only in a safe, controlled environment.

**Ethical and Legal Disclaimer**


- **Educational Context**: The implementation below is provided solely for educational purposes to demonstrate how a backdoor might work. It must be tested in a controlled, isolated environment (e.g., virtual machines on a private network) with explicit consent from all parties involved. Using this code on real systems, public networks, or systems you do not own or have permission to test is illegal and unethical.

- **Responsibility:** You are responsible for ensuring that this code is used legally and ethically. Misusing it for malicious purposes is a violation of laws (the Cybercrime Act in Rwanda, or equivalent laws in other jurisdictions) and could result in severe legal consequences.

## Features

-   **Car Movement Game:** A simple game where you can control a car using the arrow keys or WASD keys.
-   **Dependency Check:** Checks for required dependencies (Pygame) and attempts to install them.
-   **Simulated Shell Access:** Logs simulated shell commands to a file (`shell_log.txt`).
-   **Persistence:** Adds the game to the system's startup to run on boot (for educational demonstration).
-   **Cleanup Script:** Includes a script (`cleanup.py`) to remove the added persistence and logs.

## Usage Development
## Make sure the listener is in listening mode
#### Linux
```bash
nc -lvp 4444
```

#### Windows
```bash
ncat -lvp 4444
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```
1. **Run the game:**

    ```bash
    python game.py
    ```
2.  **Consent:** The game will ask for your consent before proceeding with any simulated backdoor activities.

3.  **Play the game:** Control the car using the arrow keys or WASD keys.

4.  **Cleanup:** To remove the persistence and logs, run the cleanup script:

    ```bash
    python cleanup.py
    ```

## Files

-   `game.py`: The main game file containing the game logic and simulated backdoor features.
-   `cleanup.py`: A script to remove persistence and logs created by the game.


## Simulated Backdoor Details

-   **Logging:** The game logs simulated shell commands to `shell_log.txt`. This is to demonstrate how a backdoor might record user activity.
-   **Persistence:** The game adds itself to the system's startup. This is to demonstrate how a backdoor might ensure it runs every time the system starts.

## Important

-   This project is for educational purposes only.
-   Do not use this code in a real-world environment without proper authorization.
-   Be aware of the potential security risks associated with backdoors.
-   Always practice responsible and ethical behavior when dealing with security-related code.


