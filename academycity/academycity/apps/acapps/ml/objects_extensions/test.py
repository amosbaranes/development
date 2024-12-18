import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor


class Test(object):
    def __init__(self, dic):
        print("90567-8-000 Algo\n", dic, '\n', '-'*50)

    def test(self, dic):
        print(dic)

        # Generate synthetic data
        np.random.seed(42)
        X_inliers = np.random.normal(0, 1, (200, 2))  # Normal data
        X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))  # Outliers

        # print(X_inliers, "\n", X_outliers)

        # Combine normal data and outliers
        X = np.vstack((X_inliers, X_outliers))
        # print(X)

        # Fit the Local Outlier Factor model
        lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)  # 10% outliers
        y_pred = lof.fit_predict(X)  # -1 = outlier, 1 = inlier
        lof_scores = -lof.negative_outlier_factor_  # LOF scores

        print(lof)

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='coolwarm', edgecolor='k', s=50)
        plt.title("Local Outlier Factor (LOF) Anomaly Detection")
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.colorbar(label="Outlier/Normal (-1=Outlier, 1=Normal)")
        plt.show()

        # Print outlier points
        print("Outliers detected:")
        print(X[y_pred == -1])


        result = {"status": "ok"}
        return result