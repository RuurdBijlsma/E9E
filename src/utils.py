import asyncio
import shutil
import subprocess
from pathlib import Path


async def kill_server(server_process: subprocess.Popen | None, kill_timeout=5) -> bool:
    if server_process:
        server_process.kill()
    kill_server_processes()
    waited = 0
    while True:
        if not is_server_on():
            return True
        await asyncio.sleep(0.05)
        waited += 0.05
        if waited >= kill_timeout:
            return False


def kill_server_processes() -> None:
    try:
        # Get a list of all running processes containing "java" in their command
        process_list = (
            subprocess.check_output(["ps", "-A"]).decode("utf-8").splitlines()
        )

        # Iterate through the process list
        for process in process_list:
            if "java" in process.lower():
                # Extract the process ID (PID)
                pid = int(process.split()[0])
                # Kill the process
                subprocess.run(["kill", "-9", str(pid)])
                print(f"Killed {process.lower()} process with PID {pid}")
    except subprocess.CalledProcessError:
        print("Error retrieving process list.")


def is_server_on() -> bool:
    try:
        process_list = (
            subprocess.check_output(["ps", "ax"]).decode("utf-8").splitlines()
        )
        java_processes = any(
            "java" in process.lower() and "defunct" not in process.lower()
            for process in process_list
        )
        return java_processes
    except subprocess.CalledProcessError:
        return False


def copy_world() -> bool:
    source = Path("/world")
    target = Path("/server/world")

    if not source.exists() and not target.exists():
        print(
            "Source directory for world does not exist, and there is no server world yet"
        )
        return False

    # Check if the target folder exists
    if target.exists():
        print(f"Target folder '{target}' already exists. No need to copy world.")
        return True
    else:
        # Copy the contents from source to target
        try:
            shutil.copytree(source, target)
            print(f"Folder copied from '{source}' to '{target}'.")
            return True
        except Exception as e:
            print(f"Error copying folder: {e}")
            return False
