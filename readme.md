# House price Prediction Using Machine Learning
#### Video Demo:  <URL HERE>
#### Description: 
1. Its a machine learning model based on LGBM Quantile Regression Model. It uses a listing of previous prices and trains itself on various listing provided by a CSV file.

2. It Gives a predicted price by comparing various factors.
   a) Bedrooms and Bathrooms
   b) House and Acre Size
   c) Prices of houses with same factors
   d) Comparing prices of houses with same factors in same locality
3. The Website is based on flask, it uses a login system to simplify access to many users at once.
4. Users can upload a CSV file in the required format to recieve predictions.
5. SQlite3 is used to manage the record of predictions and user accounts.
6. Users can view the predicted output in the website itself and can also download the csv file.
7. Users can also manage their predictions(Deletion) within the website itself with the help of SQlite3 Integration.
8. Javascript is used for rendering the predicted output CSV in a table format and implementing Pagination, Searching and Sorting.
9. All the Languages used in this project are : Python, Flask, Jinja, HTML, CSS, Bootstrap, JavaScript, SQlite3, Jupyter Notebook(for Machine learning)

## How to use : 
1) Run machine.ipynb To train the Machine learning model on a full set of houses.
    a)It generates Ordinal_encoder.pkl, realtor_mean_model.pkl, realtor_quantile_model.pkl, trained_columns.pkl, For clean.py to use when Predicting.
2) Clean.ipynb is used when the website is running and it makes a prediction.
3) The training and predicting have been separated to prevent retraining repeatedly and reduce time.
4) Users can upload a CSV file(in the required format) in the Upload CSV section to create predictions and can view the predictions in the website itself or download it.
TODO
