import os
import io
import gradio as gr
from PIL import Image
from rembg import new_session, remove

# Pre-cache default session
sessions = {
    "u2net (General use - recommended)": new_session("u2net"),
}

def get_session(model_name: str):
    raw_name = model_name.split()[0]
    if raw_name not in sessions:
        sessions[raw_name] = new_session(raw_name)
    return sessions[raw_name]

def process_single_image(
    image: Image.Image,
    model_choice: str,
    alpha_matting: bool,
    erode_size: int,
):
    if image is None:
        return None
    session = get_session(model_choice)
    return remove(
        image,
        session=session,
        alpha_matting=alpha_matting,
        alpha_matting_erode_size=int(erode_size),
    )

def process_batch(
    files: list,
    model_choice: str,
    alpha_matting: bool,
    erode_size: int,
):
    if not files:
        return []
    session = get_session(model_choice)
    results = []
    for file_path in files:
        try:
            with Image.open(file_path) as img:
                out = remove(
                    img.convert("RGBA"),
                    session=session,
                    alpha_matting=alpha_matting,
                    alpha_matting_erode_size=int(erode_size),
                )
                output_name = os.path.splitext(os.path.basename(file_path))[0] + "_no_bg.png"
                temp_dir = os.path.join(os.getcwd(), "output")
                os.makedirs(temp_dir, exist_ok=True)
                save_path = os.path.join(temp_dir, output_name)
                out.save(save_path, "PNG")
                results.append(save_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return results

def create_ui():
    custom_css = """
    .gradio-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .hero-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .hero-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-header p {
        color: #6b7280;
        font-size: 1.05rem;
    }
    """

    model_options = [
        "u2net (General use - recommended)",
        "u2netp (Lightweight & fast)",
        "u2net_human_seg (Optimized for human portraits)",
        "isnet-general-use (High precision general use)",
        "silueta (Ultra-compact)",
    ]

    with gr.Blocks(title="Background Remover (rembg)", css=custom_css, theme=gr.themes.Soft()) as demo:
        with gr.Column(elem_classes=["hero-header"]):
            gr.Markdown(
                """
                # 🖼️ Local Background Remover
                **Powered by [danielgatis/rembg](https://github.com/danielgatis/rembg)**  
                *100% private & local inference via ONNX Runtime. No images are sent to any external server.*
                """
            )

        with gr.Tabs():
            with gr.TabItem("Single Image"):
                with gr.Row():
                    with gr.Column(scale=1):
                        input_img = gr.Image(
                            label="Upload Image",
                            type="pil",
                            sources=["upload", "clipboard"],
                        )
                        model_dropdown = gr.Dropdown(
                            label="Model",
                            choices=model_options,
                            value=model_options[0],
                        )
                        with gr.Accordion("Advanced Refinement Settings", open=False):
                            alpha_matting = gr.Checkbox(
                                label="Alpha Matting (Refines fine edges like hair/fur)",
                                value=False,
                            )
                            erode_size = gr.Slider(
                                label="Alpha Matting Erode Size",
                                minimum=1,
                                maximum=40,
                                step=1,
                                value=10,
                            )
                        btn_run = gr.Button("✨ Remove Background", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        output_img = gr.Image(
                            label="Result (Transparent PNG)",
                            type="pil",
                            format="png",
                            image_mode="RGBA",
                        )

                btn_run.click(
                    fn=process_single_image,
                    inputs=[input_img, model_dropdown, alpha_matting, erode_size],
                    outputs=[output_img],
                )

            with gr.TabItem("Batch Processing"):
                gr.Markdown("Upload multiple images to process them all at once. Outputs will be saved in the `./output` folder.")
                with gr.Row():
                    with gr.Column():
                        batch_files = gr.File(
                            label="Select multiple images",
                            file_count="multiple",
                            file_types=["image"],
                        )
                        batch_model = gr.Dropdown(
                            label="Model",
                            choices=model_options,
                            value=model_options[0],
                        )
                        batch_matting = gr.Checkbox(
                            label="Alpha Matting",
                            value=False,
                        )
                        batch_erode = gr.Slider(
                            label="Alpha Matting Erode Size",
                            minimum=1,
                            maximum=40,
                            step=1,
                            value=10,
                        )
                        btn_batch = gr.Button("⚡ Process All Images", variant="primary", size="lg")
                    with gr.Column():
                        batch_gallery = gr.Gallery(
                            label="Processed Results",
                            columns=3,
                            height="auto",
                        )

                btn_batch.click(
                    fn=process_batch,
                    inputs=[batch_files, batch_model, batch_matting, batch_erode],
                    outputs=[batch_gallery],
                )

    return demo

if __name__ == "__main__":
    app = create_ui()
    print("\n" + "="*60)
    print("🚀 Background Remover Web UI starting at http://127.0.0.1:7860")
    print("="*60 + "\n")
    app.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
