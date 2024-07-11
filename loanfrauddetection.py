# -*- coding: utf-8 -*-
"""LoanFraudDetection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YKWdbf_o_bSgw0TX2w-1z8otzGcznBN4

# **LOAN FRAUD DETECTION MODEL WITH TENSORFLOW & KERAS**

# Importing Data through Google Drive & also importing necessary Libraries & Modules
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
file_path = '/content/drive/MyDrive/lending_club_info.csv'
df_info = pd.read_csv(file_path,index_col='LoanStatNew')
file_path1 = '/content/drive/MyDrive/lending_club_loan_two.csv'
df = pd.read_csv(file_path1)
df_copy =  pd.read_csv(file_path1)

"""# **Note - We have four main dataframes in this project -**
## df_info = has description and functionalities of each column of df.
## df - main dataframe with data we preprocess and train on.
## df_copy - original dataframe to keep for original string values.
## df_new= columns of df with just numerical attributes.

# Defining a function to get Descriptions through column name
"""

print(df_info.loc['revol_util']['Description'])
def feat_info(col_name):
    print(df_info.loc[col_name]['Description'])
feat_info('earliest_cr_line')

df_info

"""## Taking a look at our Data"""

df

"""# Data Preprocessing
## **Part - I  Finding missing values in the DataFrame**

"""

df.isnull().sum()

"""### Fraction of missing values"""

100* df.isnull().sum()/len(df)

"""## **Part II - Dealing with Missing Values**

### Lets Check what are the relevant columns to keep and what columns to drop from the ones which have null values
#### Lets check the total unique values of the emp_title and emp_length column to decide whether to drop null values or impute them.
"""

print(df['emp_title'].nunique())
print(df['emp_length'].nunique())
print(df['emp_title'].value_counts())
print(df['emp_length'].value_counts())

"""#### Observations- Realistically there are too many unique job titles to try to convert this to a dummy variable feature. Let's remove that emp_title column

#### Next Trying to find any significance of emp_length column. To decide whether to drop it or not
"""

df=df.drop('emp_title',axis=1)

sorted(df['emp_length'].dropna().unique())
emp_length_order=['1 year',
 '10+ years',
 '2 years',
 '3 years',
 '4 years',
 '5 years',
 '6 years',
 '7 years',
 '8 years',
 '9 years',
 '< 1 year']

plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order=emp_length_order)

plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order=emp_length_order,hue='loan_status')

"""#### Converting emp_years to int datatype"""

emp_co = df[df['loan_status']=="Charged Off"].groupby("emp_length").count()['loan_status']
emp_fp = df[df['loan_status']=="Fully Paid"].groupby("emp_length").count()['loan_status']
emp_len = emp_co/emp_fp
emp_len
df['emp_length']=df['emp_length'].str.split('+').str[0]
df['emp_length']=df['emp_length'].str.split(' ').str[0]
df['emp_length']=df['emp_length'].str.replace('<','0.7')
df['emp_length']=df['emp_length'].astype(float)
df

"""### Charge off rates are extremely similar across all employment lengths. Go ahead and drop the emp_length column"""

df=df.drop('emp_length',axis=1)
df['term']=df['term'].str.split('m').str[0]

df['term']=df['term'].astype(int)

"""## **Review the title column vs the purpose column. Is this repeated information?**"""

print(df['purpose'].head(10))
df['title'].head(10)

"""#### The title column is simply a string subcategory/description of the purpose column. Go ahead and drop the title column."""

df=df.drop('title',axis=1)

"""### Taking a look at morrt_acc column"""

print(feat_info('mort_acc'))
df['mort_acc'].value_counts()

"""### There are many ways we could deal with this missing data. We could attempt to build a simple model to fill it in, such as a linear model, we could just fill it in based on the mean of the other columns, or you could even bin the columns into categories and then set NaN as its own category. There is no 100% correct approach! Let's review the other columsn to see which most highly correlates to mort_acc"""

grouped = df.columns.to_series().groupby(df.dtypes)

# Print columns grouped by data type
for dtype, columns in grouped:
    print(f'Data Type: {dtype}')
    print(f'Columns: {list(columns)}')
    print()

print("Correlation with the mort_acc column")
df[['loan_amnt', 'int_rate', 'installment', 'annual_inc', 'dti', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'mort_acc', 'pub_rec_bankruptcies']].corr()['mort_acc'].sort_values()

df_new=df[['loan_amnt', 'int_rate', 'installment', 'annual_inc', 'dti', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'mort_acc', 'pub_rec_bankruptcies']]
df_new

"""###  Looks like the total_acc feature correlates with the mort_acc , this makes sense! Let's try this fillna() approach. We will group the dataframe by the total_acc and calculate the mean value for the mort_acc per total_acc entry. To get the result below:"""

print("Mean of mort_acc column per total_acc")
df_new.groupby('total_acc').mean()['mort_acc']

"""### Let's fill in the missing mort_acc values based on their total_acc value. If the mort_acc is missing, then we will fill in that missing value with the mean value corresponding to its total_acc value from the Series we created above. This involves using an .apply() method with two columns"""

total_acc_avg = df_new.groupby('total_acc').mean()['mort_acc']

def fill_mort_acc(total_acc,mort_acc):
  if np.isnan(mort_acc):
    return total_acc_avg[total_acc]
  else:
    return mort_acc
df['mort_acc'] = df_new.apply(lambda x: fill_mort_acc(x['total_acc'], x['mort_acc']), axis=1)

df.isnull().sum()

"""###  revol_util and the pub_rec_bankruptcies have missing data points, but they account for less than 0.5% of the total data. Go ahead and remove the rows that are missing those values in those columns with dropna()"""

df = df.dropna()
df.isnull().sum()

"""# **Categorial Variables to Numerical Values**"""

grouped = df.columns.to_series().groupby(df.dtypes)

# Print columns grouped by data type
for dtype, columns in grouped:
    print(f'Data Type: {dtype}')
    print(f'Columns: {list(columns)}')
    print()

"""## Lets see what to do with each of the feature
## **grade feature**

###  We already know grade is part of sub_grade, so just drop the grade feature.
"""

df=df.drop('grade',axis=1)

"""### Convert the subgrade into dummy variables. Then concatenate these new columns to the original dataframe. Remember to drop the original subgrade column and to add drop_first=True to your get_dummies call."""

subgrade_dummies = pd.get_dummies(df['sub_grade'],drop_first=True)
df = pd.concat([df.drop('sub_grade',axis=1),subgrade_dummies],axis=1)

"""## **verification_status, application_type,initial_list_status,purpose**

### TASK: Convert these columns: ['verification_status', 'application_type','initial_list_status','purpose'] into dummy variables and concatenate them with the original dataframe. Remember to set drop_first=True and to drop the original columns.
"""

dummies = pd.get_dummies(df[['verification_status', 'application_type','initial_list_status','purpose' ]],drop_first=True)
df = df.drop(['verification_status', 'application_type','initial_list_status','purpose'],axis=1)
df = pd.concat([df,dummies],axis=1)

"""## **home_ownership**
### Review the value_counts for the home_ownership column

### Convert these to dummy variables, but [replace] NONE and ANY with OTHER, so that we end up with just 4 categories, MORTGAGE, RENT, OWN, OTHER. Then concatenate them with the original dataframe. Remember to set drop_first=True and to drop the original columns.
"""

df['home_ownership']=df['home_ownership'].replace(['NONE', 'ANY'], 'OTHER')

dummies = pd.get_dummies(df['home_ownership'],drop_first=True)
df = df.drop('home_ownership',axis=1)
df = pd.concat([df,dummies],axis=1)

"""### Next the left other three -
### 1) **address** = Let's feature engineer a zip code column from the address in the data set. Create a column called 'zip_code' that extracts the zip code from the address column.

### 2) **issue_d**  - This would be data leakage, we wouldn't know beforehand whether or not a loan would be issued when using our model, so in theory we wouldn't have an issue_date, drop this feature.

### 3) **earliest_cr_line** - This appears to be a historical time stamp feature. Extract the year from this feature using a .apply function, then convert it to a numeric feature. Set this new data to a feature column called 'earliest_cr_year'.Then drop the earliest_cr_line feature.
"""

df['zip_code'] = df['address'].apply(lambda address:address[-5:])
dummies = pd.get_dummies(df['zip_code'],drop_first=True)
df = df.drop(['zip_code','address'],axis=1)
df = pd.concat([df,dummies],axis=1)

df = df.drop('issue_d',axis=1)

df['earliest_cr_year'] = df['earliest_cr_line'].apply(lambda date:int(date[-4:]))
df = df.drop('earliest_cr_line',axis=1)

df.select_dtypes(['object']).columns

"""# Exploratory Data Analysis (EDA)

### Distribution of Loan Paid vs charged off
"""

sns.countplot(x='loan_status',data=df,color='blue')

"""### Distribution of Loan Amounts"""

plt.figure(figsize=(12,4))
sns.displot(df['loan_amnt'],kde=False,bins=40)
plt.xlim(0,45000)

"""### Finding Correlations between variables of Dataframe"""

df_new.corr()

plt.figure(figsize=(12,7))
sns.heatmap(df_new.corr(),annot=True,cmap='viridis')
plt.ylim(10, 0)

feat_info('installment')

feat_info('loan_amnt')

"""### Scatter Plot of Loan Status with Hue"""

sns.scatterplot(x='installment',y='loan_amnt',data=df,hue='loan_status')

"""### Box Plot of Loan Status vs Loan amt"""

sns.boxplot(x='loan_status',y='loan_amnt',data=df)

df.groupby('loan_status')['loan_amnt'].describe()

"""### Count Plots of Grades & Subgrades"""

sns.countplot(x='grade',data=df_copy,hue='loan_status')

plt.figure(figsize=(12,4))
subgrade_order = sorted(df_copy['sub_grade'].unique())
sns.countplot(x='sub_grade',data=df_copy,order = subgrade_order,palette='coolwarm' )

plt.figure(figsize=(12,4))
subgrade_order = sorted(df_copy['sub_grade'].unique())
sns.countplot(x='sub_grade',data=df_copy,order = subgrade_order,palette='coolwarm' ,hue='loan_status')

"""### **Observation -It looks like F and G subgrades don't get paid back that often. Isloate those and recreate the countplot just for those subgrades.**"""

f_and_g = df_copy[(df_copy['grade']=='G') | (df_copy['grade']=='F')]

plt.figure(figsize=(12,4))
subgrade_order = sorted(f_and_g['sub_grade'].unique())
sns.countplot(x='sub_grade',data=f_and_g,order = subgrade_order,hue='loan_status')

"""### Create a new column called 'load_repaid' which will contain a 1 if the loan status was "Fully Paid" and a 0 if it was "Charged Off"
"""

df['loan_repaid'] = df['loan_status'].map({'Fully Paid':1,'Charged Off':0})
df[['loan_repaid','loan_status']]
df=df.drop( 'loan_status',axis=1)
df_new['loan_repaid'] = df['loan_repaid']
df_new

df_new.corr()['loan_repaid'].sort_values().plot(kind='bar')

"""# **Model Training**
## **Splitting Datasets into Training and Testing Data**

"""

from sklearn.model_selection import train_test_split
X = df.drop('loan_repaid',axis=1).values
y = df['loan_repaid'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)

"""### Normalising the Data

"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""## **Creating & Training our Model**"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm

model = Sequential()
model.add(Dense(78,  activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(39, activation='relu'))
model.add(Dropout(0.2))

# hidden layer
model.add(Dense(19, activation='relu'))
model.add(Dropout(0.2))

# output layer
model.add(Dense(units=1,activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam')

"""### Fitting our Data"""

model.fit(x=X_train,
          y=y_train,
          epochs=25,
          batch_size=256,
          validation_data=(X_test, y_test),
          )

"""## **Evaluating the Model Perfomance**"""

losses = pd.DataFrame(model.history.history)
losses[['loss','val_loss']].plot()

from sklearn.metrics import classification_report,confusion_matrix
predictions = model.predict(X_test)
# Convert predicted probabilities to binary predictions (0 or 1)
predictions_binary = (predictions > 0.5).astype(int)  # Adjust the threshold (0.5) as needed
print(classification_report(y_test,predictions_binary))

cm = confusion_matrix(y_test, predictions_binary)
plt.figure(figsize=(6,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='viridis', xticklabels=['Charged off', 'Fully Paid'], yticklabels=['Charged off ', 'Fully Paid'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""## **Making Predictions for a customer**

"""

import random
random.seed(101)
random_ind = random.randint(0,len(df))

new_customer = df.drop('loan_repaid',axis=1).iloc[random_ind]
new_customer

"""#### Predicted by our Model"""

import tensorflow as tf # Import TensorFlow

model.predict(tf.convert_to_tensor(new_customer.values.reshape(1,78), dtype=tf.float32)) # Convert NumPy array to Tensor of type float32

"""#### Actual Via the Data Given"""

df.iloc[random_ind]['loan_repaid']

"""# **GREAT. OUR MODEL IS A SUCCESS**"""