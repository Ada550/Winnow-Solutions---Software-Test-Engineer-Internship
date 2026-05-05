import subprocess
import os
import signal
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Configurare ---
VIDEO_DIR = os.path.abspath("./videos")
# Pe Windows, calea ar putea fi "C:/Program Files/VideoLAN/VLC/vlc.exe"
# Pe Linux/Mac, de obicei este doar "vlc"
PLAYER_PATH = "vlc" 

# Variabilă globală pentru a urmări procesul video activ
current_process = None

def stop_existing_video():
    """Oprește procesul video dacă acesta rulează."""
    global current_process
    if current_process and current_process.poll() is None:
        try:
            # Trimite semnal de terminare (compatibil Cross-platform)
            current_process.terminate()
            current_process.wait(timeout=2)
        except Exception:
            current_process.kill()
        current_process = None

@app.route('/status', methods=['GET'])
def get_status():
    """Returnează starea curentă a sistemului de playback."""
    global current_process
    if current_process and current_process.poll() is None:
        return jsonify({
            "status": "PLAYING",
            "message": "A video is currently being displayed."
        }), 200
    return jsonify({
        "status": "IDLE",
        "message": "System is ready for a new scenario."
    }), 200

@app.route('/play', methods=['POST'])
def play_video():
    """Declanșează un scenariu video specific."""
    global current_process
    scenario_id = request.args.get('scenario_id')
    
    if not scenario_id:
        return jsonify({"error": "Missing 'scenario_id' parameter"}), 400

    video_path = os.path.join(VIDEO_DIR, f"{scenario_id}.mp4")
    
    if not os.path.exists(video_path):
        return jsonify({"error": f"Scenario '{scenario_id}' not found at {video_path}"}), 404

    # Gestionarea cererilor repetate: oprim ce rulează înainte de a începe ceva nou
    stop_existing_video()

    try:
        # Rulăm VLC cu argumente pentru automatizare:
        # --play-and-exit: închide playerul după video
        # --fullscreen: ocupă tot ecranul pentru camera Winnow Vision
        # --no-video-title-show: ascunde titlul fișierului de pe ecran
        cmd = [PLAYER_PATH, "--play-and-exit", "--fullscreen", "--no-video-title-show", video_path]
        current_process = subprocess.Popen(cmd)
        
        return jsonify({
            "message": f"Playback started: {scenario_id}",
            "path": video_path
        }), 200
    except FileNotFoundError:
        return jsonify({"error": "VLC player not found. Please check PLAYER_PATH."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_video():
    """Oprește manual orice redare activă."""
    stop_existing_video()
    return jsonify({"message": "Playback stopped successfully"}), 200

if __name__ == '__main__':
    # Creăm folderul de resurse dacă lipsește
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
        print(f"[*] Created directory: {VIDEO_DIR}")
        
    print("--- Winnow Playback Control Service Started ---")
    app.run(host='127.0.0.1', port=5000, debug=False)