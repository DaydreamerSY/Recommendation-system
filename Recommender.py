import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import cdist


class Recommender:
    """
    Credit:
        This class is made for the specific project named DACNTT2, and can not be applied
        to another project without modifying source.

    Required Packages:
        pandas==1.4.2
        joblib==1.1.0
        sklearn==1.1.0
        scipy==1.8.0

    Input/Attributes:
        user_data <- pandas.DataFrame() : User's last visited post.
        database <- pandas.DataFrame() : DataFrame of all posts.
        cal_cols <- list: List of columns will be calculate in class.
        based_on <- string: Name of column that will be filtered, first priority
            to sort, should be "region".
        sort_by <- string: Name of column that will be sort by, should be "id".
        scaler <- joblib.load(): Scaler, should be 'MinMaxScaler' from 'sklearn' package,
                                save scaler with:
                                    import joblib
                                    joblib.dump(scaler, "MinMaxScalerModel.gz")
                                for loading scaler, see example code at the end of file.
        top <- int: Number of item head of returned result.

    Output/Methods:
        get_recommended():
            recommened_posts <- pandas.DataFrame(): Contains recommended posts similar
            to user_data.

    Algorithm:
        This class uses Euclidean Distance to calculate the distance between 'user_data' and
        each post in 'database', then found out which posts are most similar to 'user_data'.

    Advantages:
        No need for data on other users when applying to similar users.
        Able to recommend to users with unique tastes.
        Able to recommend most for specific location (based on 'region').

    Disadvantages:
        Does not recommend items outside the user profile.

    Troubleshoot:
        Add hottest item and most popular item to recommended list while using this algorithm.
    """

    def __init__(
        self, user_data, database, cal_cols, based_on, sort_by, scaler, top=None
    ) -> None:
        """
        user_data: last visited post of users
        database:
        """
        self.scaler = scaler
        self.user_last_visited = user_data.copy()
        self.database = database.copy()
        self.cal_cols = cal_cols
        self.based_on = based_on
        self.sort_by = sort_by
        self.nlargest = top
        pass

    def get_recommended(self):
        # Create a copy of each working dataframe, make sure
        # they don't affect outside dataframe of this class,
        # in this case is self.database because we'll use self.database
        # for result.
        self.cal_database = self.database.copy()

        # Apply scaler transform to self.cal_database and
        # self.user_last_visited for normalizing data.
        self.cal_database[self.cal_cols] = self.scaler.transform(
            self.database[self.cal_cols]
        )
        self.user_last_visited[self.cal_cols] = self.scaler.transform(
            self.user_last_visited[self.cal_cols]
        )

        # Filter base on "region" because this is most priority attribute.
        last_visited_region = self.user_last_visited[self.based_on][0]
        data_same_region = self.cal_database[
            self.cal_database[self.based_on] == last_visited_region
        ].copy()

        # Apply Euclidean for calculate distance data_same_region.
        # and self.user_last_visited
        data_same_region["score"] = cdist(
            data_same_region[self.cal_cols],
            self.user_last_visited[self.cal_cols],
            metric="euclidean",
        )

        # Extract sorted "id" (self.sort_by) to list.
        df_result = data_same_region.sort_values("score", ascending=True)
        recommended_id = df_result[self.sort_by].values.tolist()

        # Try to remove last visited post's id from database to prevents.
        # this will be most similar
        visited_id = self.user_last_visited[self.sort_by].values.tolist()[0]
        try:
            recommended_id.remove(visited_id)
        except:
            pass

        # Create pandas.DataFrame() contains most similar posts from user's data.
        recommended_posts = pd.DataFrame(columns=self.cal_database.columns)

        for ordered_id in recommended_id:
            recommended_posts = pd.concat(
                [
                    recommended_posts,
                    self.database[self.database[self.sort_by] == ordered_id],
                ],
                ignore_index=True,
            )

        # Get top nlargest item.
        if not self.nlargest == None:
            return recommended_posts.head(self.nlargest)

        return recommended_posts


# if __name__ == "__main__":
#     database = pd.read_csv("data.csv")

#     user_last_visited = pd.DataFrame(
#         {
#             "id": [90],
#             "region": ["Bảo Lâm"],
#             "area_by_m2": [90],
#             "width_of_facade": [5],
#             "width_of_road": [5],
#             "is_legal": [0],
#             "price": [2],
#         }
#     )

#     scaler = joblib.load("MinMaxScalerModel.gz")
#     cal_cols = ["area_by_m2", "width_of_facade", "width_of_road", "is_legal", "price"]
#     based_on = ["id"]

#     recommender = Recommender(
#         user_data=user_last_visited,
#         database=database,
#         cal_cols=cal_cols,
#         based_on="region",
#         sort_by="id",
#         scaler=scaler,
#         top=5,
#     )

#     print(recommender.get_recommended())
