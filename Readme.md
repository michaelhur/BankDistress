# Bank Distress in the News

The "Bank Distress in the News" project aims to identify the context in which the financial instutitions are being mentioned in news articles and build the predictive model to understand and detect past, ongoing or mounting bank distress events.

The app is built to show the distress signal of 87 European financial institutions who either have failed during 2008 Financial crisis and the relevant news articles, of course written at the time, mentioning the failed bank.

## Motivation

It is motivated by the [paper](https://arxiv.org/abs/1603.05670) presented by R&ouml;nnqvist and Sarlin[2]. The original paper proposes the method, including, but not limited to, heuristically labelling text according to time window, unsupervised semantic modelling, and predictive modelling. The paper demonstrates the applicability of such a predictive model to the study of the Financial Crisis in the late 2000's. 

#### Difference

This project differs from the original paper in a way that while the original paper searched and extracted the sentences that contain the name of the bank, this project uses Thomson Reuters' [Open PermID API](https://permid.org/) to extract all possible variation of mentionings of the banks.

## Data

Both the project and [the original paper](https://arxiv.org/abs/1603.05670) use the news articles obtained from Thomson Reuters.

In order to cope with Thomson Reuters' data policy, I have modified the publicly available Reuters-21578 dataset and reran the entire project. Hence, the news articles and distress signals shown in the application may sound irrelevant and outdated. The list of financial institutes is not affected.


## Get Started

The easiest way to get started is to clone this repository
```
git clone https://github.com/michaelhur/BankDistress.git
```

### Building Distress Model

'notebook' folder contains the jupyter notebooks with the step-by-step guide from 'entity tagging' to building a neural network model. <!--[Wiki Page](https://github.com/michaelhur/BankDistress/wiki) also contains this guide.--> In order to run this part of the project, you need to run following lines:

1. Change directory to notebook folder
```
cd ./notebook
```
2. Install required packages
```
pip install -r requirements.txt
```

### App

A proof-of-concept dash application is built to show how one can use such information. In order to run the app, run the following lines of bashes:

1. Change directory to 
```
cd ./app
```
2. Install required packages
```
pip install -r requirements.txt
```
3. Run the app
```
python app.py
```

## License

The project comprises of the part that must comply to the following license:
```
Calais PermID is licensed under the Creative Commons with Attribution license, version 4.0 (CC-BY)
```

## Reference

[1] Q. Le and T. Mikolov. Distributed representations of sentences and documents. In Proceedings of the 31st International Conference on Machine Learning (ICML-14), pages 11881196, 2014

[2] S. R&ouml;nnqvist and P. Sarlin. Bank Distress in the News: Describing Events through Deep Learning. arXiv preprint arXiv:1603.05670, 2016.
