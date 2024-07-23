from flask import Flask, request, redirect, url_for
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def upload_file():
    return '''
    <html>
    <head>
        <style>
            body {
                background-color: #f0f8ff;
                font-family: 'Arial', sans-serif;
                color: #333;
                padding: 0;
                margin: 0;
            }
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #0056b3;
                padding: 10px 20px;
            }
            .navbar .logo {
                font-size: 1.5rem;
                color: #fff;
                font-weight: bold;
            }
            .navbar .nav-links {
                list-style: none;
                display: flex;
                gap: 1rem;
            }
            .navbar .nav-links li a {
                text-decoration: none;
                color: #fff;
                font-weight: bold;
            }
            .navbar .search-bar {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .navbar .search-bar input {
                padding: 5px;
                border-radius: 5px;
                border: none;
            }
            .navbar .search-bar button {
                padding: 5px 10px;
                background-color: #fff;
                color: #004080;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .slider {
                position: relative;
                width: 100%;
                height: 300px;
                overflow: hidden;
                background-color: #ddd;
            }
            .slides {
                display: flex;
                width: 300%;
                height: 100%;
                animation: slide 6s infinite;
            }
            .slides img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            @keyframes slide {
                0% { margin-left: 0; }
                20% { margin-left: 0; }
                25% { margin-left: -100%; }
                45% { margin-left: -100%; }
                50% { margin-left: -200%; }
                70% { margin-left: -200%; }
                75% { margin-left: 0; }
            }
            .container {
                display: flex;
                justify-content: space-around;
                padding: 20px;
            }
            .left, .right {
                width: 45%;
                padding: 20px;
                box-sizing: border-box;
            }
            .section {
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #0056b3;
                font-size: 36px;
                margin-bottom: 20px;
                font-weight: bold;
            }
            h2 {
                color: #003366;
                font-size: 24px;
                margin-bottom: 20px;
            }
            p {
                font-size: 18px;
                margin-bottom: 20px;
            }
            form {
                margin: 20px 0;
            }
            input[type="file"], select {
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #0056b3;
                border-radius: 5px;
                background-color: #fff;
                color: #333;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #0056b3;
                border: none;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
            }
            input[type="submit"]:hover {
                background-color: #003366;
            }
            .content {
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                display: inline-block;
                margin-top: 20px;
                text-align: left;
            }
            a {
                text-decoration: none;
                color: #0056b3;
                font-size: 18px;
            }
            a:hover {
                color: #003366;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="logo">InsightWave</div>
            <ul class="nav-links">
                <li><a href="http://127.0.0.1:5000/">Home</a></li>
                <li><a href="#">Features</a></li>
                <li><a href="https://www.linkedin.com/company/insightwave2024/?viewAsMember=true">Contact Us</a></li>
            </ul>
            <div class="search-bar">
                <input type="text" placeholder="Search...">
                <button type="submit">Go</button>
            </div>
        </nav>
        <div class="slider">
            <div class="slides">
                <img src="https://i.pinimg.com/736x/ba/89/a1/ba89a180ca3b4e77f0a66d527e577dfb.jpg" alt="Data Analytics Image 1">
                <img src="https://i.pinimg.com/564x/6b/3d/1e/6b3d1e2e6b36f3a4d0fffd7dfed23e13.jpg" alt="Slide 2">
                <img src="https://i.pinimg.com/564x/f5/30/5a/f5305ac5edded37e0cd3b751ad7ce89e.jpg" alt="Slide 3">
            </div>
        </div>
        <div class="container">
            <div class="left section">
                <h1>Data Analytics AI</h1>
                <h2>Upload Excel File for Analysis</h2>
                <form action="/analyze" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <select name="operation">
                        <option value="sum">Sum</option>
                        <option value="average">Average</option>
                        <option value="prediction">Prediction</option>
                    </select>
                    <input type="submit" value="Analyze">
                </form>
            </div>
            <div class="right section">
                <h1>About</h1>
                <p>Welcome to InsightWave, where the future of data meets the power of artificial intelligence. Our cutting-edge platform transforms raw data into actionable insights with unparalleled precision and ease. Whether you're a business aiming to optimize performance, a startup looking to forecast trends, or an analyst seeking deeper insights, we provide the tools to unlock the full potential of your data.</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files or 'operation' not in request.form:
        return redirect(url_for('upload_file'))

    file = request.files['file']
    operation = request.form['operation']

    if file.filename == '':
        return redirect(url_for('upload_file'))

    df = pd.read_excel(file)

    numeric_df = df[['coi_quantity', 'coi_unit_price', 'coi_price', 'coi_unit_original_price', 'coi_total_tax_percentage']]

    result_content = ""
    if operation == 'sum':
        result = numeric_df.sum().sum()
        result_label = "Total Sum"
        result_content = f"<p>{result_label}: {result}</p>"
    elif operation == 'average':
        result = round(numeric_df.stack().mean(), 2)
        result_label = "Average"
        result_content = f"<p>{result_label}: {result}</p>"
    elif operation == 'prediction':
        if 'coi_price' in df.columns:
            features = df[['coi_quantity', 'coi_unit_price', 'coi_unit_original_price', 'coi_total_tax_percentage']]

            scaler = StandardScaler()
            X = scaler.fit_transform(features)
            y = df['coi_price']

            model = LinearRegression().fit(X, y)

            future_features = np.array([[df['coi_quantity'].mean(), df['coi_unit_price'].mean(), df['coi_unit_original_price'].mean(), df['coi_total_tax_percentage'].mean()]] * 3)
            future_X = scaler.transform(future_features)
            future_sales = model.predict(future_X)
            future_sales = [round(sale, 2) for sale in future_sales]

            plt.figure(figsize=(10, 5))
            plt.plot(range(len(df)), y, label='Actual Sales')
            plt.plot(range(len(df), len(df) + 3), future_sales, label='Predicted Sales', linestyle='--', marker='o')
            plt.xlabel('Month')
            plt.ylabel('Sales')
            plt.legend()
            plt.title('Sales Prediction')
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            img_b64 = base64.b64encode(img.getvalue()).decode()
            img_html = f'<img src="data:image/png;base64,{img_b64}" alt="Sales Prediction">'
            result_content = img_html
        else:
            result_content = "<p>Not enough data for prediction</p>"

    summary_stats = numeric_df.describe().to_html()

    return f'''
    <html>
    <head>
        <style>
            body {{
                background-color: #f0f8ff;
                font-family: 'Arial', sans-serif;
                color: #333;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                color: #0056b3;
                font-size: 36px;
                margin-bottom: 20px;
                font-weight: bold;
            }}
            p {{
                font-size: 18px;
                margin-bottom: 20px;
            }}
            .content {{
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                display: inline-block;
                margin-top: 20px;
                text-align: left;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Analysis Results</h1>
        <div class="content">
            {result_content}
            <h2>Summary Statistics</h2>
            {summary_stats}
        </div>
        <a href="/">Go back</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
