#!/usr/bin/env python3

import sqlite3
import pandas as pd 
import matplotlib as plt
import seaborn as sns

def apps_over_time(conn):
    df = pd.read_sql_query("SELECT application_date, status FROM applications", conn)
    df['application_date'] = pd.to_datetime(df['application_date'])
    df['month'] = df['application_date'].dt.to_period('M')
    apps_per_month = df.groupby(['month', 'status']).size().unstack(fill_value=0)

    apps_per_month.plot(kind='area', stacked=True, figsize=(10,6))
    plt.title("Applications by Status Over Time")
    plt.xlabel("Month")
    plt.ylabel("Number of Applications")
    plt.show()

def main():
    conn = sqlite3.connect("applications.db")

    apps_over_time(conn)

if __name__=='__main__':
    main()
