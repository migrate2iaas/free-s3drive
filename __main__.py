"""the main module. up for parsing command line parms and doing actions"""

def main():
    import sys
    if getattr( sys, 'frozen', False ) :
        # running in a bundle , we exec the same module
        import bundle_main
        return bundle_main.main()
    else:
        import gui
        gui.start_gui()

if __name__ == '__main__':
    main()
