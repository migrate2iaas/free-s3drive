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


#TODOs:
# 1. set icon
# 2. debug unmount (maybe child proc\threads are not deleted...)
# 3. Open drive letter with explorer
# 4. Fix permissions to read\write
# 5. Manipulate read\write with an option
# 6. 'Remember credentials...' feature.
