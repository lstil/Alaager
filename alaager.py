import requests
from bs4 import BeautifulSoup
import threading

class alaa(object):
    def __init__(self):
        self.url = 'https://alaatv.com/set/{}'
        self.result = {"720p": [], "480p": [], "240p": []}

    def request(self, url):
        return requests.get(url, headers={'User-agent': 'Mozilla/5.0'})

    def soup(self, url):
        return BeautifulSoup(self.request(url).text, "html.parser")

    def grabUrl(self):
        links = []
        try:
            divs = self.soup(self.url.format(self.course)) \
                .findAll("div", class_="m-widget5__item")

            for div in divs:
                links.append(div.find("a")['href'])

            return links
        except:
            raise Exception("No internet access")

    def grabDl(self, links):
        for link in links:
            while True:
                try:
                    t = self.soup(link).find("div", class_="col-md-4 text-justify")
                    break
                except:
                    continue

            for url in t.findAll("a", class_="m-link"):
                url = url['href']
                if "hq" in url:
                    self.result['480p'].append(url)
                elif "240p" in url:
                    self.result['240p'].append(url)
                else:
                    self.result['720p'].append(url)

        return

    def split(self, _data, parts):
        data = list(_data)

        if parts > len(data):
            return data

        subcount = int((len(data) -
                        (len(data) % parts)) / parts)
        result = []
        for part in range(parts - 1):
            sublist = []
            for i in range(subcount):
                item = data[0]
                sublist.append(item)
                data.remove(item)

            result.append(sublist)

        if len(data) != 0:
            result.append(data)

        return result

    def grabber(self, course, thread=5):
        while True:
            try:
                if self.request(self.url.format(course)).status_code != 200:
                    return
            except:
                return

            self.course = course
            links = self.grabUrl()
            
            if thread > 1:
                result = self.split(links, thread)
                threads = []
                for i in range(thread):
                    t = threading.Thread(target=self.grabDl, args=[result[i]])
                    threads.append(t), t.start()

                for thread_ in threads:
                    thread_.join()

            else:
                self.grabDl(links)

            if len(self.result['720p']) == len(links):
                tmp, self.request = self.result, {"720p": [], "480p": [], "240p": []}
                return tmp
            else:
                continue



while True:
    obj = alaa()
    try:
        in_ = int(input("\n\n>> Enter course number: "))
        print(">> Grabbing information...")
        res = obj.grabber(in_)
        if res == None:
            print(">> Nothing found")

        else:
            print(">> Course has been detected")
            while True:
                iz_ = int(input(">> Choose quality (1. 240p  2. 480p  3. 720p): "))
                if iz_ in [1,2,3]:
                    break

            print("\n\n"), print("_"*10, "DOWNLOAD LINK", "_"*10, "\n\n")
            link_ = ""
            if iz_ == 1:
                for link in sorted(res['240p']):
                    link_ += link + "\n"
                    print("\t", link)
            elif iz_ == 2:
                for link in sorted(res['480p']):
                    link_ += link + "\n"
                    print("\t", link)
            else:
                for link in sorted(res['720p']):
                    link_ += link + "\n"
                    print("\t", link)

            with open("dl.txt", "w") as f:
                f.write(link_)
                f.close()
                    
            print("\n\n"), print("_"*10, "DOWNLOAD LINK", "_"*10)
            
    except:
        continue


    
