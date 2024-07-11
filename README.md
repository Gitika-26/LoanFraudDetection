# **Loan Fraud Detection with Neural Networks.**

The Loan Fraud Detection Model is designed to identify fraudulent loan applications using an Artificial Neural Network (ANN) implemented with TensorFlow 2.0 and Keras. The model analyzes various features of loan applications to predict the likelihood of fraud, helping financial institutions mitigate risks and prevent fraudulent activities.

## Table of Contents-
[Introduction](#intro)  <br>
[Dataset](#dataset) <br>
[Data Preprocessing](#datapreprocessing)  <br>
[Exploratory Data Analysis (EDA)](#EDA)  <br>
[Machine Learning Models](#MLModels)  <br>
[Model Evaluation](#ModelEvaluation)  <br>
[Results](#Results) <br>


<a name="intro"></a>
## Introduction
* Background <br>
Fraud in the loan industry poses a significant threat to financial institutions, leading to substantial financial losses and reputational damage. Traditional methods of detecting fraudulent activities often fall short in the face of increasingly sophisticated fraud tactics. To address these challenges, the Loan Fraud Detection Model leverages cutting-edge artificial intelligence techniques to provide a robust and reliable solution for identifying fraudulent loan applications.<br>

* Problem Statement<br>
Financial fraud, particularly loan fraud, involves deceiving lenders into approving loans under false pretenses. This can include identity theft, falsified income information, and other fraudulent activities. The complexity and volume of loan applications make it difficult for traditional rule-based systems to effectively detect and prevent fraud. There is a pressing need for an intelligent system capable of analyzing vast amounts of data and identifying patterns indicative of fraudulent behavior.<br>

* Solution Overview <br>
The Loan Fraud Detection Model employs an Artificial Neural Network (ANN) to detect fraudulent loan applications with high accuracy. By analyzing a variety of features from loan applications, the model can identify subtle patterns that may indicate fraudulent activity. The model is built using TensorFlow 2.0 and Keras, which provide powerful tools for developing, training, and deploying deep learning models.. <br>

<a name="dataset"></a>
## Dataset
The dataset used in this project includes information on telecom customers and their subscription details. The columns are:  <br>
* loan_amnt     <br>
* term          <br>
* int_rate          <br>
* installment                 <br>
* grade                       <br>
* sub_grade                   <br>
* emp_title               <br>
* emp_length              <br>
* home_ownership              <br>
* annual_inc                  <br>
* verification_status         <br>
* issue_d                     <br>
* loan_status                 <br>
* purpose                     <br>
* title                    <br>
* dti                         <br>
* earliest_cr_line            <br>
* open_acc                    <br>
* pub_rec                     <br>
* revol_bal                   <br>
* revol_util                <br>
* total_acc                   <br>
* initial_list_status         <br>
* application_type            <br>
* mort_acc                <br>
* pub_rec_bankruptcies      <br>
* address    <br>
The descriptions of the Columns can be found in the info csv file. <br>

<a name="datapreprocessing"></a>
## Data Preprocessing
To prepare the data for modeling, the following preprocessing steps were performed:  <br>
* Handling missing values  <br>
* Encoding categorical variables  <br>
* Normalizing numerical features <br>
* Filling in missing values using appropriate correlational columns data <br>

<a name="EDA"></a>
## Exploratory Data Analysis (EDA)
EDA was conducted to understand the distribution and relationships between variables. Python Data Visualisation Libraries * Seaborn *  &  * Matplotlib* were used. Key insights were visualized using various plots and graphs. the following are the plots used - <br>
* BarPlot <br>
* Countplot <br>
* Boxplot <br>
* Displot <br>
* Histplot <br>
* Scatterplot <br>

<a name="MLModels"></a>
## Our Deep Learning Model 
Tensorflow 2.0 with Keras API was used to deploy a feed forward Artificial Neural Network. The following parameters were adjusted accordingly for better accuracy  <br>
* No of Neurons  <br>
* No of epochs <br>
* Choosing Appropriate Activation function <br>
* Dropout   <br>
* Monitering losses & Val Losses  <br>

<a name="ModelEvaluation"></a>
## Model Evaluation
The models were evaluated using the following metrics:  <br>
* Precision  <br>
* Recall  <br>
* F1 Score  <br>
* Losses <br>
* Val_Losses <br>
* Graph of Losses and Val_Losses values during training


<a name="Results"></a>
## Results
The Gradient Boosting model provided the best performance with the following metrics:  <br>
* Precision: 90 %  <br>
* Recall: 89 %   <br>
* F1 Score: 87 %  <br>
