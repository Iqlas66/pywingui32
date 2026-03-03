from pywingui32 import PyWinGUI32 as gui


if __name__ == "__main__":
    response = gui.show_message("Configuration complete.", style="info")
    print(f"User clicked: {response}")

    if gui.show_message("Delete all files?", style="question") == "yes":
        print("User confirmed deletion.")
