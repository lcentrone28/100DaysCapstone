from data_prep.process_data import process_data
import subprocess

def main():
    # process_data()
    # ^ uncomment if data is missing

    subprocess.run(["streamlit", "run", "dashboard.py"], check=True)

if __name__ == "__main__":
    main()