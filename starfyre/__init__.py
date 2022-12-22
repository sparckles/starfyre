import js


def render(js: str):
    div = js.document.createElement("div")
    div.innerHTML = f"{js}"
    return div


def render_root(component):
    div = js.document.createElement("div")
    div.appendChild(component)
    js.document.body.prepend(div)


__all__ = ["render", "render_root", "js"]
