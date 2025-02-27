from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.translation import gettext_lazy as _


def process_image(image, size, crop=True, quality=85, format="JPEG"):
    """
    Process an uploaded image:
    1. Resize to target size
    2. Crop to maintain aspect ratio if needed
    3. Convert to JPEG format
    4. Optimize file size

    Args:
        image: ImageField instance
        size: tuple of (width, height)
        crop: boolean to determine if image should be cropped
        quality: JPEG quality (1-100)
        format: output format (default JPEG)

    Returns:
        Django File object with processed image
    """
    if not image:
        return None

    # Open image
    img = Image.open(image)

    # Convert to RGB if necessary
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Get current dimensions
    src_width, src_height = img.size
    dst_width, dst_height = size

    # Calculate dimensions
    if crop:
        # Calculate dimensions to maintain aspect ratio
        src_ratio = float(src_width) / float(src_height)
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio > src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 2

        # Crop image
        img = img.crop(
            (x_offset, y_offset, x_offset + crop_width, y_offset + crop_height)
        )

    # Resize image
    img = img.resize(size, Image.Resampling.LANCZOS)

    # Save image to memory
    output = BytesIO()
    img.save(output, format=format, quality=quality, optimize=True)
    output.seek(0)

    # Create new filename
    if image.name:
        name = f"{image.name.split('.')[0]}.jpg"
    else:
        name = "image.jpg"

    # Return a Django-friendly file object
    return File(output, name=name)


def process_book_cover(image):
    """Process book cover images to a standard size."""
    return process_image(image, size=(800, 1200), crop=True)


def process_author_photo(image):
    """Process author photos to a standard square size."""
    return process_image(image, size=(400, 400), crop=True)


def process_user_avatar(image):
    """Process user avatar to a small square size."""
    return process_image(image, size=(200, 200), crop=True)
