from e2b import Sandbox as SandboxBase

import asyncio
import os
import signal
import platform


class Sandbox(SandboxBase):
    def start_stream(self):
        command = (
            "ffmpeg -f gdigrab -framerate 30 -i desktop -vcodec libx264 "
            "-preset ultrafast -tune zerolatency -f mpegts -listen 1 http://localhost:8080"
        )
        process = self.commands.run(command, background=True)
        self.process = process
        return f"https://{self.get_host(8080)}"

    def kill(self):
        if platform.system() == "Windows":
            os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)
        else:
            os.kill(self.process.pid, signal.SIGTERM)


class DisplayClient:
    def __init__(self, output_dir="."):
        self.process = None
        self.output_stream = f"{output_dir}/output.ts"
        self.output_file = f"{output_dir}/output.mp4"

    async def start_display_client(self, stream_url, title="Sandbox", delay=0):
        title = title.replace("'", "\\'")
        await asyncio.sleep(delay)  # Replace 'sleep' command with asyncio.sleep for compatibility
        self.process = await asyncio.create_subprocess_shell(
            f"ffmpeg -reconnect 1 -i {stream_url} -c:v libx264 -preset fast -crf 23 "
            f"-c:a aac -b:a 128k -f mpegts -loglevel quiet - > {self.output_stream} && "
            f"ffplay -autoexit -i {self.output_stream} -loglevel quiet -window_title '{title}'",
            stdin=asyncio.subprocess.DEVNULL,
        )

    async def stop_display_client(self):
        if self.process:
            try:
                self.process.terminate()  # Terminate process in Windows-compatible way
            except ProcessLookupError:
                pass
            await self.process.wait()

    async def save_stream(self):
        process = await asyncio.create_subprocess_shell(
            f"ffmpeg -i {self.output_stream} -c:v copy -c:a copy -loglevel quiet {self.output_file}"
        )
        await process.wait()

        if process.returncode == 0:
            print(f"Stream saved successfully as {self.output_file}.")
        else:
            print(f"Failed to save the stream as {self.output_file}.")
