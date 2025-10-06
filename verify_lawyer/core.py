"""
Core functionality for lawyer verification and search
"""

import asyncio
import json
import os
import logging
from browser_use import Browser

# Suppress all browser-use logging
os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'CRITICAL'
logging.getLogger('browser_use').setLevel(logging.CRITICAL)
logging.getLogger('cdp_use').setLevel(logging.CRITICAL)
logging.getLogger('bubus').setLevel(logging.CRITICAL)
logging.getLogger('BrowserSession').setLevel(logging.CRITICAL)


async def search_lawyers(
    name: str = None,
    sicil: str = None,
    surname: str = None,
    baro_id: str = "0",
    tip: str = "Avukat",
    verbose: bool = True
):
    """
    Search for lawyers and return all matching results

    Args:
        name: First name
        sicil: Registration number
        surname: Last name
        baro_id: Bar Association ID (0=all, 34=Istanbul, 6=Ankara, 35=Izmir)
        tip: Type ("Avukat" or "Stajyer")
        verbose: Print progress messages

    Returns:
        dict: {'count': int, 'results': [{'baro': str, 'sicil': str, 'ad': str, 'soyad': str}]}
    """
    # Parse name if surname not provided
    if name and not surname and ' ' in name:
        parts = name.rsplit(' ', 1)
        name = parts[0]
        surname = parts[1]

    browser = Browser(
        headless=False,
        window_size={'width': 1, 'height': 1},
        args=['--window-position=-2400,-2400']
    )

    try:
        await browser.start()

        if verbose:
            print("🔍 Searching...")

        page = await browser.new_page("https://www.barobirlik.org.tr/AvukatArama")
        await asyncio.sleep(5)

        await page.evaluate(f'''() => {{
            document.querySelector('input[name="ad"]').value = "{name if name else ''}";
            document.querySelector('input[name="soyad"]').value = "{surname if surname else ''}";
            document.querySelector('input[name="barosicil"]').value = "{sicil if sicil else ''}";
            document.querySelector('select[name="baroId"]').value = "{baro_id}";
            document.querySelector('button[type="submit"][name="tip"][value="{tip}"]').click();
        }}''')

        await asyncio.sleep(3)

        result = await page.evaluate('''() => {
            var table = document.querySelector('table.table-bordered');
            if (!table) return JSON.stringify({count: 0, results: []});
            var tbody = table.querySelector('tbody');
            if (!tbody) return JSON.stringify({count: 0, results: []});
            var rows = tbody.querySelectorAll('tr');
            if (rows.length === 0) return JSON.stringify({count: 0, results: []});

            var results = [];
            for (var i = 0; i < rows.length; i++) {
                var cells = rows[i].querySelectorAll('td');
                if (cells.length >= 5) {
                    results.push({
                        baro: cells[1].textContent.trim(),
                        sicil: cells[2].textContent.trim(),
                        ad: cells[3].textContent.trim(),
                        soyad: cells[4].textContent.trim()
                    });
                }
            }
            return JSON.stringify({count: results.length, results: results});
        }''')

        return json.loads(result)

    except Exception:
        return {'count': 0, 'results': []}

    finally:
        await browser.stop()


async def verify_lawyer(
    name: str,
    sicil: str = None,
    surname: str = None,
    baro_id: str = "34",
    tip: str = "Avukat",
    verbose: bool = True
):
    """
    Verify if a specific lawyer exists

    Args:
        name: First name or full name
        sicil: Registration number
        surname: Last name
        baro_id: Bar Association ID (default: 34 for Istanbul)
        tip: Type ("Avukat" or "Stajyer")
        verbose: Print progress messages

    Returns:
        dict: {'exists': bool, 'baro': str, 'sicil': str, 'ad': str, 'soyad': str} or {'exists': False}
    """
    results = await search_lawyers(
        name=name,
        sicil=sicil,
        surname=surname,
        baro_id=baro_id,
        tip=tip,
        verbose=verbose
    )

    if results['count'] > 0:
        first = results['results'][0]
        return {
            'exists': True,
            'baro': first['baro'],
            'sicil': first['sicil'],
            'ad': first['ad'],
            'soyad': first['soyad']
        }

    return {'exists': False}
