from sklearn.preprocessing import MinMaxScaler # scale the data


def scale_features(features_df):
    """Definition to scale the data"""
    
    min_max_scaler = MinMaxScaler(feature_range=(-1, 1))
    features_scaled = min_max_scaler.fit_transform(features_df)
    
    return features_scaled