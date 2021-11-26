#!/bin/bash

function list_include_item {
    local list="$1"
    local item="$2"
    if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]]; then
        result=0
    else
        result=1
    fi
    return $result
}

TALON_DIR="${HOME}/.talon/user"

SCRIPT="${BASH_SOURCE[0]}"
SCRIPT_DIR="$( cd -- "$( dirname -- "${SCRIPT}" )" &> /dev/null && pwd )"

function talon_link {
    local SOURCES_TO_LINK="$1"
    for source in ${SOURCES_TO_LINK}; do
        mkdir -p "${TALON_DIR}/$(dirname ${source})"
        ln -s "${SCRIPT_DIR}/${source}" "${TALON_DIR}/${source}"
    done
}

function talon_unlink {
    local SOURCES_TO_UNLINK="$1"
    for source in ${SOURCES_TO_UNLINK}; do
        unlink "${TALON_DIR}/${source}"
    done
}

# Local source files
SOURCES="$(find "${SCRIPT_DIR}" -mindepth 1 \( -name '*.py' -o -name '*.talon' -o -name '*.csv' \) ! -path '*/\.*' -printf '%P\n')"

SOURCES_RELATIVE=""
for source in ${SOURCES}; do
    SOURCES_RELATIVE="${SOURCES_RELATIVE}"$'\n'"./${source}"
done

# Test if local source file is currently linked to the Talon user directory
function is_linked {
    local source="$1"
    [ -L "${TALON_DIR}/${source}" ]
}

# Script to select currently linked source files in PathPicker
EXECUTE_KEYS=""
for source in ${SOURCES}; do
    if is_linked "${source}"; then
        EXECUTE_KEYS="${EXECUTE_KEYS} f"
    fi
    EXECUTE_KEYS="${EXECUTE_KEYS} j"
done
EXECUTE_KEYS="${EXECUTE_KEYS} HOME"

# Local source files selected in PathPicker
SOURCES_SELECTED="$@"

# Test if local source file is included in the user selection
function is_selected {
    local source="$1"
    list_include_item "${SOURCES_SELECTED}" "./${source}"
}

# ./setup.sh -- Display TUI
if [ "$#" -eq 0 ]; then
    fpp --clean 2>&1 1>/dev/null
    echo "${SOURCES_RELATIVE}" | fpp -nfc -ni -ai -c "${SCRIPT}" -e ${EXECUTE_KEYS}
fi

# ./setup.sh [PATH..] -- Update Talon user
if [ "$#" -gt 0 ]; then

    # Compute updates
    SOURCES_TO_LINK=""
    SOURCES_TO_UNLINK=""
    for source in ${SOURCES}; do
        if is_selected "${source}" && ! is_linked "${source}"; then
            SOURCES_TO_LINK="${SOURCES_TO_LINK}"$'\n'"${source}"
        fi
        if ! is_selected "${source}" && is_linked "${source}"; then
            SOURCES_TO_UNLINK="${SOURCES_TO_UNLINK}"$'\n'"${source}"
        fi
    done

    # Link the selected local files
    if [ ! "$SOURCES_TO_LINK" == "" ]; then
        echo "${SCRIPT} is about to link the following files to ${TALON_DIR}:"
        for source in ${SOURCES_TO_LINK}; do
            echo "- ${source}"
        done
        read -p "Are you sure? [y/N]" -n 1 -r
        echo # move to a new line
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            talon_link "${SOURCES_TO_LINK}"
        fi
    fi

    # Unlink the deselected local files
    if [ ! "$SOURCES_TO_UNLINK" == "" ]; then
        echo "${SCRIPT} is about to unlink the following files from ${TALON_DIR}:"
        for source in ${SOURCES_TO_UNLINK}; do
            echo "- ${source}"
        done
        read -p "Are you sure? [y/N]" -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            talon_unlink "${SOURCES_TO_UNLINK}"
        fi
    fi
fi
