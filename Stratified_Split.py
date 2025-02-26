import random
import math
import torch.utils.data
from collections import defaultdict
import pandas
import sklearn
from sklearn import preprocessing
import torch


class StratifiedSplit:
    def __init__(self, dataset: torch.utils.data.Dataset, labels):
        """
        dataset : torch.utils.data.Dataset 
        Label : list
        """
        self.dataset = dataset
        self.labels = labels

    def test_eval_stratified_split(self, testfraction, evalfraction, random_state=None):
        if random_state:
            random.seed(random_state)
        indices_per_label = defaultdict(list)

        """
        defaultdict(list) -> dictionary with values' type as list
        default dict helps with avoiding KeyError. If any key is absent , it gives output as "NOT PRESENT"
        """

        for index, label in enumerate(self.labels):
            indices_per_label[label].append(index)
            """ indices_per_label stores each label as key and list of it's indexes in LABELS list as value """

        test_set_indices, train_set_indices, eval_set_indices = list(), list(), list()

        for label, indices in indices_per_label.items():
            n_samples_for_label_test = round(len(indices) * testfraction)
            n_samples_for_label_eval = round(len(indices) * evalfraction)
            random_indices_sample_test = random.sample(
                indices, n_samples_for_label_test)
            random_indices_sample_eval = random.sample(
                set(indices)-set(random_indices_sample_test), n_samples_for_label_eval)
            test_set_indices.extend(random_indices_sample_test)
            eval_set_indices.extend(random_indices_sample_eval)
            train_set_indices.extend(
                set(indices) - set(random_indices_sample_test)-set(random_indices_sample_eval))
            """
            n_samples_for_label_test , n_samples_for_label_eval = rounded number of data points from total data points for each label
            random.sample() picks out random "n_samples" from the list of indices for each label
            Then these random indices are added in the test_indices/eval_indices
            """

        test_set_inputs = torch.utils.data.Subset(
            self.dataset, test_set_indices)
        test_set_labels = list(map(self.labels.__getitem__, test_set_indices))
        """ 
            torch.utils.data.Subset -> returns Subset of a dataset at specified indices. 
            labels.__getitem__ -> The magic method __getitem__ is basically used for accessing list items, dictionary entries, array elements etc. It returns the label at specific index
        """
        eval_set_inputs = torch.utils.data.Subset(
            self.dataset, eval_set_indices)
        eval_set_labels = list(map(self.labels.__getitem__, eval_set_indices))
        train_set_inputs = torch.utils.data.Subset(
            self.dataset, train_set_indices)
        train_set_labels = list(
            map(self.labels.__getitem__, train_set_indices))
        return train_set_inputs, train_set_labels, eval_set_inputs, eval_set_labels, test_set_inputs, test_set_labels 

    def test_stratified_split(self, testfraction, random_state=None):
        if random_state:
            random.seed(random_state)
        indices_per_label = defaultdict(list)
        for index, label in enumerate(self.labels):
            indices_per_label[label].append(index)
        test_set_indices, train_set_indices = list(), list()
        for label, indices in indices_per_label.items():
            n_samples_for_label = round(len(indices) * testfraction)
            random_indices_sample = random.sample(indices, n_samples_for_label)
            test_set_indices.extend(random_indices_sample)
            train_set_indices.extend(set(indices) - set(random_indices_sample))
        test_set_inputs = torch.utils.data.Subset(
            self.dataset, test_set_indices)
        test_set_labels = list(map(self.labels.__getitem__, test_set_indices))
        train_set_inputs = torch.utils.data.Subset(
            self.dataset, train_set_indices)
        train_set_labels = list(
            map(self.labels.__getitem__, train_set_indices))
        return train_set_inputs, train_set_labels, test_set_inputs, test_set_labels


# _____________________________________________EXAMPLE__________________________________________________
if __name__ == '__main__':
    "link for creditcard.scv -> https://www.kaggle.com/mlg-ulb/creditcardfraud"
    df = pandas.read_csv('/home/ntlpt-52/Downloads/creditcard.csv')
    inputs = df.iloc[:, :-1].values
    labels = df.iloc[:, -1].values
    sc = preprocessing.StandardScaler()
    torch_inputs = sc.fit_transform(inputs)
    torch_inputs = torch.from_numpy(torch_inputs).float()
    torch_labels = torch.from_numpy(labels).float()
    dataset = torch.utils.data.TensorDataset(torch_inputs, torch_labels)
    # split dataset into training-, testing- and validation set
    split_object= StratifiedSplit(dataset,labels)
    train_data, train_labels, test_data, _ = split_object.test_stratified_split(testfraction=0.1, random_state=1)

    split_object2 = StratifiedSplit(train_data, train_labels)
    train_data, train_labels, eval_data, _ = split_object.test_stratified_split( testfraction=0.1, random_state=1)


