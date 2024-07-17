### Manual for the tool
#### Installation
```
git clone https://github.com/searchstudies/seoeffekt_edu
```

Virtual environment (optional):
```
python3 -m venv seoeffekt_edu
source seoeffekt_edu/bin/activate
```

Installation of the packages:
```
pip install -r requirements.txt
```
Or if you have problems with the installation of the requirements.txt, consider to install them manually:
```
pip install --upgrade pip
pip install pip-review
pip-review --local --auto
pip install wheel
pip install setuptools
pip install psutil
pip install apscheduler
pip install pandas
pip install beautifulsoup4
pip install lxml
pip install seleniumbase
```

Available Scrapers:
- Google_de: Scraper to collect search results from the German version Google
- Bing_de: Scraper to collect search results from the German verson of Bing
- Google_de_Top10: Scraper to collect the top-10 search results from the German version Google
- Bing_de_Top10: Scraper to collect the top-10 search results from the German verson of Bing

#### Usage
- RUN /install/python install_sqlite.py : to install the database
- Create a csv file (e.g. queries.csv) with search queries (one per row)
- RUN python insert_study.py : to create a new study (type yes to scrape results and select which search engines you want to include)
- RUN python start.py or RUN nohup python start.py & : to run a BackgroundScheduler starting the threads to scrape and classify results; check the tool.log for progress
- RUN python check_status.py : to see if the tool is done
- RUN python export_results.py : export classified search results from the database
- RUN python stop.py : you can stop the tool at any point and restrat it with python start.py

#### We also suggest to run the tool on a server in the background:
An good to way to do it, is running the tool via 
```
nohup python start.py >start.out &
```

### Der Effekt der Suchmaschinenoptimierung auf die Suchergebnisse von Web-Suchmaschinen: Modellentwicklung, empirische Überprüfung und Triangulation mit Nutzer/innen- und Expert/inneneinschätzungen (SEO-Effekt)

The overall goal of the project is to describe and explain the role of search engine optimization from the perspective of the participating stakeholder groups by analysing search results/search result pages for optimized content as well as quantitative and qualitative surveys of search engine users, search engine optimizers and content providers. Thus the external influence on the results of commercial search engines can be described and quantified for the first time. The project contributes to theory building in information science by extending existing information-seeking models by a component of external influence on the search results.

The project focuses on informative content; it examines how documents that play a role in answering information-oriented search queries can be influenced externally. This sets the project apart from pure questions of online marketing, where the focus is on the optimization itself and not on the consequences for the compilation of result sets.

To measure the effect of search engine optimization, a software will be developed that can automatically query search engines and analyze the returned results. The results of the search result analyses carried out using it are combined with findings from the survey and further investigations of search engine users, search engine optimisers and content providers in order to obtain a comprehensive picture of the influence of search engine optimisation. Methodologically, the project is characterized by a triangulation of methods of data analysis from computer science and social science methods. The interdisciplinary basis of the analysis is unique and will significantly advance the understanding of search engines in general and the influence search engine optimization has in particular.

With search engine optimization, the project addresses a highly relevant topic for information seeking in society, which to a considerable extent takes place via commercial search engines. The expected empirical and theoretical results contribute to a better understanding of information seeking in the context of modern web infrastructures. At the level of transfer into practice, the results will be relevant to issues like consumer protection.

Funding period: 05/2019 bis 07/2021

Funded by: German Research Foundation (DFG – Deutsche Forschungsgemeinschaft), grant number 417552432.

Contacts: [SearchStudies](https://searchstudies.org)

For more information about the implemented SEO-Classifier: [SEO-Effekt - Development and software implementation of a preliminary model to identify the probability of search engine optimization on webpages](https://osf.io/vzehn/)

Research data: [OSF](https://osf.io/jyv9r/)
