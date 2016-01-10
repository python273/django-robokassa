from xml.dom import minidom
import urllib

from .conf import LOGIN


# robokassa api is s*it

def get_xml(url, params):
    urlencoded = urllib.urlencode(params)
    f = urllib.urlopen(url + '?' + urlencoded)
    return minidom.parseString(f.read())


def get_currencies():
    url = 'https://auth.robokassa.ru/Merchant/WebService/Service.asmx/GetCurrencies'
    values = {
        'MerchantLogin': LOGIN,
        'Language': 'ru'
    }
    response = get_xml(url, values)
    global response
    groups_dom = response.getElementsByTagName('Groups')[0].getElementsByTagName('Group')

    currencies = []

    for group_dom in groups_dom:
        currencies += [[
            'group',
            group_dom.getAttribute('Code'),
            group_dom.getAttribute('Description')
        ]]
        currencies_dom = group_dom.getElementsByTagName('Currency')

        for node in currencies_dom:
            label = node.getAttribute('Label')
            name = node.getAttribute('Name')
            currencies += [['currency', label, name]]

    return currencies


def calc_out_summ(currency, summ):
    url = 'https://auth.robokassa.ru/Merchant/WebService/Service.asmx/CalcOutSumm'
    values = {
        'MerchantLogin': LOGIN,
        'IncCurrLabel': currency,
        'IncSum': summ
    }
    response = get_xml(url, values)
    out_summ = response.getElementsByTagName('OutSum')[0].firstChild.nodeValue
    return out_summ

if __name__ == '__main__':
    print(calc_out_summ('TerminalsElecsnetOceanR', 100))
