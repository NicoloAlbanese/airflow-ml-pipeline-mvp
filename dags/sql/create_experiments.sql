CREATE TABLE IF NOT EXISTS experiments (
    experiment_id SERIAL PRIMARY KEY,
    experiment_datetime VARCHAR NOT NULL,
    cv_folds NUMERIC NOT NULL,
    logreg_maxiter NUMERIC NOT NULL,
    max_pca_components NUMERIC NOT NULL,
    best_logreg_c NUMERIC NOT NULL,
    best_pca_components NUMERIC NOT NULL,
    test_set_accuracy NUMERIC NOT NULL
);