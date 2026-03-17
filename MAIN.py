import streamlit as st
from image_utils import enhance_image
from video_utils import enhance_frame

import cv2
import numpy as np
from PIL import Image
import tempfile
import time
import io
import os
from moviepy import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(page_title="Forge Studio", layout="wide")

# ---------------------------------
# UI Styling (Adobe-like)
# ---------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #000000, #001f3f);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #0a0a0a;
}

h1, h2, h3 {
    color:#00ffd5;
}

.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #0099ff);
    color:black;
    font-weight:bold;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("🔥 Forge Studio")

tool = st.sidebar.radio(
    "Choose Tool",
    ["Home", "Image Enhancer", "Video Enhancer"]
)

# ---------------------------------
# HOME
# ---------------------------------

if tool == "Home":

    st.title("🚀 Welcome to Forge Studio")

    st.markdown("""
    ### Your Creative AI Toolkit

    🖼️ Image Enhancer → Upscale & improve images  
    🎬 Video Enhancer → Enhance video quality  

    ⚡ Built for creators  
    🔥 Powered by Forge Studio  
    """)

    st.warning("⚠️ Use medium images and short videos (5–10 sec) for best performance")

# ---------------------------------
# IMAGE ENHANCER
# ---------------------------------

elif tool == "Image Enhancer":

    st.title("🖼️ Forge Image Enhancer")

    uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if uploaded_image:

        image = Image.open(uploaded_image).convert("RGB")

        st.image(image, caption="Original Image", width='stretch')

        quality = st.selectbox("Enhancement Level", ["2X", "4X"])

        if st.button("Enhance Image"):

            scale = 2 if quality == "2X" else 4

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            enhanced = enhance_image(image, scale)

            st.success("🔥 Enhancement Complete!")

            st.image(enhanced, caption="Enhanced Image", width='stretch')

            # Download
            result = Image.fromarray(enhanced)
            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                label="⬇ Download Image",
                data=buf.getvalue(),
                file_name="forge_image.png",
                mime="image/png"
            )

# ---------------------------------
# VIDEO ENHANCER
# ---------------------------------

elif tool == "Video Enhancer":

    st.title("🎬 Forge Video Enhancer")

    uploaded_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"])

    if uploaded_file:

        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_input.write(uploaded_file.read())
        temp_input.close()

        st.video(uploaded_file)

        quality = st.selectbox("Quality", ["HD", "2K", "4K"])

        if st.button("Enhance Video"):

            st.warning("⚠️ Use short clips (5–10 sec) for best performance")
            st.info("Processing...")

            clip = VideoFileClip(temp_input.name)

            scale = 1.3 if quality == "HD" else 1.6 if quality == "2K" else 2

            frames = []
            progress = st.progress(0)

            total = int(clip.fps * clip.duration)
            count = 0

            for frame in clip.iter_frames():

                frame = enhance_frame(frame, scale)
                frames.append(frame)

                count += 1
                progress.progress(min(count / total, 1.0))

            enhanced_clip = ImageSequenceClip(frames, fps=clip.fps)

            final_clip = enhanced_clip.with_audio(clip.audio)

            output_path = "final_output.mp4"

            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            st.success("🔥 Enhancement Complete!")

            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇ Download Video",
                    data=f,
                    file_name="forge_video.mp4",
                    mime="video/mp4"
                )
