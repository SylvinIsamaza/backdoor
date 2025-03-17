import sys
from PyInstaller.__main__ import run
if __name__ == '__main__':
    common_options = [
        '--onefile',
        '--name', 'carmovementgame',
        '--clean',
        'game.py',
          '--icon=assets/car.ico',  
    ]

    if sys.platform.startswith('win'):
        options = [
            '--windowed',  
          
        ] + common_options
        run(options)
        run(['--onefile', '--name', 'cleanup', 'cleanup.py'])

    elif sys.platform.startswith('linux'):
        options = common_options
        run(options)
        run(['--onefile', '--name', 'cleanup', 'cleanup.py'])

    print("Build completed! Executables can be found in the 'dist' directory")