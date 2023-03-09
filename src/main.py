import requests
from lxml import html


if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    result = requests.get(url)
    tree = html.fromstring(result.content)

    index = []

    ulA = tree.xpath('//*[@id="mw-content-text"]/div[1]/div[2]/ul')

    counter = 1
    for li in ulA[0]:
        inner_url = url + li[0].get('href')
        result = requests.get(inner_url)
        filename = f'site_{counter}.html'
        with open('../data/' + filename, 'wb') as f:
            f.write(result.content)
            counter += 1
            index.append(f'{filename} - {inner_url}')

    ulC = tree.xpath('//*[@id="mw-content-text"]/div[1]/div[4]/ul')

    for li in ulC[0]:
        inner_url = url + li[0].get('href')
        result = requests.get(inner_url)
        filename = f'../data/site_{counter}.html'
        with open(filename, 'wb') as f:
            f.write(result.content)
            counter += 1
            index.append(f'{filename} - {inner_url}')

    with open('index.txt', 'w') as f:
        for line in index:
            f.write(line + '\n')
