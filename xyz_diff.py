#!/usr/bin/env python3

from typing import List
from typing import Tuple

import argparse
import os
import logging
import sys


def formatRGB(rgb: Tuple[float, float, float]):
    """Create an ANSI escape sequence for the given RGB color as foreground"""

    intRGB = [round(i*255) for i in rgb]

    # Convert to ANSI escape sequences
    outstr = "\x1b[38;2;" + str(intRGB[0]) + ";" + str(rgb[1]) + ";" + str(intRGB[2]) + "m"

    return outstr


def printColor(msg, rgb=(0, 0, 0), end="\n"):
    """Print the given message with the given foreground color"""

    print(formatRGB(rgb) + msg + "\x1b[0;0m", end=end)


def parseXYZ(string: str) -> List[Tuple[str, List[float]]]:
    """Parses the given string as an XYZ specification"""
    lines = string.strip().split("\n")

    if len(lines) in [0, 1, 2]:
        raise RuntimeError(
            "Invalid XYZ format encountered - insufficient lines (%d)" % len(lines))

    nAtoms = int(lines[0])
    lines = lines[2:]

    if len(lines) != nAtoms:
        raise RuntimeError(
            "Atom count specified in header (%d) is inconsistent with actual atom count (%d)" % (nAtoms, len(lines)))

    xyz = []

    for currentLine in lines:
        parts = currentLine.split()

        if len(parts) != 4:
            raise RuntimeError(
                "Encountered line with invalid amount of columns (%d instead of 4)" % len(parts))

        element = parts[0]
        xCoord = float(parts[1])
        yCoord = float(parts[2])
        zCoord = float(parts[3])

        xyz.append((element, [xCoord, yCoord, zCoord]))

    return xyz


def readXYZ(fileName: str) -> List[Tuple[str, List[float]]]:
    """Opens and reads the file at the given path and then parses its content as
    an XYZ file."""
    with open(fileName, "r") as inputFile:
        content = inputFile.read()

        return parseXYZ(content)


def xyzDiff(lhs: List[Tuple[str, List[float]]], rhs: List[Tuple[str, List[float]]]) -> List[Tuple[str, List[float]]]:
    """Computes the difference of two XYZ objects"""
    nAtoms = min(len(lhs), len(rhs))

    if len(lhs) != len(rhs):
        logging.warning("Comparing molecules of different size (%d and %d atoms) - only comparing first %d entries" %
                        (len(lhs), len(rhs), nAtoms))

    diff = []

    for i in range(0, nAtoms):
        lhsElement, lhsCoords = lhs[i]
        rhsElement, rhsCoords = rhs[i]

        if lhsElement != rhsElement:
            diffElement = lhsElement + " -> " + rhsElement
        else:
            diffElement = lhsElement
        diffElement = "{:8}".format(diffElement)

        assert len(lhsCoords) == 3
        assert len(rhsCoords) == 3

        diffCoords = []
        for j in range(0, 3):
            diffCoords.append(rhsCoords[j] - lhsCoords[j])

        diff.append((diffElement, diffCoords))

    return diff


def getRGB(value: float, maxValue: float, fromRGB: Tuple[float, float, float] = (0, 0, 0), toRGB: Tuple[float, float, float] = (0, 0, 0)) -> Tuple[float, float, float]:
    """Interpolate between the given RGB values such that 0 has fromRGB and maxValue has toRGB.
    Note that value and maxValue are expected to have the same sign."""
    fraction = value / maxValue if abs(maxValue) > 1E-8 else 0

    return tuple(x + fraction * (y - x) for x, y in zip(fromRGB, toRGB))


def printDiff(diff: List[Tuple[str, List[float]]], colorCode=True):
    """Print the given XYZ difference to the console (potentially color-coded"""
    maxDiff = 0
    for _, coords in diff:
        maxDiff = max(maxDiff, abs(max(coords, key=abs)))

    for element, coords in diff:
        assert len(coords) == 3
        def printFunc(msg, value, maxValue):
            if colorCode:
                printColor(msg, rgb=getRGB(abs(value), maxValue, fromRGB=(0.4, 0.4, 0.4), toRGB=(1, 0.2, 0.2)), end="  ")
            else:
                print(msg, end="  ")

        print(element, end=" ")
        for i in range(3):
            printFunc("{:+12.8f}".format(coords[i]), coords[i], maxDiff)

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Compares two molecular structures in XYZ format")
    parser.add_argument("xyz_file", nargs=2)
    parser.add_argument("--monochrome", default=False, action="store_true", help="Use monochrome output (no colors)")

    args = parser.parse_args()

    # Check that files exist
    for current in args.xyz_file:
        if not os.path.isfile(current):
            logging.error(
                "File \"%s\" does not exist or is not a file!" % current)
            sys.exit(1)
        if not current.endswith(".xyz"):
            logging.warning(
                "File \"%s\" does not have the expected .xyz file extension" % current)

    # Read XYZ files
    lhs = readXYZ(args.xyz_file[0])
    rhs = readXYZ(args.xyz_file[1])

    # Calculate difference
    diff = xyzDiff(lhs, rhs)

    # Pretty-print diff
    printDiff(diff, colorCode=not args.monochrome)


if __name__ == "__main__":
    main()
