#!/usr/bin/env python3
"""NEON DRIFT — open-source AI street racer.

Gradio hosts the game and can mint a public share URL (*.gradio.live)
so anyone can play. Cars are generated in the browser with Stable Diffusion
(SDXL Turbo) or Flux via the public Pollinations image API — no GPU, no API key.
"""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parent
GAME_HTML = ROOT / "game.html"

CSS = """
html, body { background: #07010f !important; }
.gradio-container {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
  background: #07010f !important;
}
.gradio-container .contain, .wrap, .main, .prose {
  max-width: 100% !important;
  padding: 0 !important;
}
footer, .footer, .built-with { display: none !important; }
#nd-frame iframe, iframe.nd-frame {
  width: 100%;
  height: 100vh;
  border: 0;
  display: block;
  background: #07010f;
}
"""


def game_iframe() -> str:
    raw = GAME_HTML.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return (
        '<iframe class="nd-frame" title="NEON DRIFT" '
        f'src="data:text/html;base64,{b64}" '
        'allow="autoplay; fullscreen" allowfullscreen '
        'tabindex="0"></iframe>'
    )


def build_demo() -> gr.Blocks:
    with gr.Blocks(
        title="NEON DRIFT — AI Street Racer",
        fill_height=True,
        fill_width=True,
        analytics_enabled=False,
    ) as demo:
        gr.HTML(
            game_iframe(),
            elem_id="nd-frame",
            padding=False,
            container=False,
            min_height=720,
            apply_default_css=False,
            js_on_load=(
                "const f = element.querySelector('iframe');"
                "if (f) { f.style.width='100%'; f.style.height='100vh'; f.style.border='0'; f.focus(); }"
            ),
        )
    return demo


demo = build_demo()


def main() -> None:
    parser = argparse.ArgumentParser(description="NEON DRIFT — AI street racer")
    parser.add_argument("--share", dest="share", action="store_true", help="Create a public *.gradio.live link")
    parser.add_argument("--no-share", dest="share", action="store_false", help="Disable public share link")
    parser.set_defaults(share=os.environ.get("GRADIO_SHARE", "1") not in {"0", "false", "False"})
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "7860")))
    args = parser.parse_args()
    share = args.share

    launch_kwargs = dict(
        server_name=args.host,
        server_port=args.port,
        share=share,
        css=CSS,
        ssr_mode=False,
        strict_cors=False,
        pwa=True,
        theme=gr.themes.Base(
            primary_hue="fuchsia",
            secondary_hue="cyan",
            neutral_hue="slate",
        ).set(body_background_fill="#07010f"),
    )

    try:
        demo.launch(**launch_kwargs)
    except Exception as exc:
        print(f"Launch with share={share} failed ({exc!r}); retrying locally.")
        launch_kwargs["share"] = False
        demo.launch(**launch_kwargs)


if __name__ == "__main__":
    main()
