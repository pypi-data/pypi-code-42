
from . import LabelEncode
from . import Impute
from . import Scale
from . import OneHotEncode

class CorrCoeffThreshold():
    def __init__(self, 
                 AbsCorrCoeff_threshold = 0.99):
        """
        Method for filtering features with correlation coefficients >= the AbsCorrCoeff_threshold (absolute value of corerlation coeff. threshold) value passed, where the correlation coefficient is the pearson coerrelation coefficient
        
        Arguments:
        ----------
            AbsCorrCoeff_threshold: float. default = 0.99
        """
        assert(AbsCorrCoeff_threshold>=0)
        assert(AbsCorrCoeff_threshold<=1)
        self.AbsCorrCoeff_threshold = AbsCorrCoeff_threshold
        
    def __fetch_dropped_features_slice_dict__(self,
                                              np_corr_col, 
                                              feature_idx,
                                              AbsCorrCoeff_threshold):
            """
            Arguments:
            ----------
                np_corr_col: column of correlation coefficients for the feature of feature_idx
                feature_idx: the index corresponding to the column slice of the correlation coeff. matrix
                AbsCorrCoeff_threshold: Absolute value threshold limit for the correlation coefficients to filter
            """
            
            import numpy as np
            
            dropped_features_slice_dict = {'dropped feature idx':[],
                                           'correlated feature idx':[],
                                           'corr coeff':[]}
            for i in range(np_corr_col.shape[0]):
                if i!=feature_idx:
                    if np.abs(np_corr_col[i])>= AbsCorrCoeff_threshold:
                        dropped_features_slice_dict['dropped feature idx'].append(i)
                        dropped_features_slice_dict['correlated feature idx'].append(feature_idx)
                        dropped_features_slice_dict['corr coeff'].append(np_corr_col[i])
                        
            return dropped_features_slice_dict
        
    def fit(self, 
            df, 
            CorrCoeff_features = 'auto',
            verbose = 0):
        """
        Fit the CorrelationCoeffThreshold object to the data
        
        Arguments:
        ----------
            df: the pandas dataframe of interest
            conv_features: list. the subset of features to analyze the covariance on. If 'auto' then all columns in the df will be used
        """
        import numpy as np
        import joblib   
        import gc
        
        df = df.copy()

        #assigne self.CorrCoeff_features
        if CorrCoeff_features == 'auto':
            self.CorrCoeff_features = list(df.columns)
        else:
            assert(type(CorrCoeff_features)==type(list())), 'CorrCoeff_features must be "auto" or a list'
            self.CorrCoeff_features = CorrCoeff_features
        
            df = df[self.CorrCoeff_features]
            
        np_corr = np.corrcoef(df, rowvar=False)
        del df
        gc.collect()
        
        executor = joblib.parallel.Parallel(n_jobs = -1, verbose=verbose, backend='multiprocessing')
        tasks = [joblib.parallel.delayed(self.__fetch_dropped_features_slice_dict__)(np_corr[:,feature_idx],
                                                                            feature_idx,
                   self.AbsCorrCoeff_threshold) for feature_idx in range(np_corr.shape[0])]
        del np_corr
        gc.collect()
        
        #execute the task
        outputs = executor(tasks)
        del tasks
        gc.collect()
        
        #assemble outputs into full dictionary
        self.dropped_features_dict = {'dropped feature':[],
                                      'correlated feature':[],
                                      'corr coeff':[]}
        for dropped_feat_slice_dict in outputs:
            for i in range(len(dropped_feat_slice_dict['dropped feature idx'])):
                correlated_feat = self.CorrCoeff_features[dropped_feat_slice_dict['correlated feature idx'][i]]
                if correlated_feat  not in self.dropped_features_dict['correlated feature']:
                    dropped_feature = self.CorrCoeff_features[dropped_feat_slice_dict['dropped feature idx'][i]]
                    self.dropped_features_dict['dropped feature'].append(dropped_feature)
                    self.dropped_features_dict['correlated feature'].append(correlated_feat)
                    self.dropped_features_dict['corr coeff'].append(dropped_feat_slice_dict['corr coeff'][i])
                        
    def transform(self, df):
        """
        Transform the pandas df based on the previously run fit
        
        Arguments:
        ----------
            df: pandas dataframe which will be transformed
        """
        df = df.copy()
        for feature in self.dropped_features_dict['dropped feature']:
            if feature in df:
                df = df.drop(columns=[feature])
        return df
        

class feat_eng_pipe():
    
    """
    Iterate through a standard feature engineering sequence and save the resulting engineered data.
    Arguments:
    ---------
        path_report_dir: directory. Default: None. the path to the directory where the feature engineering cases will be saved. It is recommended that you save outside the repo. directory where the notebook is stored, as the saved files may be > 50mb.
        verbose: int. higher values implies more print outs
        overwrite: boolean. Defeault: False. whether to overwrite a previously generated feature engineering case if it has already been saved.
    Sequence:
    ---------
        LabelEncode.categorical_features ->  
        Scale.continuous_features -> 
            -for Scaler_ID in Scalers_dict.keys()
        Impute.categorical_features ->
            - for Imputer_categorical_ID,  categorical_iterative_estimators in INSERT
                - for categorical_estimatorID in categorical_iterative_estimators:
        Imputer.continuous_features ->
            - for Imputer_continuous_ID,  continuous_iterative_estimators in INSERT
                - for continuous_estimatorID in continuous_iterative_estimators:
        OneHotEncode ->
        Train_test_split ->
        Finished!
    Future Version Updates
    -----------------------
    - add functionality for Impute_iterative_classifier_dict() to iteratively imput categorical data
    
    """
    def __init__(self, 
                 path_report_dir, 
                 verbose = 1, 
                 overwrite=False):
        
        import os, sys
        import gc
        if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
            sys.path.insert(0,  os.path.dirname(os.path.abspath(os.path.join(__file__,'..'))))
        
        self.path_report_dir = path_report_dir
        
        #define the feat_eng directory to store the cases and outputs
        self.path_feat_eng_root_dir = os.path.join(path_report_dir,'outputs','feat_eng')
        
        #build the feat_eng directory if it doesn't exist yet
        if os.path.isdir(self.path_feat_eng_root_dir)==False:
            os.makedirs(self.path_feat_eng_root_dir)
            
        self.verbose = verbose
        self.overwrite = overwrite
        
        #define default OneHot_cases
        self.OneHot_cases = [True, False]
        
        #fetch Scalers_dict
        self.Scalers_dict = Scale.default_Scalers_dict()
        
        #fetch impute iterative classifier dict
        #Imputer_iterative_classifier_dict = {None: None} #Impute.default_iterative_classifier_dict()
            
        #Imputer categorical dict of form {method: estimator}
        self.Imputer_categorical_dict = {'most_frequent':{None:None},
                                         #'iterative': Imputer_iterative_classifier_dict
                                        }
        
        #Fetch impute iterative regressors dict
        Imputer_iterative_regressors_dict = Impute.default_iterative_regressors_dict()
        
        #Imputer continous dict of form {method: estimator}
        self.Imputer_continuous_dict = {'median':{None:None},
                                        'iterative': Imputer_iterative_regressors_dict
                                        }
        
        #CorrCoeffThresholder Params
        self.AbsCorrCoeff_thresholds = [0.99] 
        
        if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
            sys.path.insert(0,  os.path.dirname(os.path.abspath(os.path.join(__file__,'..','..'))))
        from ... import file_utils
        
        self.save = file_utils.save
        self.load = file_utils.load
        
    def __feat_eng_files_saved__(self,
                                 files,
                                 path_feat_eng_dir, 
                                 format_ ):
        """
        Check if feat eng files are save for the specific case directory passed. Returns False if the X
        """
        import os, sys
        import gc
        
        gc.collect()

        file_saved_list = []

        #build list of files to look for
        files = [file+'.'+format_ for file in files]

        #check if all files exist
        for file in files:
            if format_ == 'h5_csv':
                h5_csv_file_saved_list = []
                for format_ in ['csv','h5']:
                    path_save_file = os.path.join(path_feat_eng_dir,file.replace('h5_csv',format_)) 
                    h5_csv_file_saved_list.append(os.path.isfile(path_save_file))
                #if either h5 or csv saved, append True
                file_saved_list.append(any(h5_csv_file_saved_list)) 
            else:
                path_save_file = os.path.join(path_feat_eng_dir,file)
                
                file_saved_list.append(os.path.isfile(path_save_file))
        
        gc.collect()
        
        #if all files saved, return True
        feat_eng_files_saved = all(file_saved_list) 
        
        return feat_eng_files_saved      
    
    def __path_feat_eng_base_dir__(self, path_feat_eng_dir, 
                                         OneHot_case,
                                          Scaler_ID,
                                          Imputer_cat_ID,
                                          Imputer_iter_class_ID,
                                          Imputer_cont_ID,
                                          Imputer_iter_reg_ID,
                                           AbsCorrCoeff_threshold):
        import os
        path_feat_eng_base_dir = os.path.join(path_feat_eng_dir,
                                  'Scaler_ID['+Scaler_ID+']',
                                  'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                  'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']',
                                  'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                  'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']',
                                  'OneHot_case['+str(OneHot_case)+']',
                                  'CorrCoeffThreshold['+str(AbsCorrCoeff_threshold)+']')
        return path_feat_eng_base_dir

 
    ######### Fit Transforme Operations ############
    
    def __fit_transform_LabelEncode__(self,
                                        X, 
                                        path_feat_eng_dir,
                                        headers_dict,
                                        format_):
        import os, sys
        import gc
        
        gc.collect()

        #label encode X
        files=['X']
        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'LabelEncode')
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True or self.overwrite=='LabelEncode':
            LabelEncoder = LabelEncode.categorical_features()
            LabelEncoder.fit(X, categorical_headers=headers_dict['categorical features'])

            X = LabelEncoder.transform(X)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            
            self.LabelEncoder = LabelEncoder
            
            #save the encoder
            self.save(LabelEncoder, 'LabelEncoder', 'dill', path_feat_eng_dir)

        else: 
            del X
            gc.collect()
                
            X = self.load('X', format_, path_feat_eng_dir)
            
        gc.collect()
        return X, path_feat_eng_dir
    
    
        
    def __fit_transform_Scale__(self,
                                X, 
                                path_feat_eng_dir,
                                headers_dict,
                                format_,
                                Scaler_ID,
                                Imputer_cat_ID,
                                Imputer_iter_class_ID):
        """
        Scale, transform, and save the continuous data
        """
        import os, sys
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'Scaler_ID['+Scaler_ID+']')
        
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True:

            Scaler = Scale.continuous_features(Scaler = self.Scalers_dict[Scaler_ID])
            Scaler.fit(X, headers_dict['continuous features'])
            X = Scaler.transform(X)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
                
            #save the Scaler
            self.save(Scaler, 'Scaler', 'dill', path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                          'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                          'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']')
            if self.__feat_eng_files_saved__(files, path_next_step, format_)==False:
                del X
                gc.collect()
                
                X = self.load('X', format_, path_feat_eng_dir)
                
        gc.collect()

        return X, path_feat_eng_dir
   
    def __fit_transform_Impute_categorical__(self,
                                               X, 
                                              path_feat_eng_dir,
                                              headers_dict,
                                              format_,
                                              Imputer_cat_ID,
                                              Imputer_iter_class_ID,
                                              Imputer_cont_ID,
                                              Imputer_iter_reg_ID):
        """
        Impute, transform, and save the categorical data
        """
        import os, sys
        import gc
        
        gc.collect()
        
        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 
                                   'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                   'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']')
        
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True:

            X, Imputer = Impute.categorical_features(X, 
                                                    headers_dict['categorical features'], 
                                                    strategy = Imputer_cat_ID, 
                                                    estimator = self.Imputer_categorical_dict[Imputer_cat_ID][Imputer_iter_class_ID],
                                                    verbose= 0)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
               
            #save the Imputer
            self.save(Imputer, 'Imputer', 'dill', path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                          'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                          'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']')
            if self.__feat_eng_files_saved__(files, path_next_step, format_)==False:
                del X
                gc.collect()
                
                X = self.load('X', format_, path_feat_eng_dir)
                
        gc.collect()

        return X, path_feat_eng_dir
        
        
    def __fit_transform_Impute_continuous__(self,
                                  X, 
                                  path_feat_eng_dir,
                                  headers_dict,
                                  format_,
                                  Imputer_cont_ID,
                                  Imputer_iter_reg_ID,
                                  OneHot_case):
        """
        Impute, transform, and save the continuous data
        """
        import os, sys
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 
                               'Imputer_continuous_ID['+Imputer_cont_ID+']',
                               'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']')
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True:

            X, Imputer = Impute.continuous_features(X, 
                    headers_dict['continuous features'], 
                    strategy = Imputer_cont_ID, 
                    estimator = self.Imputer_continuous_dict[Imputer_cont_ID][Imputer_iter_reg_ID],
                    verbose= 0)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
               
            #save the Imputer
            self.save(Imputer, 'Imputer', 'dill', path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir,'OneHot_case['+str(OneHot_case)+']')
            
            if self.__feat_eng_files_saved__(files, path_next_step, format_)==False or self.overwrite=='OneHot':
                del X
                gc.collect()
                
                X = self.load('X', format_, path_feat_eng_dir)
                 
                if format_ != 'csv':
                    import pandas as pd
                    headers_dict = self.load('headers_dict', 'json', self.path_feat_eng_root_dir)
                    X = pd.DataFrame(X, columns = headers_dict['features'])
                    
        gc.collect()
        
        return X, path_feat_eng_dir

    def __fit_transform_OneHot_Encode__(self,
                              X, 
                              path_feat_eng_dir,
                              headers_dict,
                              format_,
                              OneHot_case,
                              AbsCorrCoeff_threshold):
        """
        OneHotEncode, transform, and save the categorical data
        """
        import os, sys
        import numpy as np
        import pandas as pd
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'OneHot_case['+str(OneHot_case)+']')
        
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True or self.overwrite=='OneHot' or self.overwrite == 'OneHotEncode' or self.overwrite == 'OneHot_Encode':

            if OneHot_case:
                #fetch the label encoder
                self.LabelEncoder = self.load('LabelEncoder', 'dill', os.path.join(self.path_feat_eng_root_dir, 'LabelEncode') )
                return_format='npArray'
                
                OneHotEncoder = OneHotEncode.categorical_features(return_format = return_format,
                                                                  LabelEncoder = self.LabelEncoder)
                OneHotEncoder.fit(X, categorical_headers=headers_dict['categorical features'])

                X = OneHotEncoder.transform(X)
                
                #save the headers_dict after one hot
                headers_dict['headers after OneHot'] = OneHotEncoder.headers_after_OneHot

                #save the encoder
                self.save(OneHotEncoder, 'OneHotEncoder', 'dill', path_feat_eng_dir)

            else: #if OneHot is False, just skip transform to numpy array
                headers_dict['headers after OneHot'] = list(X.columns)
                X = np.array(X)
                   
            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            
            self.save(headers_dict, 'headers_dict', 'json', path_feat_eng_dir)
            
            #transform back to pandas df
            X = pd.DataFrame(X, columns = headers_dict['headers after OneHot'])
            
        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir,'CorrCoeffThreshold['+str(AbsCorrCoeff_threshold)+']')
            
            if self.__feat_eng_files_saved__(files, path_next_step, format_)==False or self.overwrite=='CorrCoeffThreshold' or self.overwrite=='CorrCoeff' or self.overwrite=='CorrCoeffThresholder' :
                del X
                gc.collect()
            
                X = self.load('X', format_, path_feat_eng_dir)
                
                headers_dict = self.load('headers_dict', 'json', path_feat_eng_dir)
                 
                #transform back to pandas df
                X = pd.DataFrame(X, columns = headers_dict['headers after OneHot'])

        gc.collect()

        return X, path_feat_eng_dir, headers_dict
    
    def __fit_transform_CorrCoeffThreshold__(self,
                                          X, 
                                          path_feat_eng_dir,
                                          headers_dict,
                                          format_,
                                          AbsCorrCoeff_threshold):
        """
        OneHotEncode, transform, and save the categorical data
        """
        import os, sys
        import numpy as np
        import pandas as pd
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir,'CorrCoeffThreshold['+str(AbsCorrCoeff_threshold)+']')
        
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_)==False or self.overwrite==True  or self.overwrite=='CorrCoeffThreshold' or self.overwrite=='CorrCoeff' or self.overwrite=='CorrCoeffThresholder' :

            if AbsCorrCoeff_threshold!=1:
                
                CorrCoeffThresholder = CorrCoeffThreshold(AbsCorrCoeff_threshold)
                
                CorrCoeffThresholder.fit(X)

                X = CorrCoeffThresholder.transform(X)
                
                #save the encoder
                self.save(CorrCoeffThresholder, 'CorrCoeffThresholder', 'dill', path_feat_eng_dir)
   
            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            
            #save the headers_dict after transform
            headers_dict['headers after CorrCoeffThreshold'] = list(X.columns)

            self.save(headers_dict, 'headers_dict', 'json', path_feat_eng_dir)
            
        else:
            del X
            gc.collect()
            
            #load
            X = self.load('X', format_, path_feat_eng_dir)
            
            headers_dict = self.load('headers_dict', 'json', path_feat_eng_dir)
        
            if format_ != 'csv':
                import pandas as pd
                X = pd.DataFrame(X, columns = headers_dict['headers after CorrCoeffThreshold'])

        gc.collect()

        return X, path_feat_eng_dir, headers_dict
    
    
    def __fit_transform_feat_eng_case__(self,
                                          X,
                                          headers_dict,
                                          path_feat_eng_dir,
                                          format_,
                                          Scaler_ID,
                                          Imputer_cat_ID,
                                          Imputer_iter_class_ID,
                                          Imputer_cont_ID,
                                          Imputer_iter_reg_ID,
                                          OneHot_case,
                                          AbsCorrCoeff_threshold):
        """
        run through a single feature engineering case instance (after Label Encoding)
        Arguments:
        ----------
            X, X_field: the datasets to run feature engineering on
            ...
        """
        import os, sys
        import gc
        
        gc.collect()
        
        #build feat_eng_case_base_dir
        path_feat_eng_base_dir = self.__path_feat_eng_base_dir__(path_feat_eng_dir, 
                                                                  OneHot_case,
                                                                  Scaler_ID,
                                                                  Imputer_cat_ID,
                                                                  Imputer_iter_class_ID,
                                                                  Imputer_cont_ID,
                                                                  Imputer_iter_reg_ID,
                                                                  AbsCorrCoeff_threshold)
        
        if os.path.isdir(path_feat_eng_base_dir)==False:
            os.makedirs(path_feat_eng_base_dir)

        #check if all the required files are saved in the base directory
        all_data_previously_saved = True
        for filename in ['X', 'headers_dict.json']:

            if 'headers_dict' not in filename:
                filename = filename+'.'+format_

            path_save_file = os.path.join(path_feat_eng_base_dir, filename)
            if os.path.isfile(path_save_file)==False:
                all_data_previously_saved = False

        if all_data_previously_saved==False or self.overwrite == True: 

            X = X.copy()
            headers_dict = headers_dict.copy()

            ####### Scale #########
            X, path_feat_eng_dir = self.__fit_transform_Scale__(X, 
                                                                path_feat_eng_dir,
                                                                headers_dict,
                                                                format_,
                                                                Scaler_ID,
                                                                Imputer_cat_ID,
                                                                Imputer_iter_class_ID)
            ####### Impute Categorical Features #########
            X, path_feat_eng_dir = self.__fit_transform_Impute_categorical__(X, 
                                                              path_feat_eng_dir,
                                                              headers_dict,
                                                              format_,
                                                              Imputer_cat_ID,
                                                              Imputer_iter_class_ID,
                                                              Imputer_cont_ID,
                                                              Imputer_iter_reg_ID)

            ###### Impute Continuous Features ########
            X, path_feat_eng_dir = self.__fit_transform_Impute_continuous__(X, 
                                                                      path_feat_eng_dir,
                                                                      headers_dict,
                                                                      format_,
                                                                      Imputer_cont_ID,
                                                                      Imputer_iter_reg_ID,
                                                                      OneHot_case)

            ##### One Hot Encode #####
            X, path_feat_eng_dir, headers_dict = self.__fit_transform_OneHot_Encode__(X, 
                                                                                  path_feat_eng_dir,
                                                                                  headers_dict,
                                                                                  format_,
                                                                                  OneHot_case,
                                                                                  AbsCorrCoeff_threshold)
            
            ##### CorreCoeffThreshold #####
            X, path_feat_eng_dir, headers_dict = self.__fit_transform_CorrCoeffThreshold__(X, 
                                                                                      path_feat_eng_dir,
                                                                                      headers_dict,
                                                                                      format_,
                                                                                      AbsCorrCoeff_threshold)
            
            assert(path_feat_eng_base_dir == path_feat_eng_dir)

            del X
            gc.collect()
            
            self.headers_dict = headers_dict
            
        else:
            if self.verbose>=2: print('pre-existing saved data found at path_feat_eng_dir:', path_feat_eng_base_dir)
        
    ############# Transform Operations #########################
    
    def __transform_LabelEncode__(self,
                                    X_field, 
                                    path_feat_eng_dir):
        """
        Transform and save X_field using LabelEncoder
        """
        import os, sys
        import gc
        
        gc.collect()

        #label encode X
        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'LabelEncode')
        
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True or self.overwrite=='LabelEncode':
            
            LabelEncoder = self.load('LabelEncoder', 'dill', path_feat_eng_dir)
            
            X_field = LabelEncoder.transform(X_field)

            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)
            
        else: 
            del X_field
            gc.collect()
            
            X_field = self.load('X_field', self.format_, path_feat_eng_dir)
        
        gc.collect()
        return X_field, path_feat_eng_dir
                
      
    def __transform_Scale__(self,
                        X_field, 
                        path_feat_eng_dir,
                        Scaler_ID,
                        Imputer_cat_ID,
                        Imputer_iter_class_ID):
        """
        transform, and save the continuous data
        """
        import os, sys
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'Scaler_ID['+Scaler_ID+']')
        
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True:

            Scaler = self.load('Scaler', 'dill', path_feat_eng_dir)
            
            X_field = Scaler.transform(X_field)

            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)
            
        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                  'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                  'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']')
            if self.__feat_eng_files_saved__(files, path_next_step, self.format_)==False:
                X_field = self.load('X_field', self.format_, path_feat_eng_dir)
        
        gc.collect()

        return X_field, path_feat_eng_dir   
    
    def __transform_Impute_categorical__(self,
                                   X_field, 
                                   path_feat_eng_dir,
                                   Imputer_cat_ID,
                                   Imputer_iter_class_ID,
                                   Imputer_cont_ID,
                                   Imputer_iter_reg_ID):
        """
        Transform and save the categorical data using the fitted Imputer
        """
        import os, sys
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 
                                  'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                  'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']')
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True:

            Imputer = self.load('Imputer', 'dill', path_feat_eng_dir)

            X_field[self.headers_dict['categorical features']] = Imputer.transform(X_field[self.headers_dict['categorical features']])

            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                          'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                          'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']')
            if self.__feat_eng_files_saved__(files, path_next_step, self.format_)==False:
                X_field = self.load('X_field', self.format_, path_feat_eng_dir)
        
        gc.collect()

        return X_field, path_feat_eng_dir
        
        
    def __transform_Impute_continuous__(self,
                                  X_field, 
                                  path_feat_eng_dir,
                                  Imputer_cont_ID,
                                  Imputer_iter_reg_ID,
                                  OneHot_case):
        """
        Impute, transform, and save the continuous data
        """
        import os, sys
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 
                                      'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                      'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']')
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True:

            Imputer = self.load('Imputer', 'dill', path_feat_eng_dir)
            
            X_field[self.headers_dict['continuous features']] = Imputer.transform(X_field[self.headers_dict['continuous features']])

            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir,'OneHot_case['+str(OneHot_case)+']')
            if self.__feat_eng_files_saved__(files, path_next_step, self.format_)==False or self.overwrite=='OneHot':
                X_field = self.load('X_field', self.format_, path_feat_eng_dir)
                    
                if self.format_ != 'csv':
                    import pandas as pd
                    X_field = pd.DataFrame(X_field, columns = self.headers_dict['features'])
        
        gc.collect()
        
        return X_field, path_feat_eng_dir

    def __transform_OneHot_Encode__(self,
                              X_field, 
                              path_feat_eng_dir,
                              OneHot_case,
                              AbsCorrCoeff_threshold):
        """
        OneHotEncode, transform, and save the categorical data
        """
        import os, sys
        import numpy as np
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'OneHot_case['+str(OneHot_case)+']')
        
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True or self.overwrite=='OneHot' or self.overwrite == 'OneHotEncode' or self.overwrite == 'OneHot_Encode':

            if OneHot_case:
                #fetch the label encoder
                self.LabelEncoder = self.load('LabelEncoder', 'dill',
                                      os.path.join(self.path_feat_eng_root_dir, 'LabelEncode') )
                
                return_format='npArray'
                
                OneHotEncoder = self.load('OneHotEncoder', 'dill', path_feat_eng_dir)
                
                X_field = OneHotEncoder.transform(X_field)
                
            else: #if OneHot is False, just skip transform to numpy array
                X_field = np.array(X_field) 
                    
            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)
            
        else:
             #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir,'CorrCoeffThreshold['+str(AbsCorrCoeff_threshold)+']')
            
            if self.__feat_eng_files_saved__(files, path_next_step, self.format_)==False or self.overwrite=='CorrCoeffThreshold' or self.overwrite=='CorrCoeff' or self.overwrite=='CorrCoeffThresholder' :
                del X_field
                gc.collect()
                
                X_field = self.load('X_field', self.format_, path_feat_eng_dir)
                
                headers_dict = self.load('headers_dict', 'json', path_feat_eng_dir)
                 
                #transform back to pandas df
                import pandas as pd
                X_field  = pd.DataFrame(X_field, columns = headers_dict['headers after OneHot'])
            
        gc.collect()

        return X_field, path_feat_eng_dir
    
    def __transform_CorrCoeffThreshold__(self,
                                          X_field, 
                                          path_feat_eng_dir,
                                          AbsCorrCoeff_threshold):
        """
        OneHotEncode, transform, and save the categorical data
        """
        import os, sys
        import numpy as np
        import pandas as pd
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir,'CorrCoeffThreshold['+str(AbsCorrCoeff_threshold)+']')
        
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_)==False or self.overwrite==True  or self.overwrite=='CorrCoeffThreshold' or self.overwrite=='CorrCoeff' or self.overwrite=='CorrCoeffThresholder' :

            if AbsCorrCoeff_threshold!=1:
                
                CorrCoeffThresholder = self.load('CorrCoeffThresholder', 'dill', path_feat_eng_dir)
                
                X_field = CorrCoeffThresholder.transform(X_field)
                
            #save
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)
            
        else:
            del X_field
            gc.collect()
            
            #load
            X_field = self.load('X_field', self.format_, path_feat_eng_dir)
            
            headers_dict = self.load('headers_dict', 'json', path_feat_eng_dir)
        
            if self.format_ != 'csv':
                import pandas as pd
                X_field = pd.DataFrame(X_field, columns = headers_dict['headers after CorrCoeffThreshold'])

        gc.collect()

        return X_field, path_feat_eng_dir
      
    def __transform_feat_eng_case__(self,
                                  X_field,
                                  path_feat_eng_dir,
                                  Scaler_ID,
                                  Imputer_cat_ID,
                                  Imputer_iter_class_ID,
                                  Imputer_cont_ID,
                                  Imputer_iter_reg_ID,
                                  OneHot_case,
                                  AbsCorrCoeff_threshold):
        """
        run through a single feature engineering case instance (after Label Encoding)
        Arguments:
        ----------
            X_field: the datasets to run feature engineering on
            ...
        """
        import os, sys
        import gc
        
        gc.collect()
        
        #define feat_eng_case_base_dir
        path_feat_eng_base_dir = self.__path_feat_eng_base_dir__(path_feat_eng_dir, 
                                                                  OneHot_case,
                                                                  Scaler_ID,
                                                                  Imputer_cat_ID,
                                                                  Imputer_iter_class_ID,
                                                                  Imputer_cont_ID,
                                                                  Imputer_iter_reg_ID,
                                                                  AbsCorrCoeff_threshold)

        #check if all the required files are saved in the base directory
        all_data_previously_saved = True
        for filename in ['X_field', 'headers_dict.json']:

            if 'headers_dict' not in filename:
                filename = filename+'.'+self.format_

            path_save_file = os.path.join(path_feat_eng_base_dir, filename)
            if os.path.isfile(path_save_file)==False:
                all_data_previously_saved = False

        if all_data_previously_saved==False or self.overwrite == True: 

            X_field = X_field.copy()
            
            ####### Scale #########
            X_field, path_feat_eng_dir = self.__transform_Scale__(X_field, 
                                                                    path_feat_eng_dir,
                                                                    Scaler_ID,
                                                                    Imputer_cat_ID,
                                                                    Imputer_iter_class_ID)
            ####### Impute Categorical Features #########
            X_field, path_feat_eng_dir = self.__transform_Impute_categorical__(X_field, 
                                                              path_feat_eng_dir,
                                                              Imputer_cat_ID,
                                                              Imputer_iter_class_ID,
                                                              Imputer_cont_ID,
                                                              Imputer_iter_reg_ID)

            ###### Impute Continuous Features ########
            X_field, path_feat_eng_dir = self.__transform_Impute_continuous__(X_field, 
                                                                      path_feat_eng_dir,
                                                                      Imputer_cont_ID,
                                                                      Imputer_iter_reg_ID,
                                                                      OneHot_case)

            ##### One Hot Encode #####
            X_field, path_feat_eng_dir = self.__transform_OneHot_Encode__(X_field, 
                                                                          path_feat_eng_dir,
                                                                          OneHot_case,
                                                                          AbsCorrCoeff_threshold)
            
            #### CorrCoeffThreshold #####
            X_field, path_feat_eng_dir = self.__transform_CorrCoeffThreshold__(X_field, 
                                                                                  path_feat_eng_dir,
                                                                                  AbsCorrCoeff_threshold)
           
            del X_field
            gc.collect()
            
        else:
            if self.verbose>=2: print('pre-existing saved data found at path_feat_eng_dir:', path_feat_eng_base_dir)
        
        
    def fit(self,
            X, 
            headers_dict = None,
            format_ = 'csv'):
        """
        Run standard feature engineering processes on data.
        Arguments:
            X: pandas dataframe. The train and test set features which will be engineered
            headers_dict: dictionary containing a list of headers. The required keys are
                - categorical features
                - continuous features
            format_: string. Default: 'csv'.
                - 'csv': saves the engineered data as a csv using pandas or numpy
                - 'h5': saves the engineered data as h5 dataset
        """
        import os, sys
        import pandas as pd
        
        import gc
        gc.collect()
        
        for key_header in ['categorical features', 'continuous features']:
            assert(key_header in headers_dict.keys()), 'headers_dict is missing the "'+key_header+'" key'
            
        X = X.copy()

        headers_dict = headers_dict.copy()
        
        self.format_ = format_ 
        
        #ensure only the features identified in the headers dict are passed
        assert(X[headers_dict['categorical features']+headers_dict['continuous features']].shape[1] == X.shape[1]), 'The headers in X do not match the contiuous and categorical headers in the headers_dict'
        
        if self.verbose>=2: 
            print('X.info():')
            X.info()
            
        #Save X
        path_feat_eng_dir = self.path_feat_eng_root_dir 
        
        files=['X']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, format_) == False or self.overwrite==True:
            self.save(X, 'X', format_, path_feat_eng_dir)
                
            #save the original headers dict
            headers_dict['features'] = list(X.columns)
            self.save(headers_dict,  'headers_dict', 'json', self.path_feat_eng_root_dir)

        #LabelEncode
        print('-------------------------------- fit feat_eng_pipe --------------------------------')
        
        if self.verbose>=1: print('LabelEncode')
        
        X, path_feat_eng_dir = self.__fit_transform_LabelEncode__(X, 
                                                                    path_feat_eng_dir,
                                                                    headers_dict,
                                                                    format_)
        
        self.path_feat_eng_dirs = []
        
        for Scaler_ID in self.Scalers_dict.keys():
            if self.verbose>=1: print('\tScale:',Scaler_ID)

            #Impute categorical features
            for Imputer_cat_ID in self.Imputer_categorical_dict.keys():
                
                for Imputer_iter_class_ID in self.Imputer_categorical_dict[Imputer_cat_ID].keys():
                    if self.verbose>=1: print('\t\tImpute Categorical Features:',
                                              Imputer_cat_ID,'[',Imputer_iter_class_ID,']')

                    #impute continuous features
                    for Imputer_cont_ID in self.Imputer_continuous_dict.keys():

                        for Imputer_iter_reg_ID in self.Imputer_continuous_dict[Imputer_cont_ID].keys():
                            
                            if self.verbose>=1: print('\t\t\tImpute Continuous Features:',
                                                      Imputer_cont_ID,'[',Imputer_iter_reg_ID,']')

                            for OneHot_case in self.OneHot_cases:
                                
                                if self.verbose>=1: print('\t\t\t\tOne Hot Encode:','[',OneHot_case,']')
                                    
                                for AbsCorrCoeff_threshold in self.AbsCorrCoeff_thresholds:
                                    
                                    if self.verbose>=1: print('\t\t\t\t\tCorrCoeffThreshold:','[',AbsCorrCoeff_threshold,']')

                                    self.__fit_transform_feat_eng_case__(X,
                                                              headers_dict,
                                                              path_feat_eng_dir,
                                                              format_,
                                                              Scaler_ID,
                                                              Imputer_cat_ID,
                                                              Imputer_iter_class_ID,
                                                              Imputer_cont_ID,
                                                              Imputer_iter_reg_ID,
                                                              OneHot_case,
                                                              AbsCorrCoeff_threshold)

                                    self.path_feat_eng_dirs.append(self.__path_feat_eng_base_dir__(path_feat_eng_dir, 
                                                                                                  OneHot_case,
                                                                                                  Scaler_ID,
                                                                                                  Imputer_cat_ID,
                                                                                                  Imputer_iter_class_ID,
                                                                                                  Imputer_cont_ID,
                                                                                                  Imputer_iter_reg_ID,
                                                                                                  AbsCorrCoeff_threshold))

                                    gc.collect()


        print('------------------------------------ !Finished! ------------------------------------')

    def transform(self, X_field):
        """
        Transform an arbitrary dataset of the same format as the X dataset passed in the fit method
        
        Arguments:
        ----------
            X_field: the dataset you wish to transform
        """
        import os, sys
        import pandas as pd
        
        import gc
        gc.collect()
        
        for key_header in ['categorical features', 'continuous features']:
            assert(key_header in self.headers_dict.keys()), 'headers_dict is missing the "'+key_header+'" key'
            
        X_field = X_field.copy()
        
        if self.verbose>=2: 
            print('\nX_field.info():')
            X_field.info()

        #Save the X and X_field data
        path_feat_eng_dir = self.path_feat_eng_root_dir 
        
        files=['X_field']
        if self.__feat_eng_files_saved__(files, path_feat_eng_dir, self.format_) == False or self.overwrite==True:
            self.save(X_field, 'X_field', self.format_, path_feat_eng_dir)
                
        #LabelEncode
        print('---------------------------- feat_eng_pipe transform ---------------------------')
        if self.verbose>=1: print('LabelEncode')
        X_field, path_feat_eng_dir = self.__transform_LabelEncode__(X_field,
                                                                    path_feat_eng_dir)
        
        self.path_feat_eng_dirs = []
        
        for Scaler_ID in self.Scalers_dict.keys():
            if self.verbose>=1: print('\tScale:',Scaler_ID)

            #Impute categorical features
            for Imputer_cat_ID in self.Imputer_categorical_dict.keys():
                
                for Imputer_iter_class_ID in self.Imputer_categorical_dict[Imputer_cat_ID].keys():
                    if self.verbose>=1: print('\t\tImpute Categorical Features:',
                                              Imputer_cat_ID,'[',Imputer_iter_class_ID,']')

                    #impute continuous features
                    for Imputer_cont_ID in self.Imputer_continuous_dict.keys():

                        for Imputer_iter_reg_ID in self.Imputer_continuous_dict[Imputer_cont_ID].keys():
                            
                            if self.verbose>=1: print('\t\t\tImpute Continuous Features:',
                                                      Imputer_cont_ID,'[',Imputer_iter_reg_ID,']')

                            for OneHot_case in self.OneHot_cases:
                                
                                if self.verbose>=1: print('\t\t\t\tOne Hot Encode:','[',OneHot_case,']')
                                    
                                for AbsCorrCoeff_threshold in self.AbsCorrCoeff_thresholds:

                                    if self.verbose>=1: print('\t\t\t\t\tCorrCoeffThreshold:','[',AbsCorrCoeff_threshold,']')

                                    self.__transform_feat_eng_case__(X_field,
                                                                      path_feat_eng_dir,
                                                                      Scaler_ID,
                                                                      Imputer_cat_ID,
                                                                      Imputer_iter_class_ID,
                                                                      Imputer_cont_ID,
                                                                      Imputer_iter_reg_ID,
                                                                      OneHot_case,
                                                                      AbsCorrCoeff_threshold)

                                    gc.collect()


        print('------------------------------------ !Finished! ------------------------------------')


        
        

