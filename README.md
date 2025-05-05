# 🎬 LatentSync - Streamlit Deployment

This repository provides a user-friendly interface for **LatentSync**, a model that synchronizes lip movement in video with input audio using diffusion models. This setup allows you to run inference on your own uploaded video and audio files via a web app.

## 📂 Project Structure

- `inference.sh` – Bash script that invokes the core inference logic with required arguments.  
- `app.py` – Streamlit web application to upload video/audio files and run LatentSync inference.

## 🚀 How to Run Locally

### 1. Clone the LatentSync Repository

```bash
git clone https://github.com/bytedance/LatentSync.git
cd LatentSync
```

### 2. Add the Streamlit App

Place the provided `app.py` and `inference.sh` inside the root or a custom directory of the cloned repo. Update the path in `app.py` if needed.

### 3. Install Dependencies

Make sure Python, ffmpeg, and the required libraries are installed:

```bash
pip install streamlit
pip install -r requirements.txt  # Assuming the LatentSync repo has one
sudo apt install ffmpeg
```

### 4. Run the App

```bash
streamlit run app.py
```

## 🧪 How It Works

1. Upload a video and an audio file.  
2. The app saves them temporarily.  
3. `inference.sh` runs `scripts.inference` with:
   - Model configs from `configs/unet/stage2.yaml`
   - Pretrained weights from `checkpoints/latentsync_unet.pt`  
4. The resulting video is re-encoded using ffmpeg for web compatibility.  
5. The synced video is displayed and downloadable.

## ⚠️ Notes

- Make sure your paths inside `inference.sh` and `app.py` reflect your local directory structure.  
- If using Google Colab or Docker, adjust the paths to match container/Colab conventions.  
- LatentSync expects pre-trained weights to be placed in `checkpoints/`.

## 📁 Output Directory

All output videos are stored in:

```
/content/output
```

Change the `OUTPUT_FOLDER` variable in `app.py` to customize this.
