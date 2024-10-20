"""Manage a live running Python web application."""
import os
import signal
import logging
import anyio

__all__ = ["Wheelbarrow"]

logger = logging.getLogger(__name__)


class Wheelbarrow:
    async def reload(self):
        """Reload the web server."""
        # Send the SIGHUP signal to the parent process to reload
        # gunicorn and the web application without downtime.
        os.kill(os.getppid(), signal.SIGHUP)

    # NOTE: These APIs are definitely not stable. I know I don't like
    #       them, but I'm proving the functionality before the API.
    #       I'm not settled on how to handle async vs sync,
    #       and these APIs don't support streaming which is critical
    #       for cases where it may take some time for things to finish.

    async def diagnostics(self):
        """Return text diagnostic information."""
        return f"PID: {os.getpid()}    PPID: {os.getppid()}"

    async def upgrade(self):
        """Upgrade all of the dependencies.

        Return the combined stdout and stderr output.
        """
        sync = await anyio.run_process("uv sync --upgrade")
        return f"{sync.stdout.decode()}\n\n{sync.stderr.decode()}"

    async def dependencies(self):
        """List the dependencies."""
        dependencies = await anyio.run_process("uv pip list")
        return dependencies.stdout.decode()
