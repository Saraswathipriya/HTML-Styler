import gradio as gr
from typing import Dict, List

# Optional AI model
from transformers import AutoTokenizer, AutoModelForCausalLM

USE_AI = False

if USE_AI:
    MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


# ===============================
# COLOR PALETTE GENERATOR
# ===============================

class ColorPaletteGenerator:

    palettes = {
        "modern":{
            "primary":"#667eea",
            "secondary":"#764ba2",
            "accent":"#f093fb",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "vibrant":{
            "primary":"#ff6b6b",
            "secondary":"#ff8e72",
            "accent":"#f5576c",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "ocean":{
            "primary":"#0099cc",
            "secondary":"#006699",
            "accent":"#00ccff",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "forest":{
            "primary":"#27ae60",
            "secondary":"#1e8449",
            "accent":"#52be80",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "sunset":{
            "primary":"#ff8c42",
            "secondary":"#ff6b35",
            "accent":"#ffa751",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "luxury":{
            "primary":"#1a1a1a",
            "secondary":"#333333",
            "accent":"#FFD700",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "creative":{
            "primary":"#9b59b6",
            "secondary":"#8e44ad",
            "accent":"#e74c3c",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        },

        "minimal":{
            "primary":"#2c3e50",
            "secondary":"#34495e",
            "accent":"#3498db",
            "background":"#0f172a",
            "surface":"#1e293b",
            "text":"#f1f5f9"
        }
    }

    @staticmethod
    def get_palette(style:str)->Dict:
        return ColorPaletteGenerator.palettes.get(style, ColorPaletteGenerator.palettes["modern"])


# ===============================
# SECTION DETECTION
# ===============================

def detect_sections(description:str)->List[str]:

    sections=[]
    desc=description.lower()

    if "hero" in desc or "banner" in desc:
        sections.append("hero")

    if "features" in desc or "services" in desc:
        sections.append("features")

    if "about" in desc:
        sections.append("about")

    if "portfolio" in desc or "gallery" in desc:
        sections.append("portfolio")

    if "testimonials" in desc or "reviews" in desc:
        sections.append("testimonials")

    if "pricing" in desc:
        sections.append("pricing")

    if "contact" in desc or "form" in desc:
        sections.append("contact")

    sections.append("footer")

    return sections


# ===============================
# CSS GENERATOR
# ===============================

def generate_css(colors):

    return f"""
<style>

body {{
font-family: Arial;
background:{colors['background']};
color:{colors['text']};
margin:0;
}}

header {{
background:{colors['primary']};
padding:80px;
text-align:center;
}}

section {{
padding:60px;
}}

.card {{
background:{colors['surface']};
padding:20px;
margin:10px;
border-radius:10px;
}}

footer {{
background:{colors['secondary']};
padding:20px;
text-align:center;
}}

button {{
background:{colors['accent']};
padding:12px 25px;
border:none;
border-radius:6px;
cursor:pointer;
}}

</style>
"""


# ===============================
# HTML GENERATOR
# ===============================

def generate_html(title,description,style):

    palette=ColorPaletteGenerator.get_palette(style)

    css=generate_css(palette)

    sections=detect_sections(description)

    html=f"""
<html>
<head>
<title>{title}</title>
{css}
</head>
<body>
"""

    if "hero" in sections:
        html+=f"""
<header>
<h1>{title}</h1>
<p>{description}</p>
<button>Get Started</button>
</header>
"""

    if "features" in sections:
        html+= """
<section>
<h2>Features</h2>
<div class='card'>Feature One</div>
<div class='card'>Feature Two</div>
<div class='card'>Feature Three</div>
</section>
"""

    if "about" in sections:
        html+= """
<section>
<h2>About</h2>
<p>Information about the company.</p>
</section>
"""

    if "portfolio" in sections:
        html+= """
<section>
<h2>Portfolio</h2>
<div class='card'>Project 1</div>
<div class='card'>Project 2</div>
</section>
"""

    if "contact" in sections:
        html+= """
<section>
<h2>Contact</h2>
<input placeholder="Name"><br><br>
<input placeholder="Email"><br><br>
<textarea placeholder="Message"></textarea>
</section>
"""

    html+="<footer>© 2026 Website</footer></body></html>"

    return html


# ===============================
# GRADIO UI
# ===============================

def create_page(title,description,style):

    html=generate_html(title,description,style)

    return html,html


with gr.Blocks() as app:

    gr.Markdown("# HTML Quick Styler")

    title=gr.Textbox(label="Page Title")

    description=gr.Textbox(label="Page Description")

    style=gr.Dropdown(
        ["modern","vibrant","ocean","forest","sunset","luxury","creative","minimal"],
        value="modern",
        label="Color Style"
    )

    btn=gr.Button("Generate Page")

    html_code=gr.Code(label="Generated HTML")

    preview=gr.HTML(label="Preview")

    btn.click(create_page,[title,description,style],[html_code,preview])


# IMPORTANT FOR VS CODE
if __name__ == "__main__":
    app.launch()