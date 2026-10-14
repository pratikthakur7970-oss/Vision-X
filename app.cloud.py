import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoProcessorBase

 #vision_engine se apna frame-processing function import karo
#(naam tumhare code ke hisaab se badlega)
from vision_engine import process_frame

st.set_page_config(page_title="Vision X", layout="wide")
st.title("Vision X - AI Computer Vision")

RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

mode = st.sidebar.selectbox(
    "Mode", ["Driver Drowsiness", "Face Detection", "Hand Tracking"]
)

class Processor(VideoProcessorBase):
    def __init__(self):
        self.mode = "Driver Drowsiness"

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = process_frame(img, self.mode)   # yahan tumhara engine chalega
        return av.VideoFrame.from_ndarray(img, format="bgr24")

ctx = webrtc_streamer(
    key="vision-x",
    video_processor_factory=Processor,
    rtc_configuration=RTC_CONFIG,
    media_stream_constraints={"video": {"width": 640, "height": 480}, "audio": False},
    async_processing=True,
)

if ctx.video_processor:
    ctx.video_processor.mode = mode
