#!/usr/bin/python3

import click
import csv
import time
import requests

ONE_MONTH = 30*24*60*60
ONE_YEAR = ONE_MONTH * 12

@click.command()
@click.argument('start', default=(int(time.time()) - ONE_YEAR - ONE_MONTH * 4))
@click.argument('end', default=int(time.time()))
@click.argument('asset', default="0x39aa39c021dfbae8fac545936693ac917d5e7563")
@click.argument('output', default="market_output.csv")
def run(start: int, end: int, asset: str, output: str):
    click.echo(f"Fetching Market Data from Compound")
    url = f"https://api.compound.finance/api/v2/market_history/graph"
    payload = {
        'asset': asset,
        'min_block_timestamp': start,
        'max_block_timestamp': end,
        'num_buckets': 485
    }
    r = requests.get(url, params=payload)
    data = r.json()
    headers = ['supply_rates', 'borrow_rates', 'prices_usd', 'total_supply_history','total_borrows_history']
    cols: List[List[Any]] = [data[h] for h in headers]
    headers = ['block_timestamp'] + headers
    with open(output, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        rows = []
        for i in range(len(cols[0])):
            row = [cols[0][i]['block_timestamp']]
            for j in range(len(cols)):
                row.append(_parse_value(cols[j][i], j))
            rows.append(row)
        csvwriter.writerows(rows)

def _parse_value(data, i) -> str:
    if i == 0 or i == 1:
        return data['rate']
    if i == 2:
        return data['price']['value']
    if i == 3 or i == 4:
        return data['total']['value']


if __name__ == '__main__':
    run()
