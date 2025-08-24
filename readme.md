# House price Prediction Using Machine Learning
#### Video Demo:  https://youtu.be/5tsoOdrBf9M
## Description: 
1. Its a machine learning model based on LightGBM Quantile Regression Model. It uses a listing of previous prices and trains itself on various listing provided by a CSV file.
2. It Gives a predicted price by comparing various factors.
   - **Bedrooms and Bathrooms**  
   - **House and Acre Size**  
   - **Prices of houses with same factors**  
   - **Comparing prices of houses with same factors in same locality**
3. The Website is based on flask, it uses a login system to simplify access to many users at once.
4. I have used the existing files from CS50 provided in the PSET #9 Finance : cs50(module), apology.py, helpers.py
5. Users can upload a CSV file in the required format to recieve predictions.
6. SQlite3 is used to manage the record of predictions and user accounts.
7. Users can view the predicted output in the website itself and can also download the csv file.
8. Users can also manage their predictions(Deletion) within the website itself with the help of SQlite3 Integration.
9. Javascript is used for rendering the predicted output CSV in a table format and implementing Pagination, Searching and Sorting.
10. All the Languages used in this project are : Python, Flask, Jinja, HTML, CSS, Bootstrap, JavaScript, SQlite3, Jupyter Notebook(for Machine learning)

## How to use : 
1) Run machine.ipynb To train the Machine learning model on a full set of houses.
    a)It generates Ordinal_encoder.pkl, realtor_mean_model.pkl, realtor_quantile_model.pkl, trained_columns.pkl, For clean.py to use when Predicting.
2) Clean.ipynb is used when the website is running and it makes a prediction.
3) The training and predicting have been separated to prevent retraining repeatedly and reduce time.
4) Users can upload a CSV file(in the required format) in the Upload CSV section to create predictions and can view the predictions in the website itself or download it.

## Connect with me
Linkedin : https://www.linkedin.com/in/mudit-dua-2a30a1223/

Email : muditdua2007@gmail.com

Edx Username : Mudit_dua

Github Username : mudit-dua


