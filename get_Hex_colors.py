import math
from collections import Counter
from PIL import Image
import ntc
import color_list
import datetime
import os

def euclidean_distance(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)

def is_near_black(rgb, threshold):
    r, g, b = rgb
    return r <= threshold and g <= threshold and b <= threshold

def is_near_white(rgb, threshold):
    white_color = 255
    r, g, b = rgb
    return r>= white_color - threshold and g >= white_color - threshold and b >= white_color - threshold 

def get_frame_number(image_path):
    #Extract the frame number from the path
    filename = os.path.basename(image_path)
    return filename.split('.')[0].replace('frame', '').replace('_used', '')

def open_image(image_path):
    print("Inside open_image function")

    frame_number = get_frame_number(image_path)
    directory = os.path.dirname(image_path)

    primary_image_path = os.path.join(directory, f'frame{frame_number}.jpg')
    backup_image_path = os.path.join(directory, f'frame{frame_number}_used.jpg')

    #Check if file is available, if not, check with alternate 'used' filename
    if os.path.exists(primary_image_path):
        print("Opening primary image path")
        img = Image.open(primary_image_path)
    elif os.path.exists(backup_image_path):
        print("Opening backup image path")
        img = Image.open(backup_image_path)
    elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.png'):
        print("Image path ends with .jpg or .png, returning the path")
        img = Image.open(image_path)
    else:
        raise FileNotFoundError(f"Neither {primary_image_path} nor {backup_image_path} exists.")
    
    return img

def get_top_colors(image_path, num_of_colors=5):

    black_threshold = 50
    white_threshold = 50

    try:

        img = open_image(image_path)

        #Ensure consistent color representation by converting to RGB
        img = img.convert("RGB")

        # Resize the image for faster processing
        #Faster if resized, more precise if not
        #img = img.resize((100, 100))  # Resize to 100x100 pixels

        #Get all pixels colors
        pixels = list(img.getdata())

        #Filter the colors near black and white
        filtered_pixels = [pixel for pixel in pixels
                           if not is_near_white(pixel, white_threshold) and not is_near_black(pixel, black_threshold)]

        if not filtered_pixels:
            print("No valid pixels after filtering!")
            return []

        #Count the colors
        color_counts = Counter(filtered_pixels)
        common_colors = color_counts.most_common()
        selected_colors = [common_colors[0][0]] #Init with the most common colors

        #Greedy Selection for Maximum Diversity: Starting with the most common color,
        #the script iteratively selects the color that is furthest from any of the previously selected ones. 
        #This helps to ensure that the final colors are as diverse as possible.

        # Greedily select the next color that is furthest from the already selected ones
        for _ in range(1, num_of_colors):
            max_distance = -1
            next_color = None

            for color, _ in common_colors:
                if color not in selected_colors:
                    #Find the color that is furthest from any of the selected colors
                    min_distance = min(euclidean_distance(color, selected) for selected in selected_colors)

                    if min_distance > max_distance:
                        max_distance = min_distance
                        next_color = color

            if next_color:
                selected_colors.append(next_color)

        #Convert RGB to Hex
        top_color_hex = [(f"#{r:02x}{g:02x}{b:02x}", color_counts[(r, g, b)]) for(r, g, b) in selected_colors]

        #Sort final output by frequency (most common first)
        top_color_hex.sort(key=lambda x: x[1], reverse=True)

        return top_color_hex
    
    except Exception as e:
        print(f"Error: {e}")
        return []


#Begin Script

start_time = datetime.datetime.now()

ntc = ntc.NTC(color_list.ntc_names)

#input image path
image_path = input("Enter the path of the image: ").strip()

#Get the top 5 colors
top_colors = get_top_colors(image_path, num_of_colors=5)


if top_colors:
    print("\nTop 5 Colors (sorted by frequency)")
    for i, (hex_color, count) in enumerate(top_colors, 1):
        color_name = ntc.name(hex_color)

        print(f"{i}. {hex_color}: {color_name[1]} ({count} times)")


else:
    print("No colors could be extracted. Please check the image path or file format")

end_time = datetime.datetime.now()
diff_time = end_time - start_time

print(f"executed in {diff_time.total_seconds()} seconds or {diff_time.total_seconds()*1000} millseconds")