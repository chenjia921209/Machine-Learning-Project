from matplotlib import pyplot as plt


def bar_chart(df, column, title, xlabel, ylabel): 
    """ Generate a bar chart for a given column in the dataframe """ 
    plt.figure(figsize=(10,6)) 
    plt.barh(df["food"], df[column], color='skyblue') 
    plt.title(title) 
    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.show()
    