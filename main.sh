#!/bin/bash

# Default values
SOURCE="content"
TEMPLATE="template.html"
STATIC="static"
OUTPUT="public"
PORT=8888

# Loop through all cli args
# $# represents the number of args
# The loop continues as long as there are arguments left
while [[ $# -gt 0 ]]; do
    # Matches the current argument ($1) against patterns
    case "$1" in
        # Pattern for "--source=<something>" arg
        --source=*)
            # ${1#*=} removes everything up to and including the "="
            # This extracts the value after the "="
            SOURCE="${1#*=}"
            # Remove the current arg and shift all others one position to the left
            # This makes the next argument become $1
            shift
            ;;
        --template=*)
            TEMPLATE="${1#*=}"
            shift
            ;;
        --static=*)
            STATIC="${1#*=}"
            shift
            ;;
        --output=*)
            OUTPUT="${1#*=}"
            shift
            ;;
        --port=*)
            PORT="${1#*=}"
            shift
            ;;
        # Default case for unknown arg
        *)
            echo "Unknown option: $1" # Display error message
            exit 1                    # Exit with error code
            ;;
    esac
done

# Run the static site generator Python script with the configured params
# Pass the arguments with their respective flags
python3 src/main.py --source "$SOURCE" --template "$TEMPLATE" --static "$STATIC" --output "$OUTPUT"

# Change to the output directory and start a simple HTTP server
cd "$OUTPUT" && python3 -m http.server "$PORT"
