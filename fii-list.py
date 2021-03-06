#!/usr/bin/env python3
import re
import csv
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal
from datetime import date


def scrap_page(*args, **kwargs):
    url = 'https://fundamentus.com.br/fii_resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca dos FIIs
    # Estão em branco para que retorne todas as disponíveis
    data = {'ffo_y_min': '',
            'ffo_y_max': '',
            'divy_min': '',
            'divy_max': '',
            'pvp_min': '',
            'pvp_max': '',
            'mk_cap_min': '',
            'mk_cap_max': '',
            'qtd_imoveis_min': '',
            'qtd_imoveis_max': '',
            'preco_m2_min': '',
            'preco_m2_max': '',
            'aluguel_m2_min': '',
            'aluguel_m2_max': '',
            'cap_rate_min': '',
            'cap_rate_max': '',
            'vacancia_min': '',
            'vacancia_max': '',
            'setor': '',
            'negociada': 'ON',
            }

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="tabelaResultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]

    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'Segmento': rows.getchildren()[1].text,
                                                                        'Cotacao': todecimal(rows.getchildren()[2].text),
                                                                        'FFO.Yield': todecimal(rows.getchildren()[3].text),
                                                                        'Dividend.Yield': todecimal(rows.getchildren()[4].text),
                                                                        'P/VP': todecimal(rows.getchildren()[5].text),
                                                                        'Valor.de.Mercado': todecimal(rows.getchildren()[6].text),
                                                                        'Liquidez': todecimal(rows.getchildren()[7].text),
                                                                        'Qtd.de.imoveis': todecimal(rows.getchildren()[8].text),
                                                                        'Preço.do.m2': todecimal(rows.getchildren()[9].text),
                                                                        'Aluguel.por.m2': todecimal(rows.getchildren()[10].text),
                                                                        'Cap.Rate': todecimal(rows.getchildren()[11].text),
                                                                        'Vacancia.Media': todecimal(rows.getchildren()[12].text),
                                                                        'Media.Dividendo': todecimal(rows.getchildren()[2].text) * (todecimal(rows.getchildren()[4].text)/12),
                                                                        }})

    return result


def filter_list(fii_list, filter_by, filter_gth, filter_lth):
    filtered_list = {}
    for key, value in fii_list.items():
        if filter_gth > 0 and filter_lth > 0:
            if value.get(filter_by) >= filter_gth and value.get(filter_by) <= filter_lth:
                filtered_list[key] = value
        elif filter_gth > 0:
            if value.get(filter_by) >= filter_gth:
                filtered_list[key] = value
        else:
            if value.get(filter_by) <= filter_lth:
                filtered_list[key] = value

    return filtered_list


def fii_list_by_primo_rico():
    scrap_result = scrap_page()
    filtered_list = {}

    filtered_list = filter_list(scrap_result, "Dividend.Yield", 0.04, 0)
    filtered_list = filter_list(filtered_list, "P/VP", 0.04, 1.20)
    filtered_list = filter_list(
        filtered_list, "Valor.de.Mercado", 500000000, 0)
    filtered_list = filter_list(filtered_list, "Vacancia.Media", 0, 0.30)
    filtered_list = filter_list(filtered_list, "Liquidez", 1000000, 0)

    output = OrderedDict(sorted(filtered_list.items(
    ), key=lambda t: t[1].get("Cotacao"), reverse=True))

    return output


def todecimal(string):
    string = string.replace('.', '')
    string = string.replace(',', '.')

    if (string.endswith('%')):
        string = string[:-1]
        return Decimal(string) / 100
    else:
        return Decimal(string)


def format_name():
    today = date.today().strftime("%d-%m-%Y")
    return f"fii_list_by_primo_rico{today}.csv"


def to_csv(result):
    with open(format_name(), mode='w') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([
            'Posição',
            'Papel',
            'Segmento',
            'Cotacao',
            'FFO.Yield',
            'Dividend.Yield',
            'P/VP',
            'Valor.de.Mercado',
            'Liquidez',
            'Qtd.de.imoveis',
            'Preço.do.m2',
            'Aluguel.por.m2',
            'Cap.Rate',
            'Vacancia.Media',
            'Media.Dividendo'
        ])

        index = 1
        for key, value in result.items():
            writer.writerow([
                index,
                key,
                value['Segmento'],
                value['Cotacao'],
                value['FFO.Yield'],
                value['Dividend.Yield'],
                value['P/VP'],
                value['Valor.de.Mercado'],
                value['Liquidez'],
                value['Qtd.de.imoveis'],
                value['Preço.do.m2'],
                value['Aluguel.por.m2'],
                value['Cap.Rate'],
                value['Vacancia.Media'],
                value['Media.Dividendo'],
            ])
            index = index + 1


if __name__ == '__main__':
    print('[*] Search FII and download')

    result = fii_list_by_primo_rico()

    print('[*] Download completed')

    to_csv(result)
