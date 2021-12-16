import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from utils.files_util import save_files, load_files
import utils.ml_pipeline_config as config


def experiment():

    x_train, x_test, y_train, y_test = load_files(['x_train', 'x_test', 'y_train', 'y_test'])
    
    # the maximum number of principal components to investigate cannot be higher than the number of coolumns in the dataset 
    max_pca_components = config.params["max_pca_components"] if config.params["max_pca_components"] <= x_train.shape[1] else x_train.shape[1]
    cv_folds = config.params["cv_folds"] 
    logreg_maxiter = config.params["logreg_maxiter"]

    # pipeline definition
    std_scaler = StandardScaler()
    pca = PCA(max_pca_components-1)
    log_reg = LogisticRegression(max_iter=logreg_maxiter)

    pipe = Pipeline(steps=[('std_scaler', std_scaler),
                        ('pca', pca), 
                        ('log_reg', log_reg)])

    # parameters for hyper-parameter tuning
    params = {
        'pca__n_components': list(range(1, max_pca_components)),
        'log_reg__C': np.logspace(0.05, 0.1, 1)
    }

    # cross-validated training through grid search
    grid_search = GridSearchCV(pipe, params, cv=cv_folds)
    grid_search.fit(x_train, y_train)

    # selection of the best parameters 
    best_c = round(grid_search.best_params_.get("log_reg__C"),2)
    best_princ_comp = grid_search.best_params_.get("pca__n_components")
    
    # performances on test set
    y_test_predicted = grid_search.best_estimator_.predict(x_test)
    test_set_accuracy = round(accuracy_score(y_test, y_test_predicted),3)

    # save esperiments information for historical persistence
    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    exp_info = pd.DataFrame([[now,
                          cv_folds,
                          logreg_maxiter,
                          max_pca_components,
                          best_c,
                          best_princ_comp,
                          test_set_accuracy]],
                          columns=['experiment_datetime',
                                   'cv_folds',
                                   'logreg_maxiter',
                                   'max_pca_components', 
                                   'best_logreg_c',
                                   'best_pca_components',
                                   'test_set_accuracy'
                                   ])
    exp_info.name = 'exp_info'

    save_files([exp_info])
