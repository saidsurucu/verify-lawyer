#!/usr/bin/env python3
"""
Command-line interface for lawyer verification
"""

import sys
import argparse
import asyncio
import os

# Completely disable all logging before importing anything
os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'CRITICAL'
os.environ['PYTHONWARNINGS'] = 'ignore'

# Monkey-patch logging to do nothing
import logging
logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.CRITICAL, handlers=[])

# Create null handler
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# Apply to all loggers
for logger_name in ['browser_use', 'cdp_use', 'bubus', 'BrowserSession', 'playwright', 'cdp_use.client']:
    logger = logging.getLogger(logger_name)
    logger.disabled = True
    logger.setLevel(logging.CRITICAL)
    logger.handlers = [NullHandler()]
    logger.propagate = False

from .core import search_lawyers, verify_lawyer


def main():
    parser = argparse.ArgumentParser(
        description='Search or verify lawyers in Turkish Bar Association'
    )
    parser.add_argument(
        'name',
        nargs='?',
        help='Lawyer name (can be "Name Surname" or just name)'
    )
    parser.add_argument(
        '-s', '--sicil',
        help='Registration number'
    )
    parser.add_argument(
        '-l', '--lastname',
        help='Last name (if not included in name)'
    )
    parser.add_argument(
        '-b', '--baro',
        default='34',
        help='Bar ID (default: 34 for Istanbul, 0 for all)'
    )
    parser.add_argument(
        '-t', '--type',
        choices=['avukat', 'stajyer'],
        default='avukat',
        help='Search type: avukat (lawyer) or stajyer (trainee)'
    )
    parser.add_argument(
        '--search',
        action='store_true',
        help='Search mode: return all matching results'
    )

    args = parser.parse_args()

    tip = "Stajyer" if args.type.lower() == "stajyer" else "Avukat"

    if args.search:
        result = asyncio.run(search_lawyers(
            name=args.name,
            sicil=args.sicil,
            surname=args.lastname,
            baro_id=args.baro,
            tip=tip,
            verbose=False
        ))

        if result['count'] > 0:
            print(f"✅ {result['count']} sonuç bulundu:\n")
            for i, lawyer in enumerate(result['results'], 1):
                print(f"{i}. {lawyer['ad']} {lawyer['soyad']}")
                print(f"   {lawyer['baro']} - Sicil: {lawyer['sicil']}")
                print()
            sys.exit(0)
        else:
            print("❌ Sonuç bulunamadı")
            sys.exit(1)
    else:
        if not args.name:
            print("❌ Error: name is required for verification mode")
            sys.exit(1)

        result = asyncio.run(verify_lawyer(
            name=args.name,
            sicil=args.sicil,
            surname=args.lastname,
            baro_id=args.baro,
            tip=tip,
            verbose=False
        ))

        if result['exists']:
            print("✅ VAR")
            print(f"   {result['ad']} {result['soyad']}")
            print(f"   {result['baro']} - {result['sicil']}")
        else:
            print("❌ YOK")

        sys.exit(0 if result['exists'] else 1)


if __name__ == "__main__":
    main()
