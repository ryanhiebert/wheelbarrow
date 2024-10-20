from django.middleware.csrf import get_token
from nanodjango import Django
import logging_tree
from wheelbarrow import Wheelbarrow

app = Django()
wheelbarrow = Wheelbarrow()


@app.route("/")
async def deps(request):
    if request.method == "POST":
        details = ""
        if "upgrade" in request.POST:
            details = f"""
                <strong>Upgrading dependencies...</strong>
                <pre>{await wheelbarrow.upgrade()}</pre>
            """
        await wheelbarrow.reload()
        return f"""
            {details}
            <strong>Reloading the web server...</strong>
            <pre>{await wheelbarrow.diagnostics()}</pre>
            <a href="/">Done</a>
        """

    return (
        f"""
        <h1>Upgrade Dependencies</h1>
        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
            <button name="upgrade" type="submit">Upgrade</button>
            <button type="submit">Cycle</button>
        </form>
        <pre>{await wheelbarrow.diagnostics()}</pre>
        <details>
            <summary>Dependencies</summary>
            <pre>{await wheelbarrow.dependencies()}</pre>
        </details>
        <details>
            <summary>Logging Tree</summary>
            <pre>{logging_tree.format.build_description()}</pre>
        </details>
        """
    )
