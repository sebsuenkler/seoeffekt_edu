#script to export the results from database

#include libs
import sys
sys.path.insert(0, '..')
from include import *

Evaluations.deleteDuplicates()

#folder to store the interim results
tmp = 'tmp/'



#Calculate the offset

db = DB()

cur = db.cursor

sql = "SELECT count(distinct(results_hash)) from results"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

next = int(round(rows[0][0] / 3))

#Results from classifications table

db = DB()

cur = db.cursor

sql = "SELECT distinct(classifications_classification) from classifications"

cur.execute(sql)

rows = cur.fetchall()
classes = rows

db.DBDisconnect()

db = DB()

cur = db.cursor

csv_header = 'hash'

for c in classes:
    classification = c[0]

    csv_header = csv_header+','+classification


csv_file = 'classifications.csv'

with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0

i = 0

save_res = ""

sql = "SELECT count(classifications_id) from classifications"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

counter = rows[0][0]

counter = int(round(counter+0.5) / next) + 1


for i in range(0, counter):

    db = DB()

    cur = db.cursor

    sql = "SELECT DISTINCT(classifications_hash) from classifications ORDER BY classifications_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    db.DBDisconnect()

    offset = offset + next

    x = 0

    for row in rows:

        x = x + 1

        print(x)

        build_res = ""
        hash = str(row[0])

        classifications_results = ""

        for c in classes:
            classification = c[0]


            result = Evaluations.getClassificationResult(hash, classification)
            if result:
                value = result[0][0]
            else:
                value = ""


            classifications_results += value+','

        classifications_results = classifications_results[:-1]


        build_res = hash+','+classifications_results

        save_res = '\n'+build_res

        with open(tmp+csv_file,'a+') as f:
            f.write(save_res)
        f.close()


#Results from queries table

db = DB()

cur = db.cursor

csv_file = 'queries.csv'

csv_header = 'queries_id,query'

with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()

save_res = ""

sql = "select queries_id, queries_query from queries ORDER BY queries_id"

print(sql)

cur.execute(sql)

rows = cur.fetchall()

for er in rows:

    build_res = ""
    query_id = str(er[0])
    query = str(er[1])

    build_res = query_id+','+query

    save_res = '\n'+build_res

    with open(tmp+csv_file,'a+') as f:
        f.write(save_res)
    f.close()

db.DBDisconnect()

query_id = "0"

query = "import"

build_res = query_id+','+query

save_res = '\n'+build_res

with open(tmp+csv_file,'a+') as f:
    f.write(save_res)
f.close()

#Results from evaluations table

db = DB()

cur = db.cursor

csv_header = 'hash,module,result'

csv_file = 'evaluations.csv'

with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()

save_res = ""

sql = "SELECT count(evaluations_id) from evaluations"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

counter = rows[0][0]

counter = int(round(counter+0.5) / next) + 1

offset = 0

i = 0

for i in range(0, counter):

    db = DB()

    cur = db.cursor

    sql = "SELECT evaluations_results_hash, evaluations_module, evaluations_result from evaluations ORDER BY evaluations_results_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    db.DBDisconnect()

    offset = offset + next

    for row in rows:
        value = ""
        build_res = ""
        hash = str(row[0])
        module = str(row[1])
        value = str(row[2])

        build_res = hash+','+module+','+value

        save_res = '\n'+build_res

        with open(tmp+csv_file,'a+') as f:
            f.write(save_res)
        f.close()

#Results from results table

db = DB()

cur = db.cursor

save_res = ""

csv_header = 'results_studies_id,results_id,results_position,results_queries_id,results_url,results_main,results_se,hash'

csv_file = 'results.csv'

with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0

i = 0

sql = "SELECT count(results_id) from results"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

counter = rows[0][0]

counter = int(round(counter+0.5) / next) + 1

for i in range(0, counter):

    db = DB()

    cur = db.cursor

    sql = "select results_id, results_studies_id, results_position, results_queries_id, results_url, results_main, results_se, results_hash from results ORDER BY results_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    db.DBDisconnect()

    offset = offset + next

    connection = None

    for er in rows:

        build_res = ""
        results_id = str(er[0])
        study = str(er[1])
        results_pos = str(er[2])
        query_id = str(er[3])
        url = str(er[4])
        url = '"'+url+'"'
        main = str(er[5])
        main = '"'+main+'"'
        se = str(er[6])
        hash = str(er[7])


        build_res = study+','+results_id+','+results_pos+','+query_id+','+url+','+main+','+se+','+hash

        save_res = '\n'+build_res

        with open(tmp+csv_file,'a+') as f:
            f.write(save_res)
        f.close()

#Results from sources table / loading speed of webpage

db = DB()

cur = db.cursor

save_res = ""

csv_file = 'speed.csv'

csv_header = 'hash,speed'


with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()


offset = 0

i = 0

sql = "SELECT count(sources_id) from sources"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

counter = rows[0][0]

counter = int(round(counter+0.5) / next) + 1

for i in range(0, counter):

    db = DB()

    cur = db.cursor

    sql = "select sources_hash, sources_speed from sources ORDER BY sources_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    db.DBDisconnect()

    offset = offset + next

    connection = None

    for er in rows:

        build_res = ""
        hash = str(er[0])
        speed = str(er[1])


        build_res = hash+','+speed

        save_res = '\n'+build_res

        with open(tmp+csv_file,'a+') as f:
            f.write(save_res)
        f.close()




#use panda to join results

print("Load: results.csv")
print("\n")

results_df = pd.read_csv(tmp+'results.csv', error_bad_lines=False, low_memory=False)


print("Load: queries.csv")
print("\n")

queries_df = pd.read_csv(tmp+'queries.csv', error_bad_lines=False, low_memory=False)


print("Load: speed.csv")
print("\n")

speed_df = pd.read_csv(tmp+'speed.csv', error_bad_lines=False, low_memory=False)


print("Load: classifications.csv")
print("\n")

classfications_df = pd.read_csv(tmp+'classifications.csv', error_bad_lines=False, low_memory=False)


print("Load: evaluations.csv")
print("\n")

evaluations_df = pd.read_csv(tmp+'evaluations.csv', error_bad_lines=False, low_memory=False)


evaluations_df = evaluations_df.groupby('hash').agg(lambda x: list(x))


print("Merge: results speed")
print("\n")

results_speed_merged = results_df.merge(speed_df, left_on='hash', right_on='hash')



print("Merge: results speed evaluations")
print("\n")

results_speed_evaluations_merged = results_speed_merged.merge(evaluations_df, left_on='hash', right_on='hash')


print("Merge: results speed evaluations queries")
print("\n")

results_speed_evaluations_queries_merged = results_speed_evaluations_merged.merge(queries_df, left_on='results_queries_id', right_on='queries_id')


print("Merge: results speed evaluations queries classifications")
print("\n")


results_speed_evaluations_queries_classifications_merged = results_speed_evaluations_queries_merged.merge(classfications_df, left_on='hash', right_on='hash')


print("Save: seo_results.csv")
print("\n")


results_speed_evaluations_queries_classifications_merged.to_csv(r'seo_results.csv', index = False)

print("Finished")
print("\n")



#script to save results as readable table in a csv file
tools = ['tools analytics', 'tools caching', 'tools seo', 'tools content', 'tools social', 'tools ads']

#todo: dynamic creation of modules and header related to the indicators
csv_header = 'Study,ID,Hash,Position,Query_ID,Query,URL,Main,Search Engine,Speed,check canonical,check description,check external links,check h1,check https,check_identical_title,check internal links,check kw_count,check kw_density,check kw_in_description-og-name,check kw_in_description-og-property,check kw_in_href,check kw_in_link-text,check kw_in_meta-content,check kw_in_meta-description,check kw_in_meta-og,check kw_in_meta-properties,check kw_in_source,check kw_in_title,check kw_in_title-meta,check kw_in_title-og,check kw_in_url,check nofollow,check og,check sitemap,check title,check title_h1_identical,check title_h1_match,check url_length,check viewport,check word_count,check wordpress,micros,micros counter,robots_txt,source ads,source company,source known,source news,source not optimized,source search engine,source shop,source top,tools ads,tools ads count,tools analytics,tools analytics count,tools caching,tools caching count,tools content,tools content count,tools seo,tools seo count,tools social,tools social count'

db_modules = ['check canonical','check description','check external links','check h1','check https','check identical title', 'check internal links','check kw_count','check kw_density','check kw_in_href','check kw_in_link-text','check kw_in_meta-content','check kw_in_meta-description','check kw_in_meta-og','check kw_in_meta-properties','check kw_in_source','check kw_in_title','check kw_in_title-meta','check kw_in_title-og','check kw_in_description-og-property','check kw_in_description-og-name','check kw_in_url','check nofollow','check og','check sitemap','check title','check title_h1_identical','check title_h1_match','check url_length','check viewport','check word_count','check wordpress','micros','micros counter','robots_txt', 'source ads','source company','source known','source news','source not optimized','source shop', 'source search engine','source top', 'tools ads','tools ads count','tools analytics','tools analytics count','tools caching','tools caching count','tools content','tools content count','tools seo','tools seo count','tools social','tools social count']

#add classifier results to table
db = DB()

cur = db.cursor

sql = "SELECT distinct(classifications_classification) from classifications"

cur.execute(sql)

rows = cur.fetchall()
classes = rows

db.DBDisconnect()

res_classes = []

for c in classes:
    csv_header = csv_header+','+ c[0]





db_modules = sorted(db_modules, key=str.lower)


save_res = ""

csv_file = 'all_res.csv'


with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()



file = 'seo_results.csv'

#eval_results = pd.read_csv(file, error_bad_lines=False, skiprows=0, nrows=10000)

eval_results = pd.read_csv(file, error_bad_lines=False, low_memory=False)

pd.set_option('display.max_columns', None)


'''
results_studies_id                                                   82
results_id                                                        23003
results_position                                                    132
results_queries_id                                                  336
results_url           https://www.abendblatt.de/region/stormarn/arti...
results_main                                 https://www.abendblatt.de/
results_se                                                       Google
hash                                   007e34735874a3f83d95106bd5778d1a
speed                                                              4.44
module                ['check url_length', 'robots_txt', 'source top...
result                ['108', '1', '1', '0', '0', '0', '1', '0', '0'...
queries_id                                                          336
query                                                        hochwasser
decision_tree                                                 optimized
rules                                                         optimized

'''

#print(list(eval_results.columns))

print("Write to CSV")


for index, row in eval_results.iterrows():

    row_len = len(row)

    y = len(classes)
    y = y + 1

    class_results = []

    for x in classes:
        y = y - 1
        row_index = row_len - y
        class_results.append(row[row_index])

    build_res = ""
    hash = str(row[7])

    query_id = str(row[3])
    study = str(row[0])
    results_id = str(row[1])
    results_pos = str(row[2])
    queries_query = '"'+row[12]+'"'



    url = row[4]
    url = url.replace('"', '')
    url = url.replace(',', '')
    url = '"'+url+'"'

    main = row[5]
    main = main.replace('"', '')
    main = main.replace(',', '')
    main = '"'+main+'"'

    se = '"'+row[6]+'"'

    speed = str(row[8])


    modules = row[9]
    #print(modules)

    modules = modules.replace('"','')
    modules = modules.replace('[','')
    modules = modules.replace(']','')
    modules = modules.replace(', ',',')



    m_split = list(modules.split(","))

    m = []

    for x in m_split:
        x = x.replace("'",'')
        m.append(x)


    results = row[10]

    results = results.replace('"','')
    results = results.replace('[','')
    results = results.replace(']','')
    results = results.replace(', ',',')

    r_split= list(results.split(","))

    r = []

    for x in r_split:
        x = x.replace("'",'')
        r.append(x)


    elements = []


    for i in range(0, len(m)):

        elements.append((m[i], r[i]))

    #test_el = []

    for db_el in db_modules:
        if not db_el in m:
            #test_el.append(hash)
            m_val = db_el
            r_val = '"-100"'
            if "source" not in m_val:
                elements.append((m_val, r_val))
            else:
                m_val = db_el
                r_val = '0'
                elements.append((m_val, r_val))

    #mylist = list(dict.fromkeys(test_el))

    #for ml in mylist:
    #    if ml:
    #        print(ml)

        #print(elements)




    build_res = study+','+results_id+','+hash+','+results_pos+','+query_id+','+queries_query+','+url+','+main+','+se+','+speed+','

    lh_values = []
    lh_results = ''

    for el in elements:

        mod = el[0]
        val = str(el[1])

        lh_values.append((mod, val))


    lh_values= set(tuple(element) for element in lh_values)

    lh_list=[]
    added_keys = set()

    for row in lh_values:
    # We use tuples because they are hashable
        lookup = tuple(row[:1])
        if lookup not in added_keys:
            lh_list.append(row)
            added_keys.add(lookup)

    lh_list.sort(key=lambda x: x[0])

    #print(lh_list)

    #print(lh_list)
    #print("\n")
    #if len(lh_list) > 42:
        #print(len(lh_list))
        #print(len(db_modules))
        #print(url)
        #print(main)

    '''
    for l in lh_list:
        if l[0] not in db_modules:
        print(l[0])

    exit()
    '''

    mods = ''

    for t in lh_list:
        mods = mods+t[0]+','
        #print(mods)


    for l in lh_list:
        lh_results = lh_results + l[1]+','


    build_res = build_res+lh_results

    for cr in class_results:
        build_res = build_res+cr+','

    build_res = build_res[:-1]


    save_res = '\n'+build_res

    with open(csv_file,'a+') as f:
        f.write(save_res)
    f.close()
