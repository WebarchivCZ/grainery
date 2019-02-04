from math import pi
from bokeh.embed import components
from bokeh.plotting import figure, ColumnDataSource
from bokeh.palettes import Category20c
from bokeh.transform import cumsum


class Figures():
    """ generate graphs with bokeh library"""

    def harvestPerYear(self, x, y):
        """ vytvoření širšího lineárního plot grafu pro počet sklizní za rok"""
        # create a new plot with a title, size and axis labels
        p = figure(title="Number of harvests per year",
                   plot_width=700,
                   plot_height=450,
                   x_axis_label='Year',
                   y_axis_label='Harvests count',
                   tooltips=[('size', '@y')]
                   )

        # define ticks scale sorted list of years,
        # range between max a min value
        p.xaxis.ticker = sorted(x)
        p.yaxis.ticker = list(range(y.min()+1, y.max()+1, 1))

        # add a line renderers
        p.line(x, y, line_width=2, line_color='#0000ff')
        p.circle(x, y, fill_color="white", size=8)

        return components(p)

    def sizePerYear(self, x, y):
        """ vytvoření lineárního plot grafu pro velikost sklizní za rok"""
        # TODO převést jednotky velikosti na TB nebo GB
        # create a new plot with a title, size and axis labels
        p = figure(title="Size of archive per year",
                   plot_width=500,
                   plot_height=450,
                   x_axis_label='Year',
                   y_axis_label='Size',
                   tooltips=[('year', '@x'), ('size', '@top')]
                   )

        # define ticks scale sorted list of years,
        # range between max a min value
        p.xaxis.ticker = sorted(list(x))

        p.vbar(x=x, top=y, width=0.3)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        return components(p)

    def sizeGrowth(self, x, y):
        """ vytvoření grafu s nárůstem velikost"""
        # create a new plot with a title, size and axis labels
        p = figure(title="Archive Growth",
                   plot_width=500,
                   plot_height=450,
                   x_axis_label='Year',
                   y_axis_label='Size',
                   tooltips=[('size', '@y')]
                   )

        # define ticks scale sorted list of years
        # range between max a min value
        p.xaxis.ticker = sorted(list(x))

        # add a line renderer with legend and line thickness
        p.line(x, y, line_width=1, line_color='#0000ff')

        return components(p)

    def typesPie(self, typ):
        """vytvoření koláčového grafu pro typy sklizní"""

        data = typ.reset_index(name='value').rename(columns={'index': 'type'})
        data['angle'] = data['value']/data['value'].sum() * 2*pi
        data['color'] = Category20c[len(typ)]

        p = figure(plot_height=350, plot_width=400,
                   title="Harvest types", toolbar_location=None,
                   tools="hover", tooltips="@type: @value",
                   x_range=(-0.5, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color',
                legend='type', source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return components(p)

    def containerCount(self, df):
        """ vytvoření bodového grafu pro počet kontejnerů na sklizeň"""
        source = ColumnDataSource(df)

        p = figure(title="Number of containers per harvest",
                   x_range=df['_id'],
                   plot_width=700,
                   plot_height=450,
                   x_axis_label='Harvests (ordered by date)',
                   y_axis_label='Containers count',
                   tooltips=[("Harvest name", "@_id"),
                             ('Conteiner count', '@count')]
                   )

        p.vbar(x='_id', top='count', source=source, width=0.5)

        p.xaxis.major_label_orientation = 1
        p.y_range.start = 0
        p.toolbar.autohide = True

        return components(p)
