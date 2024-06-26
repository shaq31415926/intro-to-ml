import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(test_user_profile,
                        tinder_data,
                        number_recommendations=10):

    # index the user ids
    tinder_data = tinder_data.set_index("user_id")

    # get the gender preference of the user
    gender_preference = list(test_user_profile.sex)[0]

    # get the tinder data of the opposite
    td = tinder_data[tinder_data.sex == gender_preference]

    # Apply SVD to the training data
    svd = TruncatedSVD(n_components=20)
    # this is a matrix of all the profiles of the opposite gender
    tinder_profiles_matrix = svd.fit_transform(td)

    # we want to find profiles that are similar to the user
    # first we apply SVD
    test_profile_matrix = svd.transform(test_user_profile)
    # then calculate the cosine similarity between the user's profile and all other profiles of the opposite gender
    cosine_sim_new = cosine_similarity(test_profile_matrix, tinder_profiles_matrix)

    # convert the scores and select the top N
    scores = pd.DataFrame(cosine_sim_new.transpose())
    scores_ordered = scores.sort_values(by=[0], ascending=False)

    # get the index for top n
    users_index = list(scores_ordered.head(number_recommendations).index)

    # get the user names of the top
    tinder_data_manipulated = td.reset_index()
    user_ids = list(tinder_data_manipulated[tinder_data_manipulated.index.isin(users_index)].user_id)

    return user_ids