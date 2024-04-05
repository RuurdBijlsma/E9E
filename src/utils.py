import subprocess


def kill_java_processes() -> None:
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
                print(f"Killed Java process with PID {pid}")
    except subprocess.CalledProcessError:
        print("Error retrieving process list.")


def check_java_processes() -> bool:
    try:
        process_list = (
            subprocess.check_output(["ps", "ax"]).decode("utf-8").splitlines()
        )
        java_processes = any("java" in process.lower() for process in process_list)
        return java_processes
    except subprocess.CalledProcessError:
        return False
