# -*- coding: utf-8 -*-
import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lấy dữ liệu từ biểu mẫu HTML
        car_brand = request.form['car-brand']
        car_model = request.form['car-model']
        car_origin = request.form['car-origin']
        mf_date = int(request.form['mf-date'])
        mileage = int(request.form['mileage'])
        car_seats = int(request.form['car-seats'])
        gearbox = request.form['gearbox']
        condition = request.form['condition']
        fuel = request.form['fuel']
        cartype = request.form['cartype']

        new_data = pd.DataFrame({
            'CarBrand': [car_brand],
            'CarModel': [car_model],
            'CarOrigin': [car_origin],
            'MfgDate': [mf_date],
            'Mileage': [mileage],
            'CarSeats': [car_seats],
            'GearBox': [gearbox],
            'Condition': [condition],
            'Fuel': [fuel],
            'CarType': [cartype]
        })

        # Lấy danh sách cột được mã hóa từ hàm columns_encoded()
        loaded_model = joblib.load('models/random_forest_model.pkl')
        encoded_columns = joblib.load('models/encoded_columns.pkl')

        # Sử dụng mô hình dự đoán để ước tính giá xe

        categorical_columns = ['CarBrand', 'CarModel', 'Condition', 'GearBox', 'Fuel', 'CarOrigin', 'CarType']
        new_data[categorical_columns] = new_data[categorical_columns].apply(lambda x: x.str.lower())
        new_data_encoded = pd.get_dummies(new_data, columns=categorical_columns)
        new_data_encoded = new_data_encoded.reindex(columns=encoded_columns, fill_value=0)

        estimated_price = loaded_model.predict(new_data_encoded)

        # Trả về kết quả ước tính cho trang web
        return render_template('index.html', pred=estimated_price)

    return render_template('index.html', pred=None)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        content = request.form.get('content')

        # Lưu dữ liệu vào tệp văn bản
        with open('contact_data.txt', 'a', encoding='utf-8') as file:
            file.write(f'First Name: {first_name}, Last Name: {last_name}, Email: {email}, Content: {content}\n')

        # Sau khi lưu dữ liệu, bạn có thể trả về một thông báo hoặc chuyển hướng người dùng đến trang khác
        return "Dữ liệu đã được ghi và xử lý thành công!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
