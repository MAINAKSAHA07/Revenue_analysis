# Revenue Analysis Project

This project analyzes revenue data using machine learning techniques to predict and analyze revenue patterns.

## Project Structure

```
revenue_analysis/
├── data_loader.py      # Data loading and preprocessing
├── ml_model.py         # Machine learning model implementation
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

The project uses PostgreSQL as the database. Before running the application, ensure you have:

1. A PostgreSQL database instance running
2. The following database parameters configured:
   - Database name: revenue_analysis
   - Username: adminuser
   - Password: #
   - Host: revenue-analysis-db.postgres.database.azure.com
   - Port: 5432

3. Run the database setup script:
```bash
psql -h revenue-analysis-db.postgres.database.azure.com -U adminuser -d revenue_analysis -f database_setup.sql
```

## Data Loading

The project supports loading data from various file formats:

### Supported File Formats
- CSV (.csv)
- Excel (.xlsx, .xls)

### Required Data Format
Your input data should contain the following columns:
- `predicted_demand`: Expected demand value
- `refund_amount`: Amount of refunds
- `actual_revenue`: Actual revenue received

### Using the Data Loader

```python
from data_loader import DataLoader

# Initialize the loader
loader = DataLoader({
    'dbname': 'revenue_analysis',
    'user': '#',
    'password': '#',
    'host': '#',
    'port': '5432'
})

# Load and push data
df = loader.load_data('your_data.csv')  # or 'your_data.xlsx'
loader.push_to_db(df)
```

The data loader will:
- Clean and validate the data
- Handle missing values
- Convert data types
- Add timestamps
- Push the data to PostgreSQL

## Machine Learning Model

The project includes a machine learning model that:
- Predicts revenue based on historical data
- Evaluates model performance using RMSE and R² metrics
- Visualizes actual vs predicted values

To run the model:
```bash
python ml_model.py
```

## Dependencies

Key dependencies include:
- pandas >= 1.5.0
- scikit-learn >= 1.0.2
- psycopg2 >= 2.9.5
- sqlalchemy >= 1.4.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0

For a complete list of dependencies, see `requirements.txt`.

## Error Handling

The project includes comprehensive error handling and logging:
- Data validation errors
- Database connection issues
- File format compatibility
- Missing required columns
- Data type conversion errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### 📊 **Revenue and Demand Analysis using ML**  

This project builds a machine learning model to analyze predicted and actual revenue and demand data stored in a PostgreSQL database hosted on Azure. It also performs refund corrections and updates the database with more accurate values.

---

## 🚀 **Features**  
✅ Connects to a PostgreSQL database on Azure  
✅ Loads data into a **Pandas DataFrame**  
✅ Trains a **Linear Regression** model to predict revenue  
✅ Evaluates performance using **RMSE** and **R²**  
✅ Visualizes actual vs predicted revenue using **Seaborn**  
✅ Automatically corrects revenue values in the database if deviation exceeds **5%**  

---

## 🏗️ **Setup Instructions**  

### 1. **Clone the Repository**  
```bash
git clone https://github.com/your-username/revenue-analysis.git
cd revenue-analysis
```

---

### 2. **Create Virtual Environment**  
```bash
python3 -m venv venv
source venv/bin/activate   # For macOS/Linux
.\venv\Scripts\activate    # For Windows
```

---

### 3. **Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

### 4. **Set Up PostgreSQL on Azure**  
- Create a PostgreSQL server on Azure.  
- Create a database named `revenue_analysis`.  
- Create a table using the following schema:  

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    product_id INT,
    predicted_revenue FLOAT,
    predicted_demand INT,
    actual_revenue FLOAT,
    actual_demand INT,
    refund_amount FLOAT
);
```

---

### 5. **Add Sample Data**  
Use the `INSERT INTO` statement provided in the `ml_model.py` script to load sample data.  

---

### 6. **Run the Model**  
```bash
python3 ml_model.py
```

---

### 7. **Results**  
- Model performance (RMSE and R²) will be displayed in the terminal.  
- A plot showing actual vs predicted revenue will be generated.  
- The corrected values will be updated directly in the database.  
- Results will be saved to `results.csv`.  

---

## 🧠 **Technologies Used**  
- Python  
- PostgreSQL (Azure)  
- Scikit-learn  
- Pandas  
- Seaborn  
- Matplotlib  

---

## 🛠️ **To-Do**  
- [ ] Improve model accuracy using more complex models  
- [ ] Add more features (e.g., seasonality, product category)  
- [ ] Deploy as a REST API  

---

## 👨‍💻 **Author**  
**Mainak Saha**  
💼 Data Engineer in Training | Machine Learning Enthusiast  

---

### ✅ **Create the File**  
Create the file and add it to Git:  
```bash
touch README.md
```

Add content to the file:
```bash
nano README.md
```

Save and commit:
```bash
git add README.md
git commit -m "Added README.md"
git push
```

