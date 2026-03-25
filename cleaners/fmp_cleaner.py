import ast
import pandas as pd 


def parse_dict_col(df, col=None, col_lst=None):
    if col is None and col_lst is not None:
        for col in col_lst:
                try: 
                    expanded = pd.json_normalize(df[col])
                    df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
                    return df
                except Exception as e:
                     df[col] = df[col].apply(ast.literal_eval)
                     expanded = pd.json_normalize(df[col])
                     df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
                     return df
    if col is not None and col_lst is None:
         try: 
            expanded = pd.json_normalize(df[col])
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            return df
         except Exception as e:
            df[col] = df[col].apply(ast.literal_eval)
            expanded = pd.json_normalize(df[col])
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            return df