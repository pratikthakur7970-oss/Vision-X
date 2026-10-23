import streamlit as st



from vision_engine import run_camera, MODULE_INFO, BrowserVisionProcessor

from streamlit_webrtc import webrtc_streamer, WebRtcMode



from pathlib import Path



from datetime import datetime





st.set_page_config(
    page_title="Vision X | AI Computer Vision Studio",
    page_icon="🧠",
    
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""



<style>



/* Keep the sidebar reopen control accessible. */
[data-testid="stToolbar"] {
    visibility: visible !important;
}

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 999999 !important;
}







/* Keep header available for reopening the sidebar */

[data-testid="stHeader"] {

    background: transparent !important;

}







/* Remove extra top space */



.block-container {



    padding-top: 1rem !important;



}



</style>



""", unsafe_allow_html=True)







st.markdown("""



<style>



@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');



:root { color-scheme: dark; }



.stApp {



  color:#f2f5ff; font-family:Inter,sans-serif;



  background:



    radial-gradient(ellipse at 10% 0%,rgba(0,199,255,.16),transparent 32%),



    radial-gradient(ellipse at 92% 4%,rgba(170,0,255,.18),transparent 30%),



    radial-gradient(ellipse at 60% 100%,rgba(255,0,170,.10),transparent 35%),



    #050713;



  background-size:180% 180%;



  animation: bgShift 14s ease-in-out infinite alternate;



}



[data-testid="stSidebar"] {



  background:linear-gradient(180deg,rgba(7,12,31,.98),rgba(10,7,27,.98));



  border-right:1px solid rgba(0,208,255,.45);



  box-shadow:5px 0 28px rgba(0,180,255,.08);



}



[data-testid="stSidebar"] > div {padding-top:1.15rem;}



.block-container {max-width:1550px;padding-top:1.45rem;padding-bottom:3rem;}



h1,h2,h3,h4 {font-family:Orbitron,Inter,sans-serif!important;color:#f5f7ff!important;letter-spacing:-.025em;}



p,label,.stMarkdown {color:#d3dcf5;}



.brand {display:flex;align-items:center;gap:12px;padding:7px 4px 18px;border-bottom:1px solid #25254d;margin-bottom:20px;}



.brand-mark {width:45px;height:45px;border-radius:14px;display:flex;align-items:center;justify-content:center;color:#07111c;font-size:24px;font-weight:900;background:linear-gradient(135deg,#00f5ff,#7c3cff,#ff37c7);background-size:220% 220%;animation:colorFlow 5s ease infinite;box-shadow:0 0 24px #00d9ff55;}



.brand-title {font:800 1.18rem Orbitron,sans-serif;color:#fff;text-shadow:0 0 15px #08dfff66;}



.brand-sub {font-size:.68rem;color:#a5b3df;margin-top:3px;}



.eyebrow {color:#4df6ff;text-transform:uppercase;font-size:.72rem;letter-spacing:.19em;font-weight:800;}



.hero {position:relative;overflow:hidden;border:1px solid transparent;border-radius:24px;padding:34px 36px;margin-bottom:24px;background:linear-gradient(115deg,rgba(19,12,58,.98),rgba(5,38,83,.96),rgba(48,8,73,.96)) padding-box,linear-gradient(110deg,#00eaff,#8b5cff,#ff31c8,#00eaff) border-box;background-size:100% 100%,300% 300%;animation:colorFlow 9s linear infinite,fadeUp .65s ease-out;box-shadow:0 0 35px rgba(0,170,255,.13),inset 0 0 30px rgba(88,56,255,.08);}



.hero:after {content:"";position:absolute;width:340px;height:340px;right:-90px;top:-160px;border-radius:50%;background:radial-gradient(circle,rgba(0,238,255,.25),rgba(160,30,255,.12) 45%,transparent 70%);pointer-events:none;animation:orb 7s ease-in-out infinite alternate;}



.hero h1 {font-size:clamp(2.5rem,5vw,4.1rem);line-height:1.03;margin:.45rem 0 .8rem;background:linear-gradient(90deg,#fff,#5ffbff,#c6a0ff,#ff8be6,#fff);background-size:250% auto;-webkit-background-clip:text;color:transparent!important;animation:textFlow 7s linear infinite;}



.hero p {max-width:700px;color:#d7e4ff;font-size:1.03rem;line-height:1.65;margin-bottom:0;}



.hero-chips {display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;}



.chip {font-size:.76rem;padding:7px 11px;border:1px solid #3d5aaf;border-radius:99px;background:rgba(11,27,67,.8);color:#d9faff;box-shadow:inset 0 0 12px #287aff12;transition:all .2s ease;}



.section-head {display:flex;align-items:end;justify-content:space-between;gap:12px;margin:26px 0 14px;}



.section-head h2 {margin:0;font-size:1.4rem;}



.section-sub,.small-muted {color:#9daed8;font-size:.84rem;line-height:1.55;}



.kpi {border:1px solid #30427f;border-radius:16px;padding:18px 19px;background:linear-gradient(145deg,rgba(17,25,65,.95),rgba(7,14,38,.98));min-height:112px;box-shadow:0 0 20px rgba(52,74,255,.08);transition:all .25s ease;position:relative;overflow:hidden;}



.kpi:after {content:"";position:absolute;inset:0;border-top:1px solid rgba(0,238,255,.35);pointer-events:none;}



.kpi-label {font-size:.73rem;color:#9db4e8;text-transform:uppercase;letter-spacing:.09em;font-weight:800;}



.kpi-value {font:800 1.75rem Orbitron,sans-serif;color:#fff;margin-top:9px;text-shadow:0 0 16px #4a8dff55;}



.kpi-note {font-size:.75rem;color:#58f5ff;margin-top:3px;}



.module-card {height:100%;min-height:174px;border:1px solid #384b94;border-radius:17px;padding:19px;background:linear-gradient(145deg,rgba(17,24,65,.98),rgba(8,13,35,.98));transition:transform .24s ease,border-color .24s ease,box-shadow .24s ease;box-shadow:0 8px 24px rgba(0,0,0,.18);position:relative;overflow:hidden;}



.module-card:before {content:"";position:absolute;inset:0;border-radius:17px;padding:1px;background:linear-gradient(135deg,rgba(0,238,255,.6),rgba(117,66,255,.2),rgba(255,49,200,.45));-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;}



.module-card:hover {transform:translateY(-4px);border-color:#44f7ff;box-shadow:0 0 24px rgba(0,215,255,.2),0 12px 32px #0005;}



.module-icon {width:45px;height:45px;border-radius:13px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#102f6b,#32145e);border:1px solid #4b66cf;font-size:1.55rem;margin-bottom:14px;box-shadow:0 0 17px #5c42ff25;}



.module-card h3 {font-size:1rem;margin:0 0 7px;}



.module-card p {font-size:.82rem;color:#aab9df;line-height:1.55;margin:0;}



.panel {border:1px solid #344783;border-radius:18px;padding:20px;background:linear-gradient(145deg,rgba(12,20,53,.98),rgba(7,12,31,.98));box-shadow:0 0 20px rgba(41,85,255,.08);}



.status-pill {display:inline-block;padding:6px 10px;border:1px solid #167c91;border-radius:99px;background:#082c43;color:#5df7ff;font-size:.74rem;font-weight:800;box-shadow:0 0 16px #00d9ff12;}



.stButton>button,.stDownloadButton>button {border:1px solid #5b69ff;border-radius:11px;background:linear-gradient(105deg,#245dff,#7a2dff,#d52dff);background-size:200% 200%;color:white;font-weight:800;min-height:2.7rem;transition:all .2s ease;box-shadow:0 0 15px rgba(93,72,255,.18);animation:buttonFlow 8s ease infinite;}



.stButton>button:hover,.stDownloadButton>button:hover {border-color:#63fbff;color:#fff;transform:translateY(-2px);box-shadow:0 0 24px rgba(0,220,255,.3);}



.stTextInput input,.stSelectbox [data-baseweb="select"],.stNumberInput input {background:#0b1430!important;border-color:#344780!important;border-radius:10px!important;color:#eef4ff!important;}



[data-testid="stMetric"] {background:linear-gradient(145deg,#111b4a,#090f2c);border:1px solid #344783;padding:15px;border-radius:15px;}



div[data-testid="stFileUploader"] {background:rgba(10,17,45,.9);border:1px dashed #5b58c9;border-radius:15px;padding:12px;}



hr {border-color:#252e61;}



[data-testid="stRadio"] label {padding-top:3px;padding-bottom:3px;}



@keyframes fadeUp {from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}



@keyframes colorFlow {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}



@keyframes textFlow {0%{background-position:0% center}100%{background-position:250% center}}



@keyframes bgShift {0%{background-position:0% 0%}100%{background-position:100% 100%}}



@keyframes orb {from{transform:translate(0,0) scale(.95)}to{transform:translate(-25px,20px) scale(1.08)}}



@keyframes buttonFlow {0%{background-position:0% 50%}100%{background-position:200% 50%}}



@media(max-width:700px){.hero{padding:24px 20px}.hero h1{font-size:2.5rem}.block-container{padding-top:1rem}}



</style>



""", unsafe_allow_html=True)







with st.sidebar:



    st.markdown("""



    <div class="brand">



      <div class="brand-mark">✳</div>



      <div><div class="brand-title">VISION X</div><div class="brand-sub">AI COMPUTER VISION STUDIO</div></div>



    </div>



    """, unsafe_allow_html=True)



    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)



    pages = ["Overview", "Live Vision Lab", "Image & Video", "Setup Guide", "About"]



    current = st.radio("Navigate", pages, label_visibility="collapsed",



                       index=pages.index(st.session_state.get("page", "Overview")) if st.session_state.get("page", "Overview") in pages else 0)



    st.session_state["page"] = current



    st.markdown("---")



    st.markdown('<div class="eyebrow">System</div>', unsafe_allow_html=True)



    st.markdown('<span class="status-pill">● Vision processing</span>', unsafe_allow_html=True)



    st.markdown('<p class="small-muted">Camera frames are processed through your browser session; uploaded files are processed by Vision X.</p>', unsafe_allow_html=True)



    st.markdown("---")



    st.caption("Vision X  •  Python / OpenCV / MediaPipe")







if current == "Overview":



    st.markdown("""



    <div class="hero">



      <div class="eyebrow">Computer vision workspace</div>



      <h1>See more.<br>Understand faster.</h1>



      <p>A futuristic AI lab for real-time hand tracking, gesture analysis, fitness posture, driver alertness and object detection — wrapped in a living neon interface.</p>







    </div>



    """, unsafe_allow_html=True)







    total = len(MODULE_INFO)



    k1,k2,k3,k4 = st.columns(4)



    cards = [



        ("AVAILABLE MODULES", str(total), "Integrated in this workspace"),



        ("PROCESSING", "LOCAL", "Runs on your machine"),



        ("CAMERA", "LIVE", "Webcam-based analysis"),



        ("DESIGN", "MODULAR", "Object-oriented engine"),



    ]



    for col, (label, value, note) in zip([k1,k2,k3,k4], cards):



        with col:



            st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)







    st.markdown('<div class="section-head"><div><h2>Explore your modules</h2><div class="section-sub">Choose a tool to open its controls in the Live Vision Lab.</div></div><span class="status-pill">WORKSPACE READY</span></div>', unsafe_allow_html=True)



    for start in range(0, len(MODULE_INFO), 3):



        cols = st.columns(3, gap="large")



        for col, (emoji, name, desc) in zip(cols, MODULE_INFO[start:start+3]):



            with col:



                st.markdown(f'<div class="module-card"><div class="module-icon">{emoji}</div><h3>{name}</h3><p>{desc}</p></div>', unsafe_allow_html=True)



                if st.button(f"Open {name} →", key=f"open_{name}", use_container_width=True):



                    st.session_state["selected_module"] = name



                    st.session_state["page"] = "Live Vision Lab"



                    st.rerun()



    st.markdown("")



    st.markdown('<div class="panel"><b>Quick tip</b><p class="small-muted">In Screenshot Capture mode, press <b>S</b> in the OpenCV preview window to save the current frame. Press <b>Q</b> or <b>ESC</b> to stop the camera.</p></div>', unsafe_allow_html=True)







elif current == "Live Vision Lab":



    st.markdown('<div class="eyebrow">Realtime workspace</div>', unsafe_allow_html=True)



    st.title("Live Vision Lab")



    st.markdown('<p class="small-muted">Select a module, configure your camera, then start real-time processing.</p>', unsafe_allow_html=True)



    names = [m[1] for m in MODULE_INFO if m[1] not in ("Text Recognition (OCR)", "Image / Video Analyzer")]



    default = st.session_state.get("selected_module", names[0])



    if default not in names:



        default = names[0]



    left, right = st.columns([0.85, 1.6], gap="large")



    with left:



        st.markdown('<div class="panel">', unsafe_allow_html=True)



        module = st.selectbox("Vision module", names, index=names.index(default))



        camera_index = st.number_input("Camera index", min_value=0, max_value=5, value=0, step=1)



        mirror = st.toggle("Mirror camera preview", value=True)



        show_fps = st.toggle("Show processing FPS", value=True)



        st.markdown("---")



        st.markdown("**Session controls**")



        st.markdown('<p class="small-muted">Press <b>Q</b> or <b>ESC</b> in the camera preview window to stop. Press <b>S</b> to save a screenshot.</p>', unsafe_allow_html=True)



        if module == "Virtual Mouse":



            st.warning("This module moves your real cursor. Keep your hand movements slow and deliberate.")



        if module == "Driver Drowsiness Detection":



            st.warning("Educational prototype only. Do not rely on it as a certified driver-safety device.")



        if st.button("▶  Start processing", use_container_width=True):

            st.session_state["camera_started"] = True



        if st.session_state.get("camera_started", False):

            if st.button("■  Stop processing", use_container_width=True):

                st.session_state["camera_started"] = False

                st.rerun()



        st.markdown('</div>', unsafe_allow_html=True)



    with right:



        st.markdown(f'<div class="panel"><div class="eyebrow">Selected module</div><h2 style="margin:.45rem 0">{module}</h2><p class="small-muted">Live camera feed and processing status appear here after you start the session.</p></div>', unsafe_allow_html=True)



        # Keep the live camera controls and preview in the original right-hand panel.

        preview = st.empty()

        status = st.empty()



        if st.session_state.get("camera_started", False):

            if module == "Virtual Mouse":

                st.info("On a hosted website, hand tracking works in the browser, but browser security prevents the server from moving your laptop's real OS cursor. Real cursor control is supported only when running locally.")

                # Preserve the original local Virtual Mouse implementation.

                host = ""

                try:

                    host = st.context.headers.get("host", "")

                except Exception:

                    pass

                is_hosted = "streamlit.app" in host or (host and "localhost" not in host and "127.0.0.1" not in host)

                if not is_hosted:

                    run_camera(module, camera_index=int(camera_index), mirror=mirror,

                            show_fps=show_fps, image_slot=preview, status_slot=status)

                else:

                    try:

                        webrtc_streamer(

                            key=f"vision-x-{module.lower().replace(' ', '-').replace('/', '-')}",

                            mode=WebRtcMode.SENDRECV,

                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},

                            video_processor_factory=lambda: BrowserVisionProcessor(

                                module=module, mirror=mirror, show_fps=show_fps

                            ),

                            media_stream_constraints={"video": {"width": 640, "height": 480}, "audio": False},

                            async_processing=True,

                        )

                        status.info("Allow browser camera access and click START in the camera panel.")

                    except Exception as exc:

                        st.error(f"Could not start browser camera: {exc}")

            else:

                try:

                    webrtc_streamer(

                        key=f"vision-x-{module.lower().replace(' ', '-').replace('/', '-')}",

                        mode=WebRtcMode.SENDRECV,

                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},

                        video_processor_factory=lambda: BrowserVisionProcessor(

                            module=module, mirror=mirror, show_fps=show_fps

                        ),

                        media_stream_constraints={"video": {"width": 640, "height": 480}, "audio": False},

                        async_processing=True,

                    )

                    status.info("Allow browser camera access and click START in the camera panel. Frames are processed by Vision X.")
                    st.caption("If the camera reports `navigator.mediaDevices is undefined`, open the deployed site directly using its HTTPS URL (not an HTTP link or an embedded preview), then allow Camera access in your browser settings.")

                except Exception as exc:

                    st.error(f"Could not start browser camera: {exc}")

                    st.info("Check streamlit-webrtc installation and browser camera permissions.")





elif current == "Image & Video":



    st.markdown('<div class="eyebrow">Media workspace</div>', unsafe_allow_html=True)



    st.title("Image & Video Analyzer")



    st.markdown('<p class="small-muted">Preview local media, inspect image dimensions and download the original file.</p>', unsafe_allow_html=True)



    upload = st.file_uploader("Choose an image or video", type=["png","jpg","jpeg","bmp","mp4","avi","mov","mkv"])



    if upload:



        ext = upload.name.lower().rsplit(".",1)[-1]



        if ext in ["png","jpg","jpeg","bmp"]:



            from PIL import Image



            img = Image.open(upload).convert("RGB")



            preview_col, info_col = st.columns([1.6, 1], gap="large")



            with preview_col:



                st.image(img, caption=upload.name, use_container_width=True)



            with info_col:



                st.markdown('<div class="panel">', unsafe_allow_html=True)



                st.markdown("### Image details")



                st.write("**Filename:**", upload.name)



                st.write(f"**Resolution:** {img.width} × {img.height}")



                st.write(f"**Format:** {img.format or ext.upper()}")



                st.write(f"**Color mode:** {img.mode}")



                st.download_button("Download original image", upload.getvalue(), file_name=upload.name, use_container_width=True)



                st.markdown('</div>', unsafe_allow_html=True)



        else:



            st.video(upload)



            st.info("For webcam-based processing, open Live Vision Lab.")



    else:



        st.markdown('<div class="panel"><h3>Ready for your media</h3><p class="small-muted">Supported images: JPG, PNG, BMP. Supported videos: MP4, AVI, MOV, MKV.</p></div>', unsafe_allow_html=True)







elif current == "Setup Guide":



    st.title("Setup Guide")



    st.markdown('<p class="small-muted">Recommended setup for Windows with Python 3.11.</p>', unsafe_allow_html=True)



    st.markdown("""



    <div class="panel">



    <div class="eyebrow">PowerShell commands</div>



    </div>



    """, unsafe_allow_html=True)



    st.code("""py -3.11 -m venv .venv



.\.venv\Scripts\Activate.ps1



python -m pip install --upgrade pip



python -m pip install -r requirements.txt



python -m streamlit run app.py""", language="powershell")



    st.markdown("**Controls**")



    st.markdown("- **Virtual Mouse:** index fingertip moves the cursor; pinch thumb and index finger to click once per pinch.")



    st.markdown("- **Driver Drowsiness:** repeating beep while eyes are detected closed; spoken warning follows sustained closure.")



    st.markdown("- **Screenshot Capture:** press **S** in the OpenCV preview window to save a frame.")



    st.markdown("- **Stop camera:** press **Q** or **ESC**.")



    st.warning("Driver drowsiness detection is an educational prototype, not a certified safety system.")







else:



    st.title("About Vision X")



    st.markdown('<p class="small-muted">A local-first, object-oriented Python computer-vision project.</p>', unsafe_allow_html=True)



    st.markdown("### Technology stack")



    t1,t2,t3,t4 = st.columns(4)



    for col, title, desc in zip([t1,t2,t3,t4], ["Python","OpenCV","MediaPipe","YOLO (optional)"],



                                ["Application logic","Camera and image processing","Hand, face and pose landmarks","Object detection add-on"]):



        with col:



            st.markdown(f'<div class="module-card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)



    st.markdown("### Included modules")



    for emoji, name, desc in MODULE_INFO:



        st.markdown(f"- {emoji} **{name}** — {desc}")



    st.caption("Detection quality depends on camera quality, lighting, angle, model availability and hardware.")
