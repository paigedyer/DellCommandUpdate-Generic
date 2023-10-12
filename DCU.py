import subprocess
from pathlib import Path
import os
import ctypes
import sys


def run_dcu_scan():
    # Variables
    path = "C:\\Program Files\\Dell\\CommandUpdate\\dcu-cli.exe"
    path_secondary = "C:\\Program Files (x86)\\Dell\\CommandUpdate\\dcu-cli.exe"
    checkpath = Path(path)
    scan = '/scan'
    output = []
    num_updates = None

    try:
        # Opens a new subprocess to run dcu-cli.exe /scan
        if os.path.isfile(path):
            result = subprocess.run(f'"{path}" {scan}', shell=True, capture_output=True, text=True, check=True)
        elif os.path.isfile(path_secondary):
            result = subprocess.run(f'"{path_secondary}" {scan}', shell=True, capture_output=True, text=True, check=True)
        # Store the output in a list
        output = result.stdout
        # Displays the output of the dcu-cli
        print(output)

        # Handle exceptions
        # TODO create exception handling process
    except subprocess.CalledProcessError as e:
        print("Error: ",
              e)  # Ex. Command '"C:\Program Files\Dell\CommandUpdate\dcu-cli.exe" /scan' returned non-zero exit status 4.
        # print("Error Output:", e.stderr) Commented out, not needed.

        error = str(e)

        if "exit status 500" in error:
            num_updates = int(0)
            print("No updates available for the current system.")
        if "exit status 1" in error:
            print("Reboot required.")

    # TODO what does it do if there are no updates

    available = "Number of applicable updates"
    bios = "BIOS"
    output = str(output)
    temp = []
    temp = output.split('\n')
    # print(temp) Remove comment if troubleshooting or want to see which updates are available

    for item in temp:
        if available in item:

            list = []
            list = item.split(': ')
            num_updates = int(list[1])
            print(num_updates, "updates are available.")
            # This section looks for the string that states the number of updates and
            # separates it to isolate the integer.
        if bios in item:
            print("BIOS update available")
            '''ctypes.windll.user32.MessageBoxW(0,
                                             "BIOS update is available. Please make sure your computer is connected "
                                             "to power and internet.",
                                             "Dell Command Update", 1)'''

        else:
            pass

    if num_updates!= None:
        return num_updates
    elif num_updates == None:
        num_updates = int(0)
        return num_updates


def run_updates(dcu_present):
    path = "C:\\Program Files\\Dell\\CommandUpdate\\dcu-cli.exe"
    path_secondary = "C:\\Program Files (x86)\\Dell\\CommandUpdate\\dcu-cli.exe"

    command = "/configure -silent -autoSuspendBitLocker=enable -userConsent=disable -scheduleManual"
    if os.path.isfile(path):
        try:
            proc = subprocess.run(f'"{path}" {command}', shell=True, capture_output=True, text=True, check=True)
            output = proc.stdout
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

        try:

            command = "/applyUpdates -silent -reboot=enable -outputLog=C:\Dell-CU-apply.log"

            proc = subprocess.run(f'"{path}" {command}', shell=True, capture_output=True, text=True, check=True)
            output = proc.stdout
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

    elif os.path.isfile(path_secondary):
        try:
            proc = subprocess.run(f'"{path_secondary}" {command}', shell=True, capture_output=True, text=True, check=True)
            output = proc.stdout
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

        try:

            command = "/applyUpdates -silent -reboot=enable -outputLog=C:\Dell-CU-apply.log"

            proc = subprocess.run(f'"{path_secondary}" {command}', shell=True, capture_output=True, text=True, check=True)
            output = proc.stdout
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error: ", e)


    # TODO when get output read what the string is to make another if statement


def check_dcu():
    path = "C:\\Program Files\\Dell\\CommandUpdate\\dcu-cli.exe"
    path_secondary = "C:\\Program Files (x86)\\Dell\\CommandUpdate\\dcu-cli.exe"
    if os.path.isfile(path):
        dcu_present = True
    if os.path.isfile(path_secondary):
        dcu_present = True
        path = path_secondary
    else:
        dcu_present = False

    return dcu_present


def install_dcu():
    path = "C:\\Program Files\\Dell\\CommandUpdate\\dcu-cli.exe"
    path_secondary = "C:\\Program Files (x86)\\Dell\\CommandUpdate\\dcu-cli.exe"
    filename = "test.bat"
    if (os.path.isfile(path)) or (os.path.isfile(path_secondary)):
        dcu_present = True
        # print("Dell Command Update already installed.") Removed because of redundancy
    # If the file for Command Update command line interface is not present
    else:
        dcu_present = False
        print("Dell Command Update not installed. Beginning installation...")
        # TODO change title of batch file

        # runs a batch file that transfers the file from file server to computer
        proc = subprocess.run(f'"\\\\pbovpfsmb01\\install\\CommandUpdate\\test.bat" start {filename}',
                              shell=True, capture_output=True, text=True, check=True)

        # If the file was transferred successfully
        if os.path.isfile("C:\\Windows\DellCommandUpdate.msi"):
            print("Installer found")
            path = "C:\\Windows"
            # filename = "DCU_Setup_4_3_0.exe"
            filename = "startInstall.bat"
            try:
                # Starts the installation of Dell Command Update
                proc = subprocess.run(
                    f'"\\\\pbovpfsmb01\\install\\CommandUpdate\\startInstall.bat" start {filename}',
                    shell=True, capture_output=True, text=True, check=True)
                # Captures the output
                output = proc.stdout
            except subprocess.CalledProcessError as e:
                print("Error: ", e)
                print("Error Output:", e.stderr)


        elif not os.path.isfile("C:\\Windows\\DellCommandUpdate.msi"):
            print("Installer not found.")


def main():
    running = True
    print("checking for Dell Command Update.")
    dcu_present = check_dcu()
    if dcu_present:
        print("Dell Command Update found")
    else:
        sys.exit("Dell Command Update not found. Aborting.")

    while running:
        if dcu_present:
            print("Scanning for Updates.")
            num_updates = run_dcu_scan()
            num_updates = int(num_updates)
            if num_updates > 0:
                print("Updates available: ", num_updates)
                run_updates(dcu_present)
                num_updates = run_dcu_scan()
                num_updates = int(num_updates)
                if num_updates == 0:
                    print("Updates installed :)")
                    running = False
                if num_updates == 0:
                    print(num_updates, " updates remaining.")
            elif num_updates == 0:
                print("No updates available.")
                running = False
                pass
            else:
                print("Error scanning for updates.")
                running = False
        else:
            print("Installing Dell Command Update.")
            install_dcu()
            pass


install_dcu()
main()
