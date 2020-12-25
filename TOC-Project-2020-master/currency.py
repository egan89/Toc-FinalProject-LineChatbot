import requests
r = requests.get('https://tw.rter.info/capi.php')
currency = r.json()


m = ['USD', 'EUR', 'JPY', 'HKD', 'GBP', 'CHF', 'CNY', 'CNH', 'KRW', 'AUD', 'NZD', 'SGD', 'THB', 'SEK', 'MYR', 'CAD', 'VND', 'MOP', 'PHP', 'INR', 'IDR', 'DKK', 'ZAR', 'MXN', 'TRY', 'TWD', 'BTC', 'LTC', 'DOGE', 'GOLD1OZ', 'SLIVER1OZ999NY', 'PLATINUM1UZ999', 'PALLADIUM1OZ', 'COPPERHIGHGRADE']

def separate(str):
    str = str.upper()
    sub = ['NOTHING', 'NOTHING']
    for i in range(0, len(str)):
        if str[i] == ' ':
            sub[0] = str[0:i]
            sub[1] = str[i+1:len(str)]
            break;
    return sub

def ifLegal(str1, str2):
    if (str1 in m) and (str2 in m):
        return True
    return False
    
    
def exRate(c1, c2):
    i = currency['USD' + c1.upper()]['Exrate']
    j = currency['USD' + c2.upper()]['Exrate']
    t = currency['USD' + c2.upper()]['UTC']
    return '1 ' + c1 + ' = ' + str(float(j)/float(i)) + ' ' + c2 + '\nLast Update Time: ' + t + '(UTC)'
    
def exchange(c1, c2, n):
    i = currency['USD' + c1.upper()]['Exrate']
    j = currency['USD' + c2.upper()]['Exrate']
    return str((float(j)/float(i)) * float(n)) + ' ' + c2
  
    


#print(exRate('TWD', 'JPY'))
#print(currency['USDTWD']['UTC'])
#print(currency['USDJPY']['UTC'])
"""
str = 'TWD JPY'
sub1 = ''
sub2 = ''
for i in range(0, len(str)):
    if str[i] == ' ':
        sub1 = str[0:i]
        sub2 = str[i+1:len(str)]
        break;
        
print(sub1)
print(sub2)
"""

