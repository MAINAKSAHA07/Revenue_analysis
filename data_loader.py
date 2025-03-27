import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, db_params):
        """Initialize database connection parameters"""
        self.db_params = db_params
        self.engine = create_engine(
            f"postgresql://{db_params['user']}:{db_params['password']}@"
            f"{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        )

    def clean_data(self, df):
        """Clean the dataframe"""
        try:
            # Convert column names to lowercase and replace spaces with underscores
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Ensure required columns exist
            required_columns = ['predicted_demand', 'refund_amount', 'actual_revenue']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")

            # Convert numeric columns to float, replacing any non-numeric values with NaN
            numeric_columns = ['predicted_demand', 'refund_amount', 'actual_revenue']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Remove rows with NaN values in required columns
            df = df.dropna(subset=numeric_columns)

            # Add created_at column if it doesn't exist
            if 'created_at' not in df.columns:
                df['created_at'] = datetime.now()

            # Ensure all numeric values are non-negative
            for col in numeric_columns:
                df[col] = df[col].clip(lower=0)

            return df

        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise

    def load_data(self, file_path, file_type=None):
        """Load data from various file formats"""
        try:
            if file_type is None:
                file_type = file_path.split('.')[-1].lower()

            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            logger.info(f"Successfully loaded data from {file_path}")
            return df

        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def push_to_db(self, df, table_name='predictions'):
        """Push cleaned data to PostgreSQL database"""
        try:
            # Clean the data
            df_cleaned = self.clean_data(df)

            # Push to database
            df_cleaned.to_sql(
                table_name,
                self.engine,
                if_exists='append',
                index=False,
                method='multi'
            )

            logger.info(f"Successfully pushed {len(df_cleaned)} rows to {table_name}")
            return True

        except Exception as e:
            logger.error(f"Error pushing data to database: {str(e)}")
            raise

def main():
    # Database connection parameters
    db_params = {
        'dbname': 'revenue_analysis',
        'user': 'adminuser',
        'password': 'SecurePassword123!',
        'host': 'revenue-analysis-db.postgres.database.azure.com',
        'port': '5432'
    }

    # Initialize DataLoader
    loader = DataLoader(db_params)

    # Example usage
    try:
        # Load data from CSV
        df = loader.load_data('your_data.csv')
        
        # Push to database
        loader.push_to_db(df)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main() 