#!/usr/bin/env python3

import sys
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from enum import Enum

class Vis(Enum):
    apps_over_time = 1
    apps_by_industry_and_status = 2
    app_outcomes = 3
    response_times = 4
    contacts_per_company = 5
    event_participation = 6
    network = 7
    industry_salaries = 8
    activity_heatmap = 9

def apps_over_time(conn):
    df = pd.read_sql_query("SELECT application_date, status FROM applications", conn)
    df['application_date'] = pd.to_datetime(df['application_date'])
    df['day'] = df['application_date'].dt.to_period('D')
    apps_per_month = df.groupby(['day', 'status']).size().unstack(fill_value=0)

    apps_per_month.plot(kind='area', stacked=True, figsize=(10,6))
    plt.title("Applications by Status Over Time")
    plt.xlabel("Month")
    plt.ylabel("Number of Applications")
    plt.show()

def apps_by_industry_and_status(conn):
    df = pd.read_sql_query("""
        SELECT c.industry, a.status, COUNT(*) as num_apps
        FROM applications a 
        JOIN companies c 
            ON a.company_name = c.company_name 
        GROUP BY c.industry, a.status;
        """, conn)

    p = df.pivot(index="industry", columns="status", values="num_apps")
    sns.heatmap(p, annot=True)
    plt.title("Applications by Industry and Status")
    plt.show()

def app_outcomes(conn):
    df = pd.read_sql_query("""
        SELECT status
        FROM applications 
        """, conn)
    sns.countplot(x='status', data=df, order=df['status'].value_counts().index)
    plt.title("Application Outcomes")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.show()

def response_times(conn):
    df = pd.read_sql_query("""
        SELECT a.application_date, a.response_date, c.industry 
        FROM applications a, companies c 
        WHERE a.company_name = c.company_name;
        """, conn)
    df['application_date'] = pd.to_datetime(df['application_date'])
    df['response_date'] = pd.to_datetime(df['response_date'])
    df['response_time'] = (df['response_date'] - df['application_date']).dt.days

    sns.boxplot(x='industry', y='response_time', data=df)
    plt.title("Response Time by Industry")
    plt.ylabel("Days from Application to Rejection")
    plt.xticks(rotation=45)
    plt.show()

def contacts_per_company(conn):
    df = pd.read_sql_query("""
        SELECT company_name, COUNT(*) AS contact_count
        FROM contacts 
        GROUP BY company_name;
        """, conn)

    sns.barplot(x='contact_count', y='company_name', data=df.sort_values('contact_count', ascending=False))
    plt.title("Number of Contacts per Company")
    plt.xlabel("Number of Contacts")
    plt.ylabel("Company")
    plt.show()

def network(conn):
    df = pd.read_sql_query("""
        SELECT c.company_name, n.contact_name
        FROM companies c, contacts n 
        WHERE c.company_name = n.company_name;
        """, conn)

    G = nx.from_pandas_edgelist(df, 'contact_name', 'company_name')
    nx.draw(G, with_labels=True, node_color='lightblue')
    plt.title("Network")
    plt.show()

def event_participation(conn):
    df = pd.read_sql_query("""
        SELECT c.company_name, e.event_name
        FROM companies c, events e, event_companies ec 
        WHERE e.event_id = ec.event_id 
        AND c.company_name = ec.company_name;
        """, conn)

    G = nx.from_pandas_edgelist(df, 'Event_name', 'company_name')
    nx.draw(G, with_labels=True, node_color='lightblue')
    plt.title("Event–Company Connections")
    plt.show()

def industry_salaries(conn):
    df = pd.read_sql_query("""
        SELECT c.industry, a.salary 
        FROM companies c, applications a 
        WHERE c.company_name = a.company_name;
        """, conn)

    sns.boxplot(x='industry', y='salary', data=df)
    plt.title("Salary Distribution by Industry")
    plt.xticks(rotation=45)
    plt.show()

def activity_heatmap(conn):
    df = pd.read_sql_query("""
        SELECT application_date 
        FROM applications;
        """, conn)

    df['application_date'] = pd.to_datetime(df['application_date'])
    df['weekday'] = df['application_date'].dt.day_name()
    df['week'] = df['application_date'].dt.isocalendar().week
    heat = df.groupby(['week', 'weekday']).size().unstack(fill_value=0)
    sns.heatmap(heat, cmap="Blues")
    plt.title("Applications by Week and Weekday")
    plt.show()


def main():
    conn = sqlite3.connect("applications.db")


    print("1: Applications Over Time")
    print("2: Applications by Industry and Status Heat Map")
    print("3: Application Outcomes")
    print("4: Response Times")
    print("5: Contacts per Company")
    print("6: Event Participation")
    print("7: Network")
    print("8: Industry Salaries")
    print("9: Activity Heatmap")
    vis = input("Which visualization to view? Enter: ")
    try:
        vis = int(vis)
    except:
        print("Invalid input (must be integer)")
        sys.exit(1)

    match vis:
        case Vis.apps_over_time.value:
            apps_over_time(conn)
        case Vis.apps_by_industry_and_status.value:
            apps_by_industry_and_status(conn)
        case Vis.app_outcomes.value:
            app_outcomes(conn)
        case Vis.response_times.value:
            response_times(conn)
        case Vis.contacts_per_company.value:
            contacts_per_company(conn)
        case Vis.event_participation.value:
            event_participation(conn)
        case Vis.network.value:
            network(conn)
        case Vis.industry_salaries.value:
            industry_salaries(conn)
        case Vis.activity_heatmap.value:
            activity_heatmap(conn)
        case _:
            print("Invalid input (must be 1-4)")
            sys.exit(2)


if __name__=='__main__':
    main()
