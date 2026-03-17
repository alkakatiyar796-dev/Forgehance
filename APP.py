import streamlit as st
import cv2
import tempfile
from moviepy import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import numpy as np
import os

# ---------------------------------
# Page Settings
# ---------------------------------

st.set_page_config(page_title="FORGEHANCE PROTOTYPE", layout="centered")

# ---------------------------------
# UI Styling
# ---------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #000000, #001f3f);
    color: white;
}
h1 {
    text-align:center;
    color:#00ffd5;
}
.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #0099ff);
    color:black;
    font-weight:bold;
    border-radius:10px;
}
video {
    border-radius: 10px;
    border: 2px solid #00ffd5;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ FORGEHANCE (FAST AI PROTOTYPE)")

uploaded_file = st.file_uploader("Upload Video", type=["mp4","mov","avi"])

# ---------------------------------
# Enhancement Function
# ---------------------------------

def enhance_frame(frame, scale):
    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    frame = cv2.filter2D(frame, -1, kernel)

    frame = cv2.convertScaleAbs(frame, alpha=1.15, beta=10)

    return frame

# ---------------------------------
# Main Logic
# ---------------------------------

if uploaded_file:

    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_input.write(uploaded_file.read())
    temp_input.close()

    st.video(uploaded_file)

    quality = st.selectbox("Select Quality", ["HD (Fast)", "2K (Balanced)", "4K (Slow)"])

    if st.button("Enhance Video"):

        st.info("Enhancing...")

        clip = VideoFileClip(temp_input.name)

        total_frames = int(clip.fps * clip.duration)
        progress = st.progress(0)

        first_frame = next(clip.iter_frames())
        h, w, _ = first_frame.shape

        # scale selection
        if quality == "HD (Fast)":
            scale = 1.3
        elif quality == "2K (Balanced)":
            scale = 1.6
        else:
            scale = 2

        frames = []
        frame_count = 0

        # ---------------------------------
        # Frame Processing
        # ---------------------------------

        for frame in clip.iter_frames():

            if frame is None:
                continue

            frame = enhance_frame(frame, scale)
            frames.append(frame)

            frame_count += 1
            progress.progress(min(frame_count / total_frames, 1.0))

        # ---------------------------------
        # Create Video (FIXED METHOD)
        # ---------------------------------

        enhanced_clip = ImageSequenceClip(frames, fps=clip.fps)

        final_video = os.path.abspath("final_output.mp4")

        final_clip = enhanced_clip.with_audio(clip.audio)

        final_clip.write_videofile(
            final_video,
            codec="libx264",
            audio_codec="aac"
        )

        # ---------------------------------
        # Output
        # ---------------------------------

        if os.path.exists(final_video):

            st.success("🔥 Enhancement Complete!")

            st.video(final_video)

            with open(final_video, "rb") as f:
                st.download_button(
                    "⬇ Download Video",
                    f,
                    "forgehance_output.mp4"
                )
        else:
            st.error("❌ Final video failed.")