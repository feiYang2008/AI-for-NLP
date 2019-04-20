import requests
from bs4 import BeautifulSoup as BS
import re


class LineCrawler(object):
    """
    scrape the information of Lines
    * Other lines connected to the current line
    * pair of stations connected by the current line
    * distance between adjacent stations
    """
    def __init__(self, url_line):
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.url = url_line
        self.page = requests.get(url_line, headers=headers)
        self.soup = BS(self.page.content, "html.parser")
        self.name = self.soup.h1.text
        self.tables = {table.caption.text: table for table in self.soup.findAll('table', {"log-set-param": 'table_view'}) if table.caption}
        self.host = "https://baike.baidu.com"

        self.next = self.findRelated()
        self.stations = self.findStations()

    def findRelated(self):
        table = None
        for i in self.tables:
            if "号线车站列表" in i:
                if table:
                    table.append(self.tables[i])
                else:
                    table = self.tables[i]
        if not table:
            return table
        links = table.find_all('a', href=re.compile('/item/.+'), text=re.compile('北京地铁[0-9]+号线'))
        for i in links:
            if i.get('href') == self.url:
                continue
            else:
                yield self.host + i.get('href')
        # return [i.get('href') for i in links if i != self.url]

    def findStations(self):
        table = None
        for i in self.tables:
            if "相邻站间距信息统计表" in i:
                if table:
                    table.append(self.tables[i])
                else:
                    table = self.tables[i]
        if not table:
            return table
        table = table.find_all('tr')
        for row in table[1:]:
            yield [i.getText(strip=True) for i in row.find_all()[:2]]
        # return [[row.th.text, row.td.text] for row in table[1:]]

if __name__ == '__main__':
    test = LineCrawler('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%8114%E5%8F%B7%E7%BA%BF')
