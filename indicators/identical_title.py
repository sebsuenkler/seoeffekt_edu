#script to check the use of https

#include libs
import sys
sys.path.insert(0, '..')
from include import *

def identical_title(hash, result_main):
    print("identical_title")

    def check_identical_title(hash, result_main):

        def check_title(tree):


            title = ""

            xpath_title = "//title/text()"
            xpath_meta_title = "//meta[@name='title']/@content"
            xpath_og_title = "//meta[@property='og:title']/@content"

            check_title = str(tree.xpath(xpath_title))
            check_meta_title = str(tree.xpath(xpath_meta_title))
            check_og_title = str(tree.xpath(xpath_og_title))

            if len(check_title) > 4 or len(check_meta_title) > 4  or len(check_og_title) > 4:
                if len(check_og_title) > 4:
                    title = check_og_title
                elif len(check_meta_title) > 4:
                    title = check_meta_title
                else:
                    title = check_title


                title = title.replace("'", "")
                title = title.replace('"', "")
                title = title.replace(':', "")
                title = title.replace(',', "")

                title = title.strip()

                print(title)


            return title


        results_urls = str(Sources.getSourcesURLs(hash))

        list_results_urls = list(results_urls.split("[url]"))

        list_results_urls = list(dict.fromkeys(list_results_urls))

        results_links = []

        if len(list_results_urls) > 20:
            list_results_urls = list_results_urls[:20]

        for l in list_results_urls:
            url_split = l.split("   ")
            if len(url_split) == 2:
                try:
                    if result_main in url_split[1]:
                        if not Helpers.matchText(url_split[1], '*javascript*') and not Helpers.matchText(url_split[1], '*None*') and url_split[1] != result_main and Helpers.validate_url(url_split[1]):
                            results_links.append(url_split[1])
                except:
                    pass




        results_links = list(dict.fromkeys(results_links))

        number_of_links = 3
        n = 0

        if len(results_links) < number_of_links:
            number_of_links = len(results_links)

        results_source = Results.getResultsSource(hash)
        code = Helpers.html_unescape(results_source[0][0])
        code = code.lower()
        tree = html.fromstring(code)

        title = check_title(tree)

        identical_title_num = 0


        while n < number_of_links:

            url_to_check = results_links[n]

            print(url_to_check)

            n+=1
            try:
                source = Results.saveResult(url_to_check)
                if source != 'error':
                    code = source.lower()
                    tree = html.fromstring(code)
                    link_title = check_title(tree)
                    if title == link_title:
                        identical_title_num = 1
                        number_of_links = 3
                else:
                    number_of_links += 1


            except:
                number_of_links += 1

        if identical_title_num > 0:
            value = '1'
        else:
            value = '0'

        return value


    module = "check identical title"
    value = check_identical_title(hash, result_main)
    print("identical:")
    print(value)
    check_evaluations_result(hash, module, value)
