# Local Image Background Remover (`rembg`)

An offline, local background removal setup powered by [danielgatis/rembg](https://github.com/danielgatis/rembg).

---

## 🛡️ Security & Privacy Audit Report

As requested, a security audit was performed on the package and dependencies:

1. **Origin & Authenticity**:
   - Installed directly from official PyPI (`rembg[cpu,cli]`).
   - The package is open-source under the MIT license, created and maintained by Daniel Gatis with 17k+ GitHub stars.
2. **Local Inference (Zero Data Leakage)**:
   - All image processing is performed **100% locally** using Microsoft ONNX Runtime on your CPU.
   - No telemetry, analytics, or images are transmitted over the network.
3. **Model Integrity**:
   - Model weights (e.g., `u2net.onnx`) are downloaded via HTTPS strictly from official GitHub release assets and verified with hardcoded cryptographic hashes (MD5) before execution.
   - The default model (`u2net`) has already been downloaded and verified in your local cache (`~/.u2net/u2net.onnx`).

---

## 🚀 How to Use

You have **4 ways** to use the tool:

### 1. Web UI (Recommended)
Double-click:
```text
start_web_ui.bat
```
or run in terminal:
```powershell
.\.venv\Scripts\activate
python app.py
```
This opens an interactive interface in your browser (`http://127.0.0.1:7860`) where you can:
- Drag and drop images or paste from clipboard.
- Compare original and background-removed results.
- Adjust edge refinement / alpha matting for hair and fine details.
- Batch process multiple images at once.

---

### Running on macOS (Non-Technical & Automatic)

For Mac users, everything is automated into a single double-clickable script:

1. **Double-click:**
   ```text
   Setup_And_Run_Mac.command
   ```
2. **What happens automatically:**
   - Detects if Python 3 is installed (prompts automatic setup if needed).
   - Automatically sets up the isolated environment and dependencies.
   - Pre-downloads the AI model for offline use.
   - Automatically opens your web browser to the Background Remover tool!
3. **Subsequent Runs**:
   - Double-clicking `Setup_And_Run_Mac.command` will skip setup and open the app in under 2 seconds.

*(Note for Mac: If macOS shows an "access privileges" notice the first time, simply right-click the file and select **Open**, or run `chmod +x *.command` in Terminal).*

---

### 2. Drag & Drop (Instant)
Simply drag any image file from Windows File Explorer and drop it onto:
```text
drag_and_drop_here.bat
```
The background will be stripped and saved as `<image_name>_no_bg.png` right next to the original.

---

### 3. Command Line (CLI)

#### Using `remove_bg.py`:
```powershell
# Single image
.\.venv\Scripts\python remove_bg.py input.jpg output.png

# Batch directory
.\.venv\Scripts\python remove_bg.py --batch ./images_folder ./output_folder
```

#### Using native `rembg` CLI:
```powershell
# Single image
.\.venv\Scripts\rembg i input.png output.png

# Whole folder
.\.venv\Scripts\rembg p ./input_folder ./output_folder
```

---

### 4. In Python Code
```python
from rembg import remove
from PIL import Image

input_image = Image.open("photo.jpg")
output_image = remove(input_image)
output_image.save("photo_no_bg.png")
```

---

## 📂 Project Structure
- `.venv/` - Isolated Python virtual environment.
- `app.py` - Local Gradio Web UI with single & batch modes.
- `remove_bg.py` - Command-line script with error handling and batch directory support.
- `start_web_ui.bat` - 1-click launcher for the Web UI.
- `drag_and_drop_here.bat` - Windows drag-and-drop launcher.
