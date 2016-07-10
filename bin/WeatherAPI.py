#coding=utf-8

'''i don't know'''

import re
import os
import json
import pprint
import logging
import logging.config
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
	
#os.chdir(r"C:\Users\liyunliang\Desktop")
logging.config.fileConfig('../conf/logconfig.ini')
	
class Weather(object):
    HTML1, HTML2 = range(2)
    def __init__(self, city=u"海淀"):
        self.city_id = 101010200
            
    def get_all_cityname(self):
        return u"海淀".encode('utf-8')
            
    def _get_html(self, idx):
        base_urls = [u"http://www.weather.com.cn/weather1d/%s.shtml"\
                 , u"http://www.weather.com.cn/weather/%s.shtml"]
        base_url = base_urls[idx]
        url = base_url%self.city_id
        html = urlopen(url)
        if html is None:
                raise RuntimeError('html is not found')
        return html
            
    def _parse_html(self):
        try:
            html = self._get_html(self.HTML1)
        except (HTTPError, RuntimeError) as e:
            logging.error(" get html error : {}".format(e))
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        hour3data, hour24data = None, None
        # get hour3 & hour24 data, format:json
        for item in bsObj.findAll('script'):
            item = item.get_text().strip()
            if item.startswith('var hour3data'):
                hour3data = item[14:]
                try:
                    hour3data = json.loads(hour3data)
                except json.decoder.JSONDecodeError as e:
                    logging.error(" hour3data json decode error : {}".format(e))
            elif item.startswith('var observe24h_data'):
                hour24data = item[22:-1]
                try:
                    hour24data = json.loads(hour24data)
                except json.decoder.JSONDecodeError as e:
                    logging.error('hour24data json decode error : {}'.format(e))
        # get index of living
        lifeindex = {}
        array = ['UV', 'ColdRate', 'Dress', 'CarWash', 'Sport', 'AirPollution']
        subarray = ['level', 'name', 'info']
        indexarray = ['span', 'em', 'p']		
        for index, item in enumerate(bsObj.findAll('li', {'class':re.compile(r'^hot$')})):
            name = array[index]
            lifeindex[name] = {}
            for subindex, subname in enumerate(subarray):
                tmp_data = None
                tagname = indexarray[subindex]
                try:
                    tmp_data = getattr(item, tagname).get_text()
                except AttributeError as e:
                    logging.error(' lifeindex name:{} subname:{} tagname:{} error:{}'\
                                  .format(name, subname, tagname, e))
                lifeindex[name][subname] = tmp_data
        lifeindex = json.dumps(lifeindex)
        # get day7 weather
        try:
            html = self._get_html(self.HTML2)
        except (HTTPError, RuntimeError) as e:
            logging.error(' get html error : {}'.format(e))
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        day7data = {}
        array = ['day','dpng','npng','wea','tmph','tmpl','win']
        for tagObj in bsObj.find('ul', {'class':'t clearfix'}).findAll('li'):
            try:
                day7data[array[0]] = tagObj.h1.get_text()
            except AttributeError as e:
                logging.error(' day7: {} parser error : {}'.format(array[0], e))
                day7data[array[0]] = None
            for index, subtag in enumerate(tagObj.findAll('big')):
                day7data[array[1:3][index]] = subtag['class']
            day7data[array[3]] = tagObj.find(class_='wea').get_text()
            subtag = tagObj.find(class_='tem')
            try:
                day7data[array[4]] = subtag.span.get_text()
            except AttributeError as e:
                logging.error(' day7: {} parser error : {}'.format(array[4], e))
            try:
                day7data[array[5]] = subtag.i.get_text()
            except AttributeError as e:
                logging.error(' day7: {} parser error : {}'.format(array[5], e))
            try:
                day7data[array[6]] = tagObj.find(class_='win').i.get_text()
            except AttributeError as e:
                logging.error(' day7: {} parser error : {}'.format(array[6], e))
        day7data = json.dumps(day7data)
        #pprint.pprint(day7data)
        return(hour3data, hour24data, day7data, lifeindex)
	
    def weather(self):
        (hour3data, hour24data, day7data, lifeindex) = self._parse_html()


def main():
    w = Weather()
    w._parse_html()

		
if __name__ == '__main__':
    main()
