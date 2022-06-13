import streamlit as st
from PIL import Image
import cv2
from call_api import api_op
import base64
from io import BytesIO

RESIZE_AS=(512,512)

st.set_page_config(page_title="cloths_segmentation", page_icon="🤖")

st.title("Semantic_Segmentation_of_cloths")

chosen_option = st.sidebar.selectbox("Select Option", {"I want to upload an image"})
st.write('chosen option : ',chosen_option)

# if chosen_option == "Try out with inbuilt test images":
#     chosen_image = st.sidebar.selectbox("Select Image", {"2712.png", "2720.png", "2722.png", "2739.png", "2746.png", "2770.png", "2845.png", "2939.png", "2991.png"})
#     st.write('chosen image : ',chosen_image)

def main():
    if chosen_option == "I want to upload an image":
        upload_image()
    if chosen_option == "Try out with inbuilt test images":
        try_using_inbuilt_image()

def upload_image():
    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None: 
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image,caption='original (uploaded) image')
        buffered = BytesIO()
        uploaded_image.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue())
        return_api_op(encoded_string)
       
def try_using_inbuilt_image():
    path = "./" + chosen_image
    uploaded_image_bgr = cv2.imread(path)
    uploaded_image_rgb = cv2.cvtColor(uploaded_image_bgr, cv2.COLOR_BGR2RGB)  #since cv2 works with bgr, st.image works with rgb, PIL works with rgb
    st.image(uploaded_image_rgb, caption='uploaded_image')
    cv2.imwrite('ip_encode.png', uploaded_image_rgb)
    with open("ip_encode.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return_api_op(encoded_string)

def return_api_op(encoded_string):
    decoded_mask = api_op(encoded_string.decode('utf-8'))
    decoded_mask_ = base64.b64decode(decoded_mask.encode('utf-8'))
    with open('decoded_mask.png', 'wb') as f:
        f.write(decoded_mask_)
    final_mask = cv2.imread('decoded_mask.png')
    st.image(final_mask, caption="mask of uploaded_image")


if __name__ == "__main__":
    main()