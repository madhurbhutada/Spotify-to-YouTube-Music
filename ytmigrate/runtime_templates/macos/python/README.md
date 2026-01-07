# macOS Python Runtime - Setup Required

PYTHON 3 BINARY GOES HERE

This folder should contain a Python 3.8+ runtime for macOS.

WHAT YOU NEED:
--------------
Place the Python 3 binary and its dependencies in this folder structure:

macos/python/
└── bin/
    └── python3           <- Python executable

RECOMMENDED APPROACH:
--------------------
1. Download Python 3.8+ for macOS from python.org
2. Install it to a temporary location
3. Copy the Python binary from the installation to this folder
4. OR use a standalone Python distribution

ALTERNATIVE - Use System Python:
--------------------------------
If you prefer to use the system Python, you'll need to modify the
run_macos.command script to point to /usr/bin/python3 instead.

Note: Using system Python requires users to have Python installed.
An embedded runtime makes the tool truly portable.

FOR CONTRIBUTORS:
-----------------
If you've successfully set up the macOS runtime, please consider
contributing to the project!
