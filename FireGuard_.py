import cv2
import numpy as np
import board
import busio
import adafruit_mlx90640
import time
import os
from telegram import Bot

# Telegram bot settings
bot_token = 'write the token of the person you want to contact'
chat_id = 'write the chat id of the same person, it will be unique for one account in telegram'
bot = Bot(token=bot_token)

# Setup MLX90640
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ  # Adjust as needed

def get_thermal_image():
    frame = np.zeros((24 * 32,))
    try:
        mlx.getFrame(frame)
        data_array = np.reshape(frame, (24, 32))
        return data_array
    except Exception as e:
        print(f"An error occurred while getting the frame: {e}")
        return np.zeros((24, 32))  # Return an empty array on error

def process_image(data_array):
    # Normalize data_array to 0-255 for image processing
    min_val, max_val = np.min(data_array), np.max(data_array)
    image = (data_array - min_val) / (max_val - min_val) * 255
    image = np.uint8(image)
    image = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    
    # Resize the image to a higher resolution for better clarity
    image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)
    
    # Apply Gaussian Blur to smooth the image
    image = cv2.GaussianBlur(image, (5, 5), 0)

    return image, max_val

def add_temperature_text(image, max_temp):
    # Add maximum temperature text to the image
    text = f"Current Max Temp: {max_temp:.1f} Celsius"
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10, 450)  # Position of the text on the bottom of the image
    font_scale = 1
    color = (255, 255, 255)  # Red color in BGR
    thickness = 2

    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    return image

def save_image(image, counter):
    # Set the path to save the images in the Pictures folder
    pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.exists(pictures_path):
        os.makedirs(pictures_path)
    filename = os.path.join(pictures_path, f"thermal_image_{counter}.jpg")
    cv2.imwrite(filename, image)
    return filename

def send_telegram_alert(message, image_path):
    # Send text message
    bot.send_message(chat_id=chat_id, text=message)
    
    # Send image if available
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)

def main():
    counter = 0  # Image counter to keep track of saved images
    num_images = 50  # Number of images to capture
    duration = 120  # Total duration in seconds
    interval = duration / num_images  # Time interval between each capture (in seconds)

    while counter < num_images:
        data_array = get_thermal_image()
        image, max_temp = process_image(data_array)
        image_with_temp = add_temperature_text(image, max_temp)  # Add temperature to the image
        
        # Save the image with the temperature text
        image_path = save_image(image_with_temp, counter)
        
        # Check temperature and send alert if needed
        if max_temp > 40:
            alert_message = f"Warning! High temperature detected: {max_temp:.1f}°C"
            send_telegram_alert(alert_message, image_path)
        
        counter += 1
        time.sleep(interval)  # Wait for the next capture

    print(f"Captured and saved {num_images} images in the Pictures folder.")

if __name__ == '__main__':
    main()
