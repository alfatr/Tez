from flask import Blueprint, render_template, redirect, url_for, request

results_bp = Blueprint("results", __name__,
                       static_folder="static", template_folder="templates")


@results_bp.route("/results", methods=['GET', 'POST'])
def results():
    chosen_columns = request.args.getlist('chosen_columns')
    dataset = request.args.get('dataset')

    import pandas as pd
    import numpy as np
    import itertools
    import os
    from main import app
    import json

    graphs = pd.read_excel(os.path.join(
        app.root_path, 'static/datasets', "graphsv2.xlsx"))

    df = pd.DataFrame([])

    if dataset.endswith('.csv'):
        df = pd.read_csv(os.path.join(
            app.root_path, 'static/datasets', dataset))

    elif dataset.endswith('.xlsx'):
        df = pd.read_excel(os.path.join(
            app.root_path, 'static/datasets', dataset))

    df = df.loc[:, chosen_columns]

    def return_datatype(datatype) -> str:
        numeric_types = ['float64', 'int64']
        categorical_types = ['object']
        time_series_types = []

        if(str(datatype) in (numeric_types)):
            return 'Numeric'
        if(str(datatype) in (categorical_types)):
            return 'Categorical'
        if(str(datatype) in (time_series_types)):
            return 'Time Series'

    dt_df = pd.DataFrame(df.dtypes)

    numeric_columns = []
    categorical_columns = []
    time_series_columns = []

    def create_datatype_lists(dt_df: pd.DataFrame):
        numeric_types = ['float64', 'int64']
        categorical_types = ['object']
        time_series_types = []

        for i in range(dt_df.shape[0]):
            column_datatype = dt_df.iloc[i][0]
            column_name = dt_df.iloc[i].name

            if(column_datatype in (numeric_types)):
                numeric_columns.append(column_name)
            if(column_datatype in (categorical_types)):
                categorical_columns.append(column_name)
            if(column_datatype in (time_series_types)):
                time_series_columns.append(column_name)

    create_datatype_lists(dt_df)

    def dataframe_datatypes(df: pd.DataFrame) -> []:
        numeric = 0
        categorical = 0
        time_series = 0

        for d in df.dtypes:
            if(return_datatype(str(d)) == 'Numeric'):
                numeric = numeric + 1
            if(return_datatype(str(d)) == 'Categorical'):
                categorical = categorical + 1
            if(return_datatype(str(d)) == 'Time Series'):
                time_series = time_series + 1

        return [numeric, categorical, time_series]

    df_dtypes = dataframe_datatypes(df)

    def find_possible_graphs(df_dtypes: [], graphs: pd.DataFrame,) -> []:
        possible = []

        for g in graphs.values:
            g_dtypes = [int(g[2]), int(g[3]), int(g[4])]
            if(df_dtypes == g_dtypes):
                possible.append(g)

        possible = pd.DataFrame(possible)
        possible.columns = graphs.columns

        return possible

    possible_graphs = find_possible_graphs(df_dtypes, graphs)

    def ordering_of_df(df: pd.DataFrame) -> []:
        orderings = []

        for c in df.columns:
            if(return_datatype(str(df[c].dtype)) == 'Numeric'):
                values = df[c].values
                sorted_elements = [values[index] <= values[index+1]
                                   for index in range(len(values)-1)]
                orderings.append(all(sorted_elements))
            else:
                orderings.append(False)

        return orderings

    def single_obs_per_group(df=pd.DataFrame) -> []:
        groupings = []

        for c in df.columns:
            if(return_datatype(str(df[c].dtype)) == 'Categorical'):
                groupings.append(len(df.groupby(c).size()) == df.shape[0])
            else:
                groupings.append(False)

        return groupings

    def several_obs_per_group(df=pd.DataFrame) -> []:
        groupings = []

        for c in df.columns:
            if(return_datatype(str(df[c].dtype)) == 'Categorical'):
                groupings.append(not len(df.groupby(c).size()) == df.shape[0])
            else:
                groupings.append(False)

        return groupings

    def eliminate_further(df : pd.DataFrame, possible_graphs : pd.DataFrame):
        possible = []
        
        orderings = ordering_of_df(df)
        one_obs = single_obs_per_group(df)
        sev_obs = several_obs_per_group(df)
        
        print(orderings)

        # Elimination
        for g in range(possible_graphs.shape[0]):
            possible_flag = True
            
            if(possible_graphs.loc[g]['Order'] == 1.0):
                if(any(ordering_of_df(df))):
                    print(1)
                    possible_flag = True
                else:
                    possible_flag = False
                    print(2)
                    
            if(possible_graphs.loc[g]['One Obs'] == 1):
                if(any(one_obs) == 1):
                    print(3)
                    possible_flag = True
                else:
                    possible_flag = False
            
            if(possible_graphs.loc[g]['Several Obs'] == 1):
                if(any(sev_obs) == 1):
                    possible_flag = True
                    print(4)
                else:
                    possible_flag = False
                
            if(possible_flag):
                possible.append(possible_graphs.loc[g].values)
                
        
        possible_graphs = pd.DataFrame(possible)
        possible_graphs.columns = graphs.columns
        
        return possible_graphs

    possible_graphs = eliminate_further(df, possible_graphs)

    penalties = []

    for g in range(possible_graphs.shape[0]):
        penalties.append(0)

    def max_group_penalty(df: pd.DataFrame, graph: pd.DataFrame):
        penalty = 0
        # diff = len(df.groupby('variety').size()) - possible_graphs.loc[g]['Max Group']
        diff = 0

        for c in df.columns:
            if(return_datatype(str(df[c].dtype)) == 'Categorical'):
                diff = len(df.groupby(c).size()) - graph['Max Group']

        if (diff) < 0:
            penalty = ((diff**2)**.25)
        else:
            penalty = ((diff + 1)**4)

        return penalty

    max_group_penalty(df, possible_graphs.loc[0])

    def min_row_penalty(df: pd.DataFrame, graph: pd.DataFrame):

        rows = df.shape[0]
        diff = graph['Min Row'] - rows
        if (diff < 0):
            penalty = diff / (diff - graph['Min Row'])
            # Üstel artış
        else:
            penalty = diff / (diff - graph['Min Row'])
            # Logaritmik artış

        return penalty

    min_row_penalty(df, possible_graphs.loc[0])

    def calculate_scores(possible_graphs: pd.DataFrame) -> []:
        scores = []

        for g in range(possible_graphs.shape[0]):
            scores.append([possible_graphs.loc[g]['Name'], 0])

            # Scoring
            if(possible_graphs.loc[g]['Min Row'] > 0):
                scores[g][1] = + min_row_penalty(df, possible_graphs.loc[g])
            if(possible_graphs.loc[g]['Std'] > 0):
                print('  - Std calculation')
            if(possible_graphs.loc[g]['Max Group'] > 0):
                scores[g][1] = + max_group_penalty(df, possible_graphs.loc[g])

        return scores

    scores = calculate_scores(possible_graphs)

    return render_template('results.html',
                           title='Results Page',
                           dataset=dataset,
                           chosen_columns=chosen_columns,
                           scores=scores,
                           numeric_columns=numeric_columns,
                           categorical_columns=categorical_columns,
                           time_series_columns=time_series_columns)
