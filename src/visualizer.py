import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        self.point_cloud_counter = 0
        self.persistence_homology_counter = 0

    def plot_point_cloud(self, point_cloud):
        plt.figure()
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1])
        plt.title("Point Cloud")
        filename = f'point_cloud_{self.point_cloud_counter}.png'
        plt.savefig(filename)
        plt.close()
        self.point_cloud_counter += 1

    def plot_persistence_homology(self, persistence_data):
        plt.figure()
        colors = ['b', 'r']
        labels = ['H0', 'H1']

        for dim, dgms in enumerate(persistence_data):
            plt.scatter(dgms[:, 0], dgms[:, 1], c=colors[dim], label=labels[dim])

        plt.title("Persistence Diagram (H0 and H1)")
        plt.xlabel("Birth")
        plt.ylabel("Death")
        plt.legend()
        filename = f'persistence_diagram_combined_{self.persistence_homology_counter}.png'
        plt.savefig(filename)
        plt.close()
        self.persistence_homology_counter += 1

    def plot_normalized_wasserstein(self, wasserstein_dist, std_lifetimes1, std_lifetimes2):
        print("Wasserstein Distance:", wasserstein_dist)
        print("Standard Deviation of Lifetimes for Time Series 1:", std_lifetimes1)
        print("Standard Deviation of Lifetimes for Time Series 2:", std_lifetimes2)

        normalized_wasserstein1 = wasserstein_dist / std_lifetimes1
        normalized_wasserstein2 = wasserstein_dist / std_lifetimes2

        plt.figure()
        values = [normalized_wasserstein1, normalized_wasserstein2]
        labels = ["Normalized Wasserstein (TS1)", "Normalized Wasserstein (TS2)"]
        colors = ['b', 'g']

        plt.bar(labels, values, color=colors)
        plt.title("Normalized Wasserstein Distance")
        plt.ylabel("Normalized Distance")
        plt.savefig('normalized_wasserstein.png')
        plt.close()
