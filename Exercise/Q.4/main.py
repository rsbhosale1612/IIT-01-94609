import argparse
from weather_app import cli, gui

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")
    args = parser.parse_args()
    if args.gui:
        gui.start_gui()
    else:
        cli.run_cli()

if __name__ == "__main__":
    main()
