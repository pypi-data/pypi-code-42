
from . import LabelEncode
from . import Impute
from . import Scale
from . import OneHotEncode

class CorrelationCoeffThreshold():
    def __init__(self, 
                 AbsCorrCoeff_threshold = 0.99,
                 method='pearson'):
        """
        Method for filtering features with correlation coefficients >= the AbsCorrCoeff_threshold (absolute value of corerlation coeff. threshold) value passed
        
        Arguments:
        ----------
            AbsCorrCoeff_threshold: float. default = 0.99
            method: string. default: 'pearson'. The correlation coeffient method to be used 
                - pearson : standard correlation coefficient
                - kendall : Kendall Tau correlation coefficient
                - spearman : Spearman rank correlation
                - see pandas.DataFrame.corr for more details
        """
        assert(AbsCorrCoeff_threshold>=0)
        self.AbsCorrCoeff_threshold = AbsCorrCoeff_threshold
        self.method = method
        
    def fit(self, 
            df, CorrCoeff_features = 'auto'):
        """
        Fit the CorrelationCoeffThreshold object to the data
        
        Arguments:
        ----------
            df: the pandas dataframe of interest
            conv_features: list. the subset of features to analyze the covariance on. If 'auto' then all columns in the df will be used
        """
        import numpy as np
        
        #assigne self.CorrCoeff_features
        if CorrCoeff_features == 'auto':
            self.CorrCoeff_features = list(df.columns)
        else:
            assert(type(CorrCoeff_features)==type(list())), 'CorrCoeff_features must be "auto" or a list'
            self.CorrCoeff_features = CorrCoeff_features
        
        df = df.copy()
        df = df[self.CorrCoeff_features]
        
        df_cov = df.corr(method=self.method)
        
        self.dropped_features_dict = {'dropped feature':[],
                                 'correlated feature':[],
                                 'corr coeff':[]}
        for header in df_cov:
            slice_ = df_cov[header].drop([header]).reset_index()
            slice_.columns= ['header','corr coeff']
            for i in range(slice_.shape[0]):
                if str(slice_.iloc[i,:]['header']) not in self.dropped_features_dict['correlated feature']:
                    if np.abs(slice_.iloc[i,:]['corr coeff'])>= self.AbsCorrCoeff_threshold:
                        self.dropped_features_dict['dropped feature'].append(str(slice_.iloc[i,:]['header']))
                        self.dropped_features_dict['correlated feature'].append(header)
                        self.dropped_features_dict['corr coeff'].append(slice_.iloc[i,:]['corr coeff'])
                        
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
        
        if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
            sys.path.insert(0,  os.path.dirname(os.path.abspath(os.path.join(__file__,'..','..'))))
        from ... import file_utils
        
        self.save = file_utils.save
        self.load = file_utils.load
        
    def __feat_eng_files_saved__(self,
                                 path_feat_eng_dir, 
                                 format_ ,
                                 find_X_field):
        """
        Check if feat eng files are save for the specific case directory passed. Returns False if the X
        """
        import os, sys
        import gc
        
        gc.collect()

        feat_eng_files_saved=False

        #build list of files to look for
        files = ['X.'+format_, 'X_field.'+format_]

        #drop the X_field file from the list if find_X_filed==False
        if find_X_field==False:
            files = [file for file in files if 'X_field' not in file]

        #check if all files exist
        for file in files:
            if format_ == 'h5_csv':
                for format_ in ['csv','h5']:
                    path_save_file = os.path.join(path_feat_eng_dir,file.replace('h5_csv',format_)) #replace csv or h5
                    if os.path.isfile(path_save_file)==True:
                        feat_eng_files_saved = True
            else:
                path_save_file = os.path.join(path_feat_eng_dir,file)
                if os.path.isfile(path_save_file)==True:
                    feat_eng_files_saved = True
        
        gc.collect()

        return feat_eng_files_saved      
            
    def __run_LabelEncode__(self,
                            X, X_field, 
                            path_feat_eng_dir,
                            headers_dict,
                            format_,
                            find_X_field):
        import os, sys
        import gc
        
        gc.collect()

        #label encode X
        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'LabelEncode')
        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field)==False or self.overwrite==True or self.overwrite=='LabelEncode':
            LabelEncoder = LabelEncode.categorical_features()
            LabelEncoder.fit(X, categorical_headers=headers_dict['categorical features'])

            X = LabelEncoder.transform(X)
            
            #label encode field data
            if type(X_field) != type(None): 
                X_field = LabelEncoder.transform(X_field)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): self.save(X_field, 'X_field', format_, path_feat_eng_dir)
            
            self.LabelEncoder = LabelEncoder
            
            #save the encoder
            self.save(LabelEncoder, 'LabelEncoder', 'dill', path_feat_eng_dir)

        else: 
            X = self.load('X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): X_field = self.load('X_field', format_, path_feat_eng_dir)
        
        gc.collect()
        return X, X_field, path_feat_eng_dir
                
        
    def __run_Scale__(self,
                      X, X_field, 
                        path_feat_eng_dir,
                        headers_dict,
                        format_,
                        find_X_field,
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

        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field)==False or self.overwrite==True:

            Scaler = Scale.continuous_features(Scaler = self.Scalers_dict[Scaler_ID])
            Scaler.fit(X, headers_dict['continuous features'])
            X = Scaler.transform(X)

            if type(X_field) != type(None):
                X_field = Scaler.transform(X_field)

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): self.save(X_field, 'X_field', format_, path_feat_eng_dir)
                
            #save the Scaler
            self.save(Scaler, 'Scaler', 'dill', path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                          'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                          'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']')
            if self.__feat_eng_files_saved__(path_next_step, format_, find_X_field)==False:
                X = self.load('X', format_, path_feat_eng_dir)
                if type(X_field) != type(None): X_field = self.load('X_field', format_, path_feat_eng_dir)
        
        gc.collect()

        return X, X_field, path_feat_eng_dir


    def __run_Impute_categorical__(self,
                                   X, X_field, 
                                  path_feat_eng_dir,
                                  headers_dict,
                                  format_,
                                  find_X_field,
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
        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field)==False or self.overwrite==True:

            X, Imputer = Impute.categorical_features(X, 
                                                    headers_dict['categorical features'], 
                                                    strategy = Imputer_cat_ID, 
                                                    estimator = self.Imputer_categorical_dict[Imputer_cat_ID][Imputer_iter_class_ID],
                                                    verbose= 0)

            if type(X_field) != type(None):
                X_field[headers_dict['categorical features']] = Imputer.transform(X_field[headers_dict['categorical features']])

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): self.save(X_field, 'X_field', format_, path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir, 
                                          'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                          'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']')
            if self.__feat_eng_files_saved__(path_next_step, format_, find_X_field)==False:
                X = self.load('X', format_, path_feat_eng_dir)
                if type(X_field) != type(None): X_field = self.load('X_field', format_, path_feat_eng_dir)
        
        gc.collect()

        return X, X_field, path_feat_eng_dir
        
        
    def __run_Impute_continuous__(self,
                                  X, X_field, 
                                  path_feat_eng_dir,
                                  headers_dict,
                                  format_,
                                  find_X_field,
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
        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field)==False or self.overwrite==True:

            X, Imputer = Impute.continuous_features(X, 
                                        headers_dict['continuous features'], 
                                        strategy = Imputer_cont_ID, 
                                        estimator = self.Imputer_continuous_dict[Imputer_cont_ID][Imputer_iter_reg_ID],
                                        verbose= 0)

            if type(X_field) != type(None):
                X_field[headers_dict['continuous features']] = Imputer.transform(X_field[headers_dict['continuous features']])

            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): self.save(X_field, 'X_field', format_, path_feat_eng_dir)

        else:
            #check if the step after this has been completed, if not load the data here
            path_next_step = os.path.join(path_feat_eng_dir,'OneHot_case['+str(OneHot_case)+']')
            if self.__feat_eng_files_saved__(path_next_step, format_, find_X_field)==False or self.overwrite=='OneHot':
                X = self.load('X', format_, path_feat_eng_dir)
                if type(X_field) != type(None): X_field = self.load('X_field', format_, path_feat_eng_dir)
                    
                if format_ != 'csv':
                    import pandas as pd
                    headers_dict = self.load('headers_dict', 'json', self.path_feat_eng_root_dir)
                    X = pd.DataFrame(X, columns = headers_dict['features'])
                    if type(X_field) != type(None): X_field = pd.DataFrame(X_field, columns = headers_dict['features'])
        
        gc.collect()
        
        return X, X_field, path_feat_eng_dir

    def __run_OneHot_Encode__(self,
                              X, X_field, 
                              path_feat_eng_dir,
                              headers_dict,
                              format_,
                              find_X_field,
                              OneHot_case):
        """
        OneHotEncode, transform, and save the categorical data
        """
        import os, sys
        import numpy as np
        import gc
        
        gc.collect()

        path_feat_eng_dir = os.path.join(path_feat_eng_dir, 'OneHot_case['+str(OneHot_case)+']')

        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field)==False or self.overwrite==True or self.overwrite=='OneHot' or self.overwrite == 'OneHotEncode' or self.overwrite == 'OneHot_Encode':

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

                #label encode field data
                if type(X_field) != type(None): 
                    X_field = OneHotEncoder.transform(X_field)
                
                #save the encoder
                self.save(OneHotEncoder, 'OneHotEncoder', 'dill', path_feat_eng_dir)

            else: #if OneHot is False, just skip transform to numpy array
                headers_dict['headers after OneHot'] = list(X.columns)
                X = np.array(X)
                if type(X_field) != type(None): X_field = np.array(X_field) 
                    
            #save
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): self.save(X_field, 'X_field', format_, path_feat_eng_dir)
            
            self.save(headers_dict, 'headers_dict', 'json', path_feat_eng_dir)
            
        else:
            #load
            X = self.load('X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): X_field = self.load('X_field', format_, path_feat_eng_dir)
                
            headers_dict = self.load('headers_dict', 'json', path_feat_eng_dir)
            
        gc.collect()

        return X, X_field, path_feat_eng_dir, headers_dict
    
    def __path_feat_eng_base_dir__(self, path_feat_eng_dir, 
                                         OneHot_case,
                                          Scaler_ID,
                                          Imputer_cat_ID,
                                          Imputer_iter_class_ID,
                                          Imputer_cont_ID,
                                          Imputer_iter_reg_ID):
        import os
        path_feat_eng_base_dir = os.path.join(path_feat_eng_dir,
                                  'Scaler_ID['+Scaler_ID+']',
                                  'Imputer_categorical_ID['+Imputer_cat_ID+']',
                                  'Imputer_iterator_classifier_ID['+str(Imputer_iter_class_ID)+']',
                                  'Imputer_continuous_ID['+Imputer_cont_ID+']',
                                  'Imputer_iterator_regressor_ID['+str(Imputer_iter_reg_ID)+']',
                                  'OneHot_case['+str(OneHot_case)+']')
        return path_feat_eng_base_dir

    def __run_feat_eng_case__(self,
                              X, X_field,
                              headers_dict,
                              path_feat_eng_dir,
                              format_,
                              find_X_field,
                              Scaler_ID,
                              Imputer_cat_ID,
                              Imputer_iter_class_ID,
                              Imputer_cont_ID,
                              Imputer_iter_reg_ID,
                              OneHot_case):
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
                                                                  Imputer_iter_reg_ID)
        
        if os.path.isdir(path_feat_eng_base_dir)==False:
            os.makedirs(path_feat_eng_base_dir)

        #check if all the required files are saved in the base directory
        all_data_previously_saved = True
        for filename in ['X', 'X_field', 'headers_dict.json']:

            if 'headers_dict' not in filename:
                filename = filename+'.'+format_

            path_save_file = os.path.join(path_feat_eng_base_dir, filename)
            if os.path.isfile(path_save_file)==False:
                all_data_previously_saved = False

        if all_data_previously_saved==False or self.overwrite == True: 

            X = X.copy()
            if type(X_field) != type(None): X_field = X_field.copy()
            headers_dict = headers_dict.copy()

            ####### Scale #########
            X, X_field, path_feat_eng_dir = self.__run_Scale__(X, X_field, 
                                                            path_feat_eng_dir,
                                                            headers_dict,
                                                            format_,
                                                            find_X_field,
                                                            Scaler_ID,
                                                            Imputer_cat_ID,
                                                            Imputer_iter_class_ID)
            ####### Impute Categorical Features #########
            X, X_field, path_feat_eng_dir = self.__run_Impute_categorical__(X, X_field, 
                                                              path_feat_eng_dir,
                                                              headers_dict,
                                                              format_,
                                                              find_X_field,
                                                              Imputer_cat_ID,
                                                              Imputer_iter_class_ID,
                                                              Imputer_cont_ID,
                                                              Imputer_iter_reg_ID)

            ###### Impute Continuous Features ########
            X, X_field, path_feat_eng_dir = self.__run_Impute_continuous__(X, X_field, 
                                                                      path_feat_eng_dir,
                                                                      headers_dict,
                                                                      format_,
                                                                      find_X_field,
                                                                      Imputer_cont_ID,
                                                                      Imputer_iter_reg_ID,
                                                                      OneHot_case)

            ##### One Hot Encode #####
            X, X_field, path_feat_eng_dir, headers_dict = self.__run_OneHot_Encode__(X, X_field, 
                                                                                      path_feat_eng_dir,
                                                                                      headers_dict,
                                                                                      format_,
                                                                                      find_X_field,
                                                                                      OneHot_case)
            
            assert(path_feat_eng_base_dir == path_feat_eng_dir)

            del X, X_field
            gc.collect()
            
        else:
            if self.verbose>=2: print('pre-existing saved data found at path_feat_eng_dir:', path_feat_eng_base_dir)
        
    def fit(self,
            X, 
            X_field = None,
            headers_dict = None,
            format_ = 'csv'):
        """
        Run standard feature engineering processes on data.
        Arguments:
            X: pandas dataframe. The train and test set features which will be engineered
            X_field: pandas dataframe. The field data (label is unknown) features which will be transformed after fitting on the X dataset.
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
        if type(X_field) != type(None): 
            X_field = X_field.copy()
            find_X_field = True
        else:
            find_X_field = False
        headers_dict = headers_dict.copy()
        
        self.format_ = format_ 
        
        #ensure only the features identified in the headers dict are passed
        assert(X[headers_dict['categorical features']+headers_dict['continuous features']].shape[1] == X.shape[1]), 'The headers in X do not match the contiuous and categorical headers in the headers_dict'
        
        if type(X_field) != type(None): 
            assert(X_field[headers_dict['categorical features']+headers_dict['continuous features']].shape[1] == X_field.shape[1]), 'The headers in X_field do not match the contiuous and categorical headers in the headers_dict'
        
        if self.verbose>=2: 
            print('X.info():')
            X.info()
            if type(X_field) != type(None):
                print('\nX_field.info():')
                X_field.info()
            
        #Save the X and X_field data
        path_feat_eng_dir = self.path_feat_eng_root_dir 
        if self.__feat_eng_files_saved__(path_feat_eng_dir, format_, find_X_field) == False or self.overwrite==True:
            self.save(X, 'X', format_, path_feat_eng_dir)
            if type(X_field) != type(None): 
                self.save(X_field, 'X_field', format_, path_feat_eng_dir)
                
        #save the original headers dict
        headers_dict['features'] = list(X.columns)
        self.save(headers_dict,  'headers_dict', 'json', self.path_feat_eng_root_dir)
            
            
        #LabelEncode
        print('-------------------------------- fit feat_eng_pipe --------------------------------')
        if self.verbose>=1: print('LabelEncode')
        X, X_field, path_feat_eng_dir = self.__run_LabelEncode__(X, X_field, 
                                                path_feat_eng_dir,
                                                headers_dict,
                                                format_,
                                                find_X_field)
        
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

                                self.__run_feat_eng_case__(X, X_field,
                                                          headers_dict,
                                                          path_feat_eng_dir,
                                                          format_,
                                                          find_X_field,
                                                          Scaler_ID,
                                                          Imputer_cat_ID,
                                                          Imputer_iter_class_ID,
                                                          Imputer_cont_ID,
                                                          Imputer_iter_reg_ID,
                                                          OneHot_case)
                                
                                self.path_feat_eng_dirs.append(self.__path_feat_eng_base_dir__(path_feat_eng_dir, 
                                                                                              OneHot_case,
                                                                                              Scaler_ID,
                                                                                              Imputer_cat_ID,
                                                                                              Imputer_iter_class_ID,
                                                                                              Imputer_cont_ID,
                                                                                              Imputer_iter_reg_ID))
                                
                                gc.collect()


        print('------------------------------------ !Finished! ------------------------------------')


