import sys
import platform
from PyInstaller.__main__ import run

if __name__ == '__main__':
    common_options = [
        '--onefile',
        '--name', 'CarMovementGame',
        '--clean',
        'game.py',
        '--icon=assets/car.ico', 
    ]

    cleanup_common_options = [
        '--onefile',
        '--name', 'carCleanup',
        '--clean',
        'cleanup.py',
    ]

    build_all = '--all' in sys.argv

    current_os = sys.platform

    if build_all:
        print("Building executables for all supported OSes (Windows and Linux)...")
        print("Note: PyInstaller can only build for the current OS. Run this script on each OS to generate all binaries.")

        print("\nConfiguring build for Windows...")
        windows_options = [
            '--windowed', 
        ] + common_options
        run(windows_options)
        run(cleanup_common_options)  

        print("\nConfiguring build for Linux...")
        linux_options = common_options
        run(linux_options)
        run(cleanup_common_options)

        print("\nBuild completed! Executables for the current OS can be found in the 'dist' directory.")
        if current_os.startswith('win'):
            print("Windows binaries generated. Run this script on Linux with --all to generate Linux binaries.")
        elif current_os.startswith('linux'):
            print("Linux binaries generated. Run this script on Windows with --all to generate Windows binaries.")
        else:
            print("Unsupported OS detected. Only Windows and Linux are supported.")

    else:
        if current_os.startswith('win'):
            print("Building for Windows...")
            options = [
                '--windowed',  
            ] + common_options
            run(options)
            run(cleanup_common_options)
            print("Build completed! Windows executables can be found in the 'dist' directory")

        elif current_os.startswith('linux'):
            print("Building for Linux...")
            options = common_options
            run(options)
            run(cleanup_common_options)
            print("Build completed! Linux executables can be found in the 'dist' directory")

        else:
            print("Error: Unsupported OS. This script supports Windows and Linux only.")
            sys.exit(1)