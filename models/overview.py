# Standard Library

# Third Party Library
# import lazypredict
# from lazypredict.Supervised import LazyClassifier, LazyRegressor

# Local Library

# Logger
logger = setup_logger("Data Analysis")



def setup_modeling_info(x, y, test_size, random_state, shuffle=False, stratify=False, classify = False, regressor= False):
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    import seaborn as sns
    logger.info(f"Training data shape: {x.shape}")
    logger.info(f"Target variable shape: {y.shape}")
    logger.info(f"Train Test Split with ")   
    x_train, y_train, x_test, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state, stratify= stratify, shuffle=shuffle)

    if classify == True:
        logger.info("Testing Classifier models...")
        clf = LazyClassifier(verbose=True)
        model_train, prediction_train = clf.fit(x_train, y_train)
        model_test, prediction_test = clf.fit(x_test, y_test)


        plt.figure(figsize=(10, 5))
        # sns.set_theme(style="whitegrid")
        plt.title("Classifier Model Training Results")
        ax = sns.barplot(x=model_train.index, y="Accuracy", data=model_train)
        # plt.xticks(rotation=90)
        plt.title("Classifier Model Test Results")
        ax2 = sns.barplot(x=model_test.index, y="Accuracy", data=model_test)
        plt.show()


    elif regressor == True:
        from lazypredict.Supervised import LazyRegressor
        logger.info("Testing regressors...")
        reg = LazyRegressor()
        model_train_reg, prediction_train_reg = reg.fit(x_train, y_train)
        model_train_reg["R2"] = [0 if i < 0 else i for i in model_train.iloc[:,0] ]
        model_test_reg, prediction_test_reg = reg.fit(x_test, y_test)
        model_test_reg["R2"] = [0 if i < 0 else i for i in model_train.iloc[:,0] ]
        plt.figure(figsize=(10, 5))
        # sns.set_theme(style="whitegrid")
        plt.title("Regressor Model Training Results")
        ax = sns.barplot(x=model_train_reg.index, y="R2", data=model_train_reg)
        # plt.xticks(rotation=90)
        ax.set(ylim=(0,1))
        plt.title("Regressor Model Test Results")
        ax2 = sns.barplot(x=model_test_reg.index, y="R2", data=model_test_reg)
        plt.show()


    return x_train, y_train, x_test, y_test, model_train, model_test, model_train_reg, model_test_reg, prediction_train, prediction_test, prediction_train_reg, prediction_test_reg