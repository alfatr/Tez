
from flask import Blueprint, render_template, redirect, url_for, request

results_bp = Blueprint("results", __name__, static_folder="static", template_folder="templates")

@results_bp.route("/results", methods=['GET', 'POST'])
def results():
        import pandas as pd
        import numpy as np
        import itertools
        import os
        from main import app

        ## Bu sayfa şuan statik durumunda
        ## Değerleri kod içinden değiştirmek gerekiyor.
        
        graphs = pd.read_excel(os.path.join(app.root_path, 'static/datasets', "graphs.xlsx"))
        df = pd.read_csv(os.path.join(app.root_path, 'static/datasets', "iris.csv"))
        chosen_columns = ['sepal.length', 'sepal.width', 'variety']


        # df = pd.read_csv('datasets/3_TwoNumOrdered.csv')
        # chosen_columns = ['date', 'value']

        df = df.loc[:,chosen_columns]
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


        def return_datatypes(df : pd.DataFrame) -> []:
                numeric = 0
                categorical = 0
                time_series = 0
                several_num = 0
                several_cat = 0

                for t in df.dtypes:
                        if(return_datatype(t) == 'Numeric'):
                                numeric = numeric + 1
                        if(return_datatype(t) == 'Categorical'):
                                categorical = categorical + 1
                        if(return_datatype(t) == 'Time Series'):
                                time_series = time_series + 1
                
                ##Num&Cat
                if(numeric > 0 and categorical > 0):
                        if(categorical > 1):
                                categorical = 0
                                several_cat = 1
                        if(numeric > 1):
                                numeric = 0
                                several_num = 1
                
                ##Num
                if(categorical == 0 and numeric > 0):
                        if(numeric > 3):
                                numeric = 0
                                several_num = 1
                ##Cat
                if(numeric == 0 and categorical > 0):
                        if(categorical > 1):
                                categorical = 0
                                several_cat = 1 
                
                return[numeric, several_num, categorical, several_cat, time_series]
                
        df_dtypes = return_datatypes(df)
        drawable_graphs = graphs.loc[(graphs["Numeric"] == df_dtypes[0]) & (graphs["Several Numeric"] == df_dtypes[1]) & (graphs["Categorical"] == df_dtypes[2]) & (graphs["Several Categorical"] == df_dtypes[3]) & (graphs["Time Series"] == df_dtypes[4])]

        def check_order_status(df : pd.DataFrame) -> []:
                orderings = []
                
                for c in df.columns:
                        if(return_datatype(df[c].dtypes) == 'Numeric'):
                                if(df[c].is_monotonic):
                                        orderings.append([c, True])
                                else:
                                        orderings.append([c, False])
                
                return orderings

        orderings = check_order_status(df)

        def calculate_row_cost(df : pd.DataFrame) -> float:
    
                cost = df.shape[0]
                
                return cost
                
        row_cost = calculate_row_cost(df)

        def check_groups(df : pd.DataFrame) -> []:
                groupings = []
                
                for c in df.columns:
                #         if(return_datatype(df[c].dtypes) == 'Categorical'):            
                #             flag = False
                        
                #             for group in df.groupby(c).size().values:
                #                 if group > 1:
                #                     flag = True
                                
                #             groupings.append([c, flag, df.groupby(c).size().shape[0]])
                        flag = False
                        
                        for group in df.groupby(c).size().values:
                                if group > 1:
                                        flag = True

                                groupings.append([c, flag, df.groupby(c).size().shape[0]])
                                
                return groupings

        groupings = check_groups(df)
        pd.DataFrame(groupings)
        if(len(groupings) == 0):
                groupings = [['', '', '']]
    
        df_lists = [groupings, orderings]

        characteristic_list = []

        for element in itertools.product(*df_lists):
                characteristic_list.append([element[0][0], element[0][1], element[0][2], element[1][0], element[1][1], row_cost])

        characteristics = pd.DataFrame(characteristic_list, columns = ['Grouping Column', 'Several Observations', 'Group Count', 'Ordering Column', 'Ordered', 'Row Count'])

        possible_drawings = []

        for combination in characteristics.values:
                several_obs = 0
                single_obs = 0
                ordered = 0
        
                if(combination[1]):
                        several_obs = 1
                        single_obs = 0
                else:
                        several_obs = 1
                        single_obs = 0
                
                if(combination[4]):
                        ordered = 1
                else:
                        ordered = 0

        combination_df = drawable_graphs.loc[((drawable_graphs["One Obs. Per Group"] == single_obs)
                                                & (graphs["Several Obs. Per Group"] == several_obs)
                                                & (graphs["Ordered"] == ordered)) | ((graphs["Several Obs. Per Group"] == 0)
                                                & (graphs["Ordered"] == 0))]
        
        
        possible_drawings.append(pd.DataFrame(combination_df.values, columns = graphs.columns))

        return render_template("results.html", title = 'Results Page',  possible_drawings = possible_drawings[0])

        