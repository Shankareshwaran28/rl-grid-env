import gradio as gr
import matplotlib.pyplot as plt
from run import evaluate_env

# 🎨 Custom Fonts + UI Styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&family=Inter:wght@400;500&display=swap');

body {
    font-family: 'Inter', sans-serif;
    background: #0f172a;
    color: white;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
}

/* Buttons */
.gr-button {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #22c55e, #3b82f6) !important;
    color: white !important;
}

/* Textbox */
textarea, .gr-textbox {
    border-radius: 12px !important;
    background-color: #1e293b !important;
    color: white !important;
}

/* Dropdown */
.gr-dropdown {
    border-radius: 12px !important;
}
"""

# 🎮 Grid → HTML (Hero Icons)
def render_grid(grid):
    cols = len(grid[0])
    html = f"<div style='display:grid;grid-template-columns:repeat({cols},60px);gap:10px;justify-content:center;'>"

    agent_icon = """<svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" width="26" height="26">
    <path d="M12 2a7 7 0 00-7 7v4H4a1 1 0 000 2h1v2a3 3 0 003 3h8a3 3 0 003-3v-2h1a1 1 0 100-2h-1V9a7 7 0 00-7-7z"/>
    </svg>"""

    goal_icon = """<svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" width="26" height="26">
    <path d="M5 3v18l7-5 7 5V3H5z"/>
    </svg>"""

    obstacle_icon = """<svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" width="26" height="26">
    <path d="M6 6l12 12M6 18L18 6" stroke="white" stroke-width="2"/>
    </svg>"""

    for row in grid:
        for cell in row:
            color = "#1e293b"
            icon = ""

            if cell == "A":
                color = "#22c55e"
                icon = agent_icon
            elif cell == "G":
                color = "#3b82f6"
                icon = goal_icon
            elif cell == "X":
                color = "#ef4444"
                icon = obstacle_icon

            html += f"""
            <div style='width:60px;height:60px;
                        display:flex;align-items:center;justify-content:center;
                        background:{color};
                        border-radius:14px;
                        box-shadow:0 6px 15px rgba(0,0,0,0.4);
                        transition:0.2s;'>
                        {icon}
            </div>
            """
    html += "</div>"
    return html


# 📊 Chart
def create_chart(score):
    fig, ax = plt.subplots()
    ax.bar(["Score"], [score])
    ax.set_title("Final Score")
    ax.set_ylabel("Value")
    return fig


# 🧠 Main logic
def run_game(level):
    result, grid = evaluate_env(level)

    result_text = f"""
🎯 Success Rate: {result['success_rate']}
📊 Avg Steps: {result['avg_steps']}
🏆 Best Path: {result['best_path']}
⭐ Final Score: {result['final_score']}
"""

    return result_text, render_grid(grid), create_chart(result["final_score"])


# 🎨 UI DESIGN
with gr.Blocks(css=custom_css) as iface:

    gr.Markdown("""
# 🧠 Smart RL Grid Environment  
### 🚀 AI Agent + Visual Evaluation System
""")

    with gr.Row():
        level = gr.Dropdown(
            ["easy", "medium", "hard"],
            value="easy",
            label="🎮 Select Difficulty"
        )

    run_btn = gr.Button("🚀 Run Simulation")

    gr.Markdown("## 📊 Results")
    result_box = gr.Textbox(lines=6)

    gr.Markdown("## 🎮 Game Visualization")
    grid_display = gr.HTML()

    gr.Markdown("## 📈 Score Analysis")
    chart_display = gr.Plot()

    run_btn.click(
        fn=run_game,
        inputs=level,
        outputs=[result_box, grid_display, chart_display]
    )


# 🚀 Launch
iface.launch()