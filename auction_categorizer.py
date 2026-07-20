import os
import gradio as gr
import google.generativeai as genai


API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-pro"

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

PROMPT = """
Act as an Auction House item categorizer. Given an item's title, description,
and image, determine:

1. Category: one or more categories that best fit the item.
2. Subcategory: one or more subcategories associated with the chosen
   category (in parentheses next to the category, if applicable).
3. Attributes: a list of relevant attributes for the item, drawn from the
   attribute set that matches the selected category/subcategory (e.g.
   material, condition, brand, size, era, color, etc.)

Format the response clearly using this structure:

Category: <category 1>, <category 2>, ...
Subcategory: <subcategory 1>, <subcategory 2>, ...
Attributes:
  - <attribute name>: <value or description>
  - <attribute name>: <value or description>
  ...

Be concise but thorough. If information is not visible or inferable, mark it
as "Unknown" rather than guessing.
"""


def configure_gemini(api_key: str) -> None:
    if not api_key:
        raise ValueError(
            "No Gemini API key found. Set GEMINI_API_KEY as an environment "
            "variable, or enter it in the API Key box in the UI."
        )
    genai.configure(api_key=api_key)


def categorize_item(image_path: str, text_input: str, api_key: str):
    """Uploads the image + text to Gemini and returns the categorization."""

    if not image_path:
        return "⚠️ Please upload an image of the item."
    if not text_input or not text_input.strip():
        return "⚠️ Please enter a title/description for the item."

    key_to_use = api_key.strip() if api_key and api_key.strip() else API_KEY

    try:
        configure_gemini(key_to_use)
    except ValueError as e:
        return f"❌ {e}"

    try:
        uploaded_file = genai.upload_file(image_path)

        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=GENERATION_CONFIG,
        )

        response = model.generate_content(
            [PROMPT, text_input.strip(), uploaded_file, "output: "]
        )

        return response.text

    except Exception as e:
        return f"❌ Error while processing item: {e}"


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="Auction House Categorizer") as demo:
    gr.Markdown(
        """
        # 🏺 Auction House Categorizer
        Upload a photo of an item and provide a short title/description.
        Gemini will suggest a **Category**, **Subcategory**, and relevant
        **Attributes** for the item.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                type="filepath",
                label="Item Image",
                height=320,
            )
            text_input = gr.Textbox(
                label="Title / Description",
                placeholder="e.g. Antique mahogany writing desk, early 1900s, "
                            "brass handles, minor scuffing on top surface",
                lines=5,
            )
            api_key_input = gr.Textbox(
                label="Gemini API Key (optional if GEMINI_API_KEY env var is set)",
                placeholder="Leave blank to use the environment variable",
                type="password",
            )
            submit_btn = gr.Button("Categorize Item", variant="primary")
            clear_btn = gr.Button("Clear")

        with gr.Column(scale=1):
            output_box = gr.Textbox(
                label="Categorization Result",
                lines=20,
                interactive=False,
            )

    submit_btn.click(
        fn=categorize_item,
        inputs=[image_input, text_input, api_key_input],
        outputs=output_box,
    )

    clear_btn.click(
        fn=lambda: (None, "", "", ""),
        inputs=[],
        outputs=[image_input, text_input, api_key_input, output_box],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
