import datetime as dt

# filters data frame by date
# defined for luftklima_reformatted.csv and verkehrszählungen_reformatted.csv
def filter_date(df, start, end):
    if "Date" in df.columns:
        df2 = df
        df2.Date = df2.Date.apply(lambda x: dt.datetime.strptime(x, "%d.%m.%Y"))
        filter_df = df2[(df2.Date >= start) & (df2.Date <= end)]
    elif "Datum" in df.columns:
        filter_df = df[(df.Datum >= start) & (df.Datum <= end)]
    else:
        filter_df = None

    return filter_df 
