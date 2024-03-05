import cv2
import numpy as np
import pyautogui
import time

def find_image_on_screen(target_image_path, timeout=10):
    start_time = time.time()

    # Load the target image
    target_image = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
    if target_image is None:
        raise ValueError(f"Image not found or unable to read: {target_image_path}")

    # Handle images with an alpha channel (transparency)
    if target_image.shape[-1] == 4:
        # Convert to grayscale while preserving alpha channel
        target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2GRAY)
    else:
        # Convert to grayscale
        target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    while True:
        # Check for timeout
        if time.time() - start_time > timeout:
            raise TimeoutError("Timeout reached while searching for the image on screen.")

        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # Template matching to find the image
        result = cv2.matchTemplate(screen, target_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Threshold for detection
        if max_val > 0.8:  # Adjust this threshold as needed
            return max_loc, target_image.shape

def move_mouse_and_click(position, target_image_shape, duration=1.0):
    # Calculate the center of the target image
    center_x = position[0] + target_image_shape[1] // 2
    center_y = position[1] + target_image_shape[0] // 2

    # Move the mouse to the center of the target image
    pyautogui.moveTo(center_x, center_y, duration=duration)
    time.sleep(0.5)

    # Click the mouse
    pyautogui.click()

def find_and_get_coords(target_image_path, timeout=10):
    try:
        position, target_image_shape = find_image_on_screen(target_image_path, timeout)
        return position
    except TimeoutError as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def find_and_click_image(target_image_path, timeout=10):
    try:
        position, target_image_shape = find_image_on_screen(target_image_path, timeout)
        move_mouse_and_click(position, target_image_shape)
    except TimeoutError as e:
        print(f"Timeout error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

# Example usage
# find_and_click_image('path_to_your_image.png')
