import streamlit as st
from io import BytesIO
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import os

class ImageUtil:
    def __init__(self, image) -> None:
        self.image = image

    def open(self):
        st.image(self.image, caption='Uploaded Image', use_column_width=True)

    def crop(self, val):
        try:
            x, y = val.split(',')
            size = (int(x), int(y))
            self.image.thumbnail(size)
        except ValueError:
            pass

    def rotate(self, val):
        try:
            angle = int(val)
            self.image = self.image.rotate(angle)
        except ValueError:
            pass

    def blur(self, val):
        try:
            radius = int(val)
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        except ValueError:
            pass

    def adjust_brightness(self, val):
        try:
            brightness_factor = float(val)
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(brightness_factor)
        except ValueError:
            pass

    def adjust_sharpness(self, val):
        try:
            sharpness_factor = float(val)
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(sharpness_factor)
        except ValueError:
            pass

    def adjust_color(self, val):
        try:
            color_factor = float(val)
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(color_factor)
        except ValueError:
            pass

    def adjust_contrast(self, val):
        try:
            contrast_factor = float(val)
            mod = ImageEnhance.Contrast(self.image)
            self.image = mod.enhance(contrast_factor)
        except ValueError:
            pass


def main():
    st.title("Image Editor")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        edit_image = ImageUtil(image)

        st.subheader("Original Image")
        edit_image.open()

        st.subheader("Edit Options")
        selected_options = []

        if st.checkbox("Resize/Crop"):
            selected_options.append("crop")

        if st.checkbox("Adjust Brightness"):
            selected_options.append("adjust_brightness")

        if st.checkbox("Adjust Sharpness"):
            selected_options.append("adjust_sharpness")

        if st.checkbox("Adjust Color"):
            selected_options.append("adjust_color")

        if st.checkbox("Adjust Contrast"):
            selected_options.append("adjust_contrast")

        if st.checkbox("Adjust Rotation"):
            selected_options.append("rotate")

        if st.checkbox("Blur"):
            selected_options.append("blur")

        if selected_options:
            for option in selected_options:
                value = None
                if option == "crop":
                    value = st.text_input(f"Enter size (X,Y) for {option.replace('_', ' ')}:")
                elif option == "rotate":
                    value = st.slider(f"Enter angle for {option.replace('_', ' ')}", -180, 180, 0)
                elif option == "blur":
                    value = st.slider(f"Enter radius for {option.replace('_', ' ')}", 0, 10, 0)
                else:
                    value = st.slider(f"Enter value for {option.replace('_', ' ')}", 0.0, 2.0, 1.0)

                getattr(edit_image, option)(value)

            if st.button("Apply"):
                st.subheader("Edited Image")
                st.image(edit_image.image, caption='Edited Image', use_column_width=True)
                download_button(edit_image.image)

def download_button(edited_image):
    buffer = BytesIO()
    edited_image.save(buffer, format="PNG")
    buffer.seek(0)
    st.download_button(
        label="Download Edited Image",
        data=buffer,
        file_name="edited_image.png",
        mime="image/png",
    )

if __name__ == "__main__":
    main()
