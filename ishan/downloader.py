''' Manga downloader for manga freak
    Usage: python mangadownloader.py manga_name (Downloads all images realted to mange chapetr wise)
    Usage: python mangadownloader.py manga_name chapter (Downloads only specified chapter)
    Usage: python mangadownloader.py manga_name chapter_start chapter_end (Downloads all chapters between and including start and end)
    '''

from bs4 import BeautifulSoup
from urlparse import urljoin
import requests, os, urllib, random, time, re, sys

# initialize fixed variables
image_url = "http://mangafreak.com/images/manga/{}/{}/{}.jpg"
base_url = "http://mangafreak.com/"
base_dir = os.getcwd()
user_agents = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36",\
                "Googlebot/2.1"]
image = urllib.URLopener()

# creates and/or returns path to folder with name manga
def folder_creator(folder_path, manga, debug):
    if not os.path.exists(os.path.join(folder_path, manga)):
        os.mkdir(os.path.join(folder_path, manga))
        if debug: print "manga folder created at" + os.path.join(folder_path, manga)
    return os.path.join(folder_path, manga)

# creates and/or returns path to chapter inside folder manga
def chapter_creator(folder_path, chapter, debug):
    if not os.path.exists(os.path.join(folder_path, chapter)):
        os.mkdir(os.path.join(folder_path, chapter))
        if debug: print "chapter folder created at" + os.path.join(folder_path, chapter)
    return os.path.join(folder_path, chapter)

# performs extraction and storage of image data
def chapter_parser(manga, image_manga, chapter, manga_folder, debug):
    chapter_folder = chapter_creator(manga_folder, chapter, debug)
    request_url = urljoin(base_url, manga+"/chapter-"+chapter)
    data = requests.get(request_url)
    soup = BeautifulSoup(data.text, "html5lib")
    total = soup.select("table.full-table tbody tr td div.label")

    if debug: print "downloading images for {} chapter {}".format(manga, chapter)
    for i in range(1, int(total[0].text[3:])+1):
        # changes user agent for each request
        user = random.choice(user_agents)
        image.addheaders = [('User-Agent', user), ('Accept', '*/*')]
        image.version = user
        image.retrieve(image_url.format(image_manga, chapter, i), os.path.join(chapter_folder, str(i)+".jpg"))
        time.sleep(3)
        if debug: print "dowloaded chapter {} image {}".format(chapter, i)

# interprets command line instructions and engages downloader
def manga_parser(arguments):
    manga = arguments[1]
    debug = True
    manga_folder = folder_creator(base_dir, manga, debug)
    image_manga = re.sub(r'-', '_', manga)
    if len(arguments) == 3:
        chapter_parser(manga, image_manga,arguments[2], manga_folder, debug)
    elif len(arguments) == 4:
        for j in range(int(arguments[2]), int(arguments[3])+1):
            chapter_parser(manga, image_manga, str(j), manga_folder, debug)

if __name__ == "__main__":
    manga_parser(sys.argv)