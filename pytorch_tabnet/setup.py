# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_tabnet']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0',
 'scikit_learn>0.21',
 'scipy>1.4',
 'torch>=1.2,<2.0',
 'tqdm>=4.36,<5.0']

setup_kwargs = {
    'name': 'pytorch-tabnet',
    'version': '3.1.1',
    'description': 'PyTorch implementation of TabNet',
    'long_description': '# README\n\n# TabNet : Attentive Interpretable Tabular Learning\n\nThis is a pyTorch implementation of Tabnet (Arik, S. O., & Pfister, T. (2019). TabNet: Attentive Interpretable Tabular Learning. arXiv preprint arXiv:1908.07442.) https://arxiv.org/pdf/1908.07442.pdf.\n\n[![CircleCI](https://circleci.com/gh/dreamquark-ai/tabnet.svg?style=svg)](https://circleci.com/gh/dreamquark-ai/tabnet)\n\n[![PyPI version](https://badge.fury.io/py/pytorch-tabnet.svg)](https://badge.fury.io/py/pytorch-tabnet)\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pytorch-tabnet)\n\nAny questions ? Want to contribute ? To talk with us ? You can join us on [Slack](https://join.slack.com/t/mltooling/shared_invite/zt-fxaj0qk7-SWy2_~EWyhj4x9SD6gbRvg)\n\n# Installation\n\n## Easy installation\nYou can install using pip by running:\n`pip install pytorch-tabnet`\n\n## Source code\nIf you wan to use it locally within a docker container:\n\n- `git clone git@github.com:dreamquark-ai/tabnet.git`\n\n- `cd tabnet` to get inside the repository\n\n-----------------\n#### CPU only\n- `make start` to build and get inside the container\n\n#### GPU\n- `make start-gpu` to build and get inside the GPU container\n\n-----------------\n- `poetry install` to install all the dependencies, including jupyter\n\n- `make notebook` inside the same terminal. You can then follow the link to a jupyter notebook with tabnet installed.\n\n# What problems does pytorch-tabnet handles?\n\n- TabNetClassifier : binary classification and multi-class classification problems\n- TabNetRegressor : simple and multi-task regression problems\n- TabNetMultiTaskClassifier:  multi-task multi-classification problems\n\n# How to use it?\n\nTabNet is now scikit-compatible, training a TabNetClassifier or TabNetRegressor is really easy.\n\n```python\nfrom pytorch_tabnet.tab_model import TabNetClassifier, TabNetRegressor\n\nclf = TabNetClassifier()  #TabNetRegressor()\nclf.fit(\n  X_train, Y_train,\n  eval_set=[(X_valid, y_valid)]\n)\npreds = clf.predict(X_test)\n```\n\nor for TabNetMultiTaskClassifier :\n\n```python\nfrom pytorch_tabnet.multitask import TabNetMultiTaskClassifier\nclf = TabNetMultiTaskClassifier()\nclf.fit(\n  X_train, Y_train,\n  eval_set=[(X_valid, y_valid)]\n)\npreds = clf.predict(X_test)\n```\n\nThe targets on `y_train/y_valid` should contain a unique type (i.e. they must all be strings or integers).\n\n### Default eval_metric\n\nA few classical evaluation metrics are implemented (see bellow section for custom ones):\n- binary classification metrics : \'auc\', \'accuracy\', \'balanced_accuracy\', \'logloss\'\n- multiclass classification : \'accuracy\', \'balanced_accuracy\', \'logloss\'\n- regression: \'mse\', \'mae\', \'rmse\', \'rmsle\'\n\n\nImportant Note : \'rmsle\' will automatically clip negative predictions to 0, because the model can predict negative values.\nIn order to match the given scores, you need to use `np.clip(clf.predict(X_predict), a_min=0, a_max=None)` when doing predictions.\n\n\n### Custom evaluation metrics\n\nIt\'s easy to create a metric that matches your specific need. Here is an example for gini score (note that you need to specifiy whether this metric should be maximized or not):\n\n```python\nfrom pytorch_tabnet.metrics import Metric\nfrom sklearn.metrics import roc_auc_score\n\nclass Gini(Metric):\n    def __init__(self):\n        self._name = "gini"\n        self._maximize = True\n\n    def __call__(self, y_true, y_score):\n        auc = roc_auc_score(y_true, y_score[:, 1])\n        return max(2*auc - 1, 0.)\n\nclf = TabNetClassifier()\nclf.fit(\n  X_train, Y_train,\n  eval_set=[(X_valid, y_valid)],\n  eval_metric=[Gini]\n)\n\n```\n\nA specific customization example notebook is available here : https://github.com/dreamquark-ai/tabnet/blob/develop/customizing_example.ipynb\n\n# Semi-supervised pre-training\n\nAdded later to TabNet\'s original paper, semi-supervised pre-training is now available via the class `TabNetPretrainer`:\n\n```python\n# TabNetPretrainer\nunsupervised_model = TabNetPretrainer(\n    optimizer_fn=torch.optim.Adam,\n    optimizer_params=dict(lr=2e-2),\n    mask_type=\'entmax\' # "sparsemax"\n)\n\nunsupervised_model.fit(\n    X_train=X_train,\n    eval_set=[X_valid],\n    pretraining_ratio=0.8,\n)\n\nclf = TabNetClassifier(\n    optimizer_fn=torch.optim.Adam,\n    optimizer_params=dict(lr=2e-2),\n    scheduler_params={"step_size":10, # how to use learning rate scheduler\n                      "gamma":0.9},\n    scheduler_fn=torch.optim.lr_scheduler.StepLR,\n    mask_type=\'sparsemax\' # This will be overwritten if using pretrain model\n)\n\nclf.fit(\n    X_train=X_train, y_train=y_train,\n    eval_set=[(X_train, y_train), (X_valid, y_valid)],\n    eval_name=[\'train\', \'valid\'],\n    eval_metric=[\'auc\'],\n    from_unsupervised=unsupervised_model\n)\n```\n\nThe loss function has been normalized to be independent of `pretraining_ratio`, `batch_size` and number of features in the problem.\nA self supervised loss greater than 1 means that your model is reconstructing worse than predicting the mean for each feature, a loss bellow 1 means that the model is doing better than predicting the mean.\n\nA complete example can be found within the notebook `pretraining_example.ipynb`.\n\n/!\\ : current implementation is trying to reconstruct the original inputs, but Batch Normalization applies a random transformation that can\'t be deduced by a single line, making the reconstruction harder. Lowering the `batch_size` might make the pretraining easier.\n\n\n# Useful links\n\n- [explanatory video](https://youtu.be/ysBaZO8YmX8)\n- [binary classification examples](https://github.com/dreamquark-ai/tabnet/blob/develop/census_example.ipynb)\n- [multi-class classification examples](https://github.com/dreamquark-ai/tabnet/blob/develop/forest_example.ipynb)\n- [regression examples](https://github.com/dreamquark-ai/tabnet/blob/develop/regression_example.ipynb)\n- [multi-task regression examples](https://github.com/dreamquark-ai/tabnet/blob/develop/multi_regression_example.ipynb)\n- [multi-task multi-class classification examples](https://www.kaggle.com/optimo/tabnetmultitaskclassifier)\n- [kaggle moa 1st place solution using tabnet](https://www.kaggle.com/c/lish-moa/discussion/201510)\n\n## Model parameters\n\n- `n_d` : int (default=8)\n\n    Width of the decision prediction layer. Bigger values gives more capacity to the model with the risk of overfitting.\n    Values typically range from 8 to 64.\n\n- `n_a`: int (default=8)\n\n    Width of the attention embedding for each mask.\n    According to the paper n_d=n_a is usually a good choice. (default=8)\n\n- `n_steps` : int (default=3)\n\n    Number of steps in the architecture (usually between 3 and 10)  \n\n- `gamma` : float  (default=1.3)\n\n    This is the coefficient for feature reusage in the masks.\n    A value close to 1 will make mask selection least correlated between layers.\n    Values range from 1.0 to 2.0.\n\n- `cat_idxs` : list of int (default=[] - Mandatory for embeddings) \n\n    List of categorical features indices.\n\n- `cat_dims` : list of int (default=[] - Mandatory for embeddings)\n\n    List of categorical features number of modalities (number of unique values for a categorical feature)\n    /!\\ no new modalities can be predicted\n\n- `cat_emb_dim` : list of int (optional)\n\n    List of embeddings size for each categorical features. (default =1)\n\n- `n_independent` : int  (default=2)\n\n    Number of independent Gated Linear Units layers at each step.\n    Usual values range from 1 to 5.\n\n- `n_shared` : int (default=2)\n\n    Number of shared Gated Linear Units at each step\n    Usual values range from 1 to 5\n\n- `epsilon` : float  (default 1e-15)\n\n    Should be left untouched.\n\n- `seed` : int (default=0)\n\n    Random seed for reproducibility\n\n- `momentum` : float\n\n    Momentum for batch normalization, typically ranges from 0.01 to 0.4 (default=0.02)\n\n- `clip_value` : float (default None)\n\n    If a float is given this will clip the gradient at clip_value.\n    \n- `lambda_sparse` : float (default = 1e-3)\n\n    This is the extra sparsity loss coefficient as proposed in the original paper. The bigger this coefficient is, the sparser your model will be in terms of feature selection. Depending on the difficulty of your problem, reducing this value could help.\n\n- `optimizer_fn` : torch.optim (default=torch.optim.Adam)\n\n    Pytorch optimizer function\n\n- `optimizer_params`: dict (default=dict(lr=2e-2))\n\n    Parameters compatible with optimizer_fn used initialize the optimizer. Since we have Adam as our default optimizer, we use this to define the initial learning rate used for training. As mentionned in the original paper, a large initial learning of ```0.02 ```  with decay is a good option.\n\n- `scheduler_fn` : torch.optim.lr_scheduler (default=None)\n\n    Pytorch Scheduler to change learning rates during training.\n\n- `scheduler_params` : dict\n\n    Dictionnary of parameters to apply to the scheduler_fn. Ex : {"gamma": 0.95, "step_size": 10}\n\n- `model_name` : str (default = \'DreamQuarkTabNet\')\n\n    Name of the model used for saving in disk, you can customize this to easily retrieve and reuse your trained models.\n\n- `saving_path` : str (default = \'./\')\n\n    Path defining where to save models.\n\n- `verbose` : int (default=1)\n\n    Verbosity for notebooks plots, set to 1 to see every epoch, 0 to get None.\n\n- `device_name` : str (default=\'auto\')\n    \'cpu\' for cpu training, \'gpu\' for gpu training, \'auto\' to automatically detect gpu.\n\n- `mask_type: str` (default=\'sparsemax\')\n    Either "sparsemax" or "entmax" : this is the masking function to use for selecting features\n\n## Fit parameters\n\n- `X_train` : np.array\n\n    Training features\n\n- `y_train` : np.array\n\n    Training targets\n\n- `eval_set`: list of tuple  \n\n    List of eval tuple set (X, y).  \n    The last one is used for early stopping  \n\n- `eval_name`: list of str  \n              List of eval set names.  \n\n- `eval_metric` : list of str  \n              List of evaluation metrics.  \n              The last metric is used for early stopping.\n\n- `max_epochs` : int (default = 200)\n\n    Maximum number of epochs for trainng.\n    \n- `patience` : int (default = 15)\n\n    Number of consecutive epochs without improvement before performing early stopping.\n\n    If patience is set to 0 then no early stopping will be performed.\n\n    Note that if patience is enabled, best weights from best epoch will automatically be loaded at the end of `fit`.\n\n- `weights` : int or dict (default=0)\n\n    /!\\ Only for TabNetClassifier\n    Sampling parameter\n    0 : no sampling\n    1 : automated sampling with inverse class occurrences\n    dict : keys are classes, values are weights for each class\n\n- `loss_fn` : torch.loss or list of torch.loss\n\n    Loss function for training (default to mse for regression and cross entropy for classification)\n    When using TabNetMultiTaskClassifier you can set a list of same length as number of tasks,\n    each task will be assigned its own loss function\n\n- `batch_size` : int (default=1024)\n\n    Number of examples per batch, large batch sizes are recommended.\n\n- `virtual_batch_size` : int (default=128)\n\n    Size of the mini batches used for "Ghost Batch Normalization".\n    /!\\ `virtual_batch_size` should divide `batch_size`\n\n- `num_workers` : int (default=0)\n\n    Number or workers used in torch.utils.data.Dataloader\n\n- `drop_last` : bool (default=False)\n\n    Whether to drop last batch if not complete during training\n\n- `callbacks` : list of callback function  \n        List of custom callbacks\n\n- `pretraining_ratio` : float\n\n        /!\\ TabNetPretrainer Only : Percentage of input features to mask during pretraining.\n\n        Should be between 0 and 1. The bigger the harder the reconstruction task is.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dreamquark-ai/tabnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)