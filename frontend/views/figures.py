from bokeh.embed import components
from bokeh.plotting import figure


def harvestPerYear(x, y):
    """ vytvoření širšího lineárního plot grafu pro počet sklizní za rok"""
    # create a new plot with a title, size and axis labels
    p = figure(title="Number of harvests per year",
               plot_width=700,
               plot_height=450,
               x_axis_label='Year',
               y_axis_label='Harvests count'
               )

    # define ticks scale sorted list of years, range between max a min value
    p.xaxis.ticker = sorted(list(x))
    p.yaxis.ticker = list(range(y.min()+1, y.max()+1, 1))

    # add a line renderer with legend and line thickness
    p.line(x, y, line_width=1, line_color='#0000ff')

    return components(p)
