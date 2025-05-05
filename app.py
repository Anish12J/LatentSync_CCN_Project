
import streamlit as st
import os
import subprocess
import tempfile
import uuid

# Create output folder
OUTPUT_FOLDER = "/content/output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def run_inference(video_file, audio_file, inference_steps, guidance_scale):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save input files temporarily
        video_path = os.path.join(tmpdir, "input_video.mp4")
        audio_path = os.path.join(tmpdir, "input_audio.wav")

        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())

        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        inference_script_path = "/content/LatentSync/inference.sh"

        # Generate a unique filename for output
        unique_id = str(uuid.uuid4())
        video_out_path_raw = os.path.join(OUTPUT_FOLDER, f"{unique_id}_raw.mp4")
        video_out_path_final = os.path.join(OUTPUT_FOLDER, f"{unique_id}.mp4")

        # Run inference - Pass video_path, audio_path, output_path directly
        command = [
            "bash", inference_script_path,
            video_path,
            audio_path,
            video_out_path_raw
        ]

        result = subprocess.run(command)

        if result.returncode != 0:
            raise RuntimeError("Inference script failed!")

        # Check if output exists
        if not os.path.exists(video_out_path_raw):
            raise FileNotFoundError(f"Inference did not produce output video: {video_out_path_raw}")

        # Re-encode the video for Streamlit compatibility
        ffmpeg_command = f"ffmpeg -y -i {video_out_path_raw} -vcodec libx264 -pix_fmt yuv420p {video_out_path_final}"
        subprocess.run(ffmpeg_command, shell=True, check=True)

        return video_out_path_final

def main():
    st.title("LatentSync Inference App")
    st.header("Upload Video and Audio Files")

    video_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

    inference_steps = st.slider("Inference Steps", min_value=1, max_value=50, value=20, step=1)
    guidance_scale = st.slider("Guidance Scale", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

    if st.button("Submit"):
        if video_file is not None and audio_file is not None:
            st.write("Running inference...")
            output_video_path = run_inference(video_file, audio_file, inference_steps, guidance_scale)
            st.write("Inference completed! Here's the result:")
            st.video(output_video_path)

            # Add download button
            with open(output_video_path, "rb") as file:
                st.download_button(
                    label="Download Synced Video",
                    data=file,
                    file_name=os.path.basename(output_video_path),
                    mime="video/mp4"
                )
        else:
            st.error("Please upload both a video and an audio file.")

if __name__ == "__main__":
    main()
