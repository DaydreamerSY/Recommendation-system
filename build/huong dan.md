1. Cài đặt các thư viện

    `pip install -r requirements.txt`

2. Import vô code

```
import joblib
import pandas as pd
from Recommender import Recommender
```

3. Load model scaler để chuẩn hóa dữ liệu

```
scaler = joblib.load("MinMaxScalerModel.gz")
```

4. Chuẩn bị file data đầu vào

data_1: 
- Type: dict (Dictionary) hoặc json
- thông tin đầu vào của user

data_2:
- Type: list
- toàn bộ database chứa [id, region, area, price, mat_tien, huong_nha, duong_vao, bedroom_number, toilet_number, phap_ly]

```
data_1 = {"region": "abc",
          "area": 260,
          "price": "1 triệu/m2",
          "mat_tien": 15,
          "huong_nha": "Nam",
          "duong_vao": 9,
          "bedroom_number": 0,
          "toilet_number": 0,
          "phap_ly": "Sổ đỏ/ Sổ hồng"}


data_2 = [...]
```

5. Gọi thư viện và lấy kết quả output

```
similor = Recommender(user_data=data_1, database=data_2, scaler=scaler)
similor.get_recommended()
-------------------------------------------------------------------------------
#Output: [similar_id_1, similar_id_2, similar_id_3, similar_id_4, similar_id_5]
```

6. Toàn bộ code ví dụ

```
import joblib
from Recommender import Recommender
scaler = joblib.load("MinMaxScalerModel.gz")

data_1 = {"region": "abc",
          "area": 260,
          "price": "1 triệu/m2",
          "mat_tien": 15,
          "huong_nha": "Nam",
          "duong_vao": 9,
          "bedroom_number": 0,
          "toilet_number": 0,
          "phap_ly": "Sổ đỏ/ Sổ hồng"}

data_temp = {"id": 1, "region": "abc", "area": 260, "price": "3 tỷ", "mat_tien": 15,
             "huong_nha": "Nam", "duong_vao": 9, "bedroom_number": 0, "toilet_number": 0, "phap_ly": "Sổ đỏ/ Sổ hồng"}

data_2 = [data_temp, data_temp, data_temp, data_temp]


similor = Recommender(user_data=data_1, database=data_2, scaler=scaler)
display(similor.user_last_visited)
display(similor.database)
similor.get_recommended()
```