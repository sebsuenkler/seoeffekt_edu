# Decision Tree Classification

#include libs

import sys
sys.path.insert(0, '..')
from include import *

#load classifiers from config file

try:

    with open('../../config/classifier.ini', 'r') as f:
        array = json.load(f)

    classifier = array['classifier']


    hashes_check = []

    evaluations_modules = Evaluations.getEvaluationModules()

    number_of_indicators = len(evaluations_modules)

    hashes = Evaluations.getResultstoClassify(number_of_indicators)

    if(Evaluations.getUnassigned()):
        hashes_check = Evaluations.getResultstoClassifyCheck()


    #classify results using all available classifiers
    for c in classifier:
        classifier_id = c
        classification_result = "unassigned"
        Evaluations.deleteDupClassifiedData()


        if(hashes):
            for h in hashes:
                hash = h[0]
                if (not Evaluations.getClassificationResultValue(hash, classifier_id, classification_result)):
                    Evaluations.insertClassificationResult(hash, classification_result, classifier_id, today)
                    #print(hash)
                    #print(classification_result)


        if(hashes_check):
            for hc in hashes_check:
                hash = hc[0]
                classes = hc[1]
                if classifier_id not in classes:
                    if (not Evaluations.getClassificationResultValue(hash, classifier_id, classification_result)):
                        Evaluations.insertClassificationResult(hash, classification_result, classifier_id, today)
                        #print(hash)
                        #print(classification_result)




        hashes_to_classify = Evaluations.getResultstoUpdateClassification(classifier_id, classification_result)



        if(hashes_to_classify):
            class_module = __import__(classifier_id)
            class_module.classify(classifier_id, hashes_to_classify)


except Exception as e:
    print(e)
    print('error')

else:
    exit()
