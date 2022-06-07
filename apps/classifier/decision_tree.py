# Decision Tree Classifier

#include libs

import sys
sys.path.insert(0, '..')
from include import *

def classify(classifier_id, hashes):

    #convert nominal values to numerical values
    def is_float(value):
      try:
        float(value)
        return True
      except:
        return False

    def is_int(value):
      try:
        int(value)
        return True
      except:
        return False

    #load results with features and check if all features available: skip results without the number of all indicators (skip incomplete results)
    for h in hashes:
        hash = h[0]

        result = Evaluations.getResultwithIndicators(hash)


        #add loading speed as indicator
        speed = Results.getSpeed(hash)
        speed = speed[0][0]

        data_dict = {}

        if len(result) == int(number_indicators):

            for r in result:


                feature = r[2]
                value = r[3]




                data_dict.update( {feature: value} )

            df = pd.DataFrame([data_dict])

            df.rename(columns=lambda x: x.lower(), inplace=True)

            df['speed'] = float(speed)

            df.loc[df['speed'] < 0, 'speed'] = -1

            pd.set_option('display.max_columns', None)

            #remove cols which are no part of the model
            id_cols = ['micros', 'tools ads', 'tools analytics', 'tools caching', 'tools content', 'tools seo', 'tools social']

            df.drop(columns=id_cols, inplace=True)

            #load indicators as features
            features = df.columns.values

            #load model
            model = load('dt_classifier.joblib')

            #predict the seo probability
            def predict_func(model, df, features):
                return model.predict(df[features])


            predict_vals = predict_func(model, df, features)



            #assign seo probability to nominal value
            seo_classes = {0:'not_optimized', 1:'probably_not_optimized', 2:'probably_optimized', 3:'optimized'}

            for p in predict_vals:
                print(p)
                df['seo'] = seo_classes.get(p)
                classification_result = seo_classes.get(p)

            #save predicted value to database
            Evaluations.updateClassificationResult(hash, classification_result, classifier_id, today)
            print(hash)
            print(classification_result)
