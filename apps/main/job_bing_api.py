#background scheduler to scrape bing

#include libs
import sys
sys.path.insert(0, '..')
from include import *


job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

def job():
    os.chdir('../scraper/')
    os.system('python3 bing_api.py')

if __name__ == '__main__':
    scheduler = BackgroundScheduler(job_defaults=job_defaults)
    scheduler.add_job(job, 'interval', seconds=60)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
