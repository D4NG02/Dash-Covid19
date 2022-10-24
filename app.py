from distutils.log import debug
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

github_root = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/'
github_epidemic = 'epidemic/'
github_mysejahtera = 'mysejahtera/'
github_static = 'static/'
github_vaccination = 'vaccination/'


csv_population = 'population.csv'
population = pd.read_csv(github_root + github_static + csv_population)
population_state = population[population.columns[0]]
population_idxs = population[population.columns[1]]
population_pop = population[population.columns[2]]
population_pop_18 = population[population.columns[3]]
population_pop_60 = population[population.columns[4]]
population_pop_12 = population[population.columns[5]]
population_pop_5 = population[population.columns[6]]
# print(population_pop_5)

app = Dash(
    __name__,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap',
    ])

app.layout = html.Div(
    children = [
        html.H1(children='Population'),
        html.P(children='Show population ' + str(sum(population_pop))),
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': population_state,
                        'y': population_pop,
                        'type': 'lines',
                    }
                ],
                'layout': {'title': 'Total population'}
            }
        ),
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': population_state,
                        'y': population_pop_18,
                        'type': 'lines',
                    }
                ],
                'layout': {'title': 'Total population 18'}
            }
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)