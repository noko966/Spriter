from PIL import Image
import cssutils
import os

# Directory containing images
image_dir = './images'
sprite_dir = './Input/spriteTournament1.png'
css_file_dir = './Input/spriteTournament.css'
output_dir = './Output/spriteTournament.png'



# Open the existing sprite
sprite = Image.open(sprite_dir)

# Get list of image files
image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

# Open images and store them in a list'
desired_size = (48, 48)

images = []
for f in image_files:
    img = Image.open(os.path.join(image_dir, f))
    bbox = img.getbbox()
    cropped_img = img.crop(bbox)
    max_dim = max(cropped_img.size)
    square_img = Image.new('RGBA', (max_dim, max_dim))
    paste_position = ((max_dim - cropped_img.width) // 2,
                      (max_dim - cropped_img.height) // 2)
    
    # paste the cropped image onto the square image
    square_img.paste(cropped_img, paste_position)
    resized_img = square_img.resize(desired_size)
    images.append(resized_img)
# Create a dictionary to hold file names and images

# Crop the image to the contents of the bounding box
images_dict = {f: img.resize((48, 48)) for f, img in zip(image_files, images)}

# Calculate new height and width for the sprite
new_height = sprite.height + 48 * len(images_dict)
new_width = max(sprite.width, 48*3)  # 3 images in a row

# Create a new image with the new dimensions
combined = Image.new('RGBA', (new_width, new_height))

# Paste the existing sprite and the new images into the combined image
combined.paste(sprite, (0, 0))

# Create a new CSS stylesheet
stylesheet = cssutils.css.CSSStyleSheet()

for i, (filename, img) in enumerate(images_dict.items()):
    for j in range(4):  # paste the same image 3 times side by side
        x = j*desired_size[0]
        y = sprite.height + i * desired_size[1]
        combined.paste(img, (x, y))

    x = 0
    rule = cssutils.css.CSSStyleRule()
    # rule.selectorText = f".{os.path.splitext(filename)[0]}:before"
    # rule.style.backgroundPosition = f"{x}px {-y}px"
    # stylesheet.add(rule)
    print(f"{os.path.splitext(filename)[0]}")
    # rule.selectorText = "os.path.splitext(filename)[0]"
    rule.selectorText = f".sport_tournament{os.path.splitext(filename)[0]}:before"  # Class selector is the filename without extension
    rule.style.backgroundPosition = f"{x}px {-y / 2}px"

        # Add the rule to the stylesheet
    stylesheet.add(rule)

# Save the sprite
combined.save(output_dir)

# Write the CSS to a file
with open(css_file_dir, 'a') as css_file:
    css_file.write(stylesheet.cssText.decode())


