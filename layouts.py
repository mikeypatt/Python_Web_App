import dash_core_components as dcc
import dash_html_components as html
import components_plus_methods as cm
import style as app_style

VHS = {
    "g_timeline": "30vh",
    "g_avg_daily": "20vh",
    "g_estm_cost": "20vh",
    "g_avg_serious": "20vh",
    "g_top5": "58vh",
    "g_total": "34vh",
    "h": "1vh",
}
CPANEL_ML = 1.7


def g_disclaimer():
    return [
        html.H2(
            children=[
                "DISCLAIMER"
            ],
            style={
                'textAlign': 'center',
                'padding-top': 5
            },
        ),
        html.Div(
            children=[
                "                                                                "
                "These interactive figures are generated using publicly available monthly data. "
                "A certain month is included on the map if more than 15 days are selected."
                " The statistics tab shows monthly data normalized over the requested range."
            ],
            style={
                'textAlign': 'center',
            },
        ),
    ]


def g_tab1():
    return dcc.Tab(
        label='Map',
        value='tab-1',
        style=app_style.tab_style,
        selected_style=app_style.tab_selected_style,
        children=[
            dcc.Loading(
                dcc.Graph(
                        id="map-graph",
                        config={
                            'displaylogo': False,
                        },
                        style={
                            "position": "absolute",
                            "bottom": "10px",
                            "top": "40px",
                            "left": "26%",
                            "right": "10px",
                            "background": "#292927",
                        },
                    )
                ,
                type="default",
            ),
             html.Div(
                 style={
                     'position': 'absolute',
                     'bottom': '10px',
                     'right': '10px',
                     'height': "100px",
                     "width": "300px",
                     "z-index": "1",
                     "opacity": "0.3",
                     "background": ""
                 },
                 children=g_disclaimer()
            ),
        ],
    )


def g_timeline():
    return html.Div(
        children=[
            html.H3(
                children=["Crime timeline in X from Date to Date"],
                id="timeline-graph-title",
                style={"height": VHS["h"]},
            ),
            dcc.Graph(
                id="timeline-graph",
                config={
                    'displaylogo': False,
                    "responsive": True,
                },
                style={
                    "height": VHS["g_timeline"],
                },
            )
        ],
        style={
            "grid-column": "1 / span 5",
            "grid-row": "1 / span 1",
        }
    )


def g_avg_daily():
    return html.Div(
        children=[
            html.Div([
                html.H3(
                    children=['Avg Daily Crime'],
                    id="avg-daily-title",
                    style={"height": VHS["h"]},
                ),
                dcc.Graph(
                    id="avg-daily",
                    config={
                        'displaylogo': False,
                        "responsive": True,
                    },
                    style={
                        "height": VHS["g_avg_daily"],
                    },
                )
            ]),
        ],
        style={
            "grid-column": "1 / span 1",
            "grid-row": "2 / span 1",
        }
    )


def g_estm_cost():
    return html.Div(
        children=[
            html.Div([
                html.H3(
                    children=['Crime Density'],
                    id="estm-cost-title",
                    style={"height": VHS["h"]},
                ),
                dcc.Graph(
                    id="estm-cost",
                    config={
                        'displaylogo': False,
                        "responsive": True,
                    },
                    style={
                        "height": VHS["g_estm_cost"],
                    },
                )
            ]),
        ],
        style={
            "grid-column": "2 / span 1",
            "grid-row": "2 / span 1",
        }
    )


def g_avg_serious():
    return html.Div(
        children=[
            html.Div([
                html.H3(
                    children=['Avg Monthly Crime'],
                    id="avg-serious-title",
                    style={"height": VHS["h"]},
                ),
                dcc.Graph(
                    id="avg-serious",
                    config={
                        'displaylogo': False,
                        "responsive": True,
                    },
                    style={
                        "height": VHS["g_avg_serious"],
                    },
                )
            ]),
        ],
        style={
            "grid-column": "3 / span 1",
            "grid-row": "2 / span 1",
        }
    )


def g_top5():
    return html.Div(
        children=[
            html.Div([
                html.H3(
                    children=['Top 5 crime boroughs from Date to Date'],
                    id="bar-graph-title",
                    style={"height": VHS["h"]},
                ),
                dcc.Graph(
                    id="bar-graph",
                    config={
                        'displaylogo': False,
                        "responsive": True,
                    },
                    style={
                        "height": VHS["g_top5"],
                    },
                )
            ]),
        ],
        style={
            "grid-column": "4 / span 2",
            "grid-row": "2 / span 3",
            "margin-left": "10px",
        }
    )


def g_total():
    return html.Div(
        children=[
            html.H3(
                children=['Total crime in X from Date to Date'],
                id="pie-chart-title",
                style={"height": VHS["h"]},
            ),
            dcc.Graph(
                id='pie-chart',
                config={
                    'displaylogo': False,
                    "responsive": True,
                },
                style={
                    "height": VHS["g_total"],
                },
            )
        ],
        style={
            "grid-column": "1 / span 3",
            "grid-row": "3 / span 2",
        }
    )


def g_tab2():
    return dcc.Tab(
        label='Statistics',
        value='tab-2',
        style=app_style.tab_style,
        selected_style=app_style.tab_selected_style,
        children=[
            html.Div(
                children=[
                    dcc.Loading(
                        [html.Div(
                            children=[
                                g_timeline(),
                                g_avg_daily(),
                                g_avg_serious(),
                                g_estm_cost(),
                                g_top5(),
                                g_total(),
                            ],
                            style={
                                "display": "grid",
                                "grid-template-columns": "auto auto auto auto auto",
                                "grid-template-rows": "auto auto auto auto",

                                "position": "absolute",
                                "bottom": "10px",
                                "top": "40px",
                                "left": "26%",
                                "right": "10px",
                                "background": "#1e1e1e",
                            },
                        )]
                    )
                ],
            )
        ],
    )


def g_tabs():
    return html.Div(
        className="eight columns",
        children=[
            html.Div(
                className="div-for-charts",
                children=[
                    dcc.Tabs(
                        id="tabs-styled-with-props",
                        value='tab-1',
                        children=[
                            g_tab1(),
                            g_tab2(),
                        ],
                        style={
                            "margin-left": f"-{CPANEL_ML + .7}%",
                        }
                    ),
                ],
            ),
        ],
    )


def g_panel():
    return html.Div(
        className="three columns",
        children=[
            html.Div(
                html.H1(
                    className="div-for-title",
                    children="A  G  A  T  H  A",
                    style={
                        'textAlign': 'center',
                        'padding': 5,
                    },
                ),
            ),
            html.Div(
                html.H2(
                    className="div-for-search-title",
                    children="CRIME SEARCH",
                    style={
                        'textAlign': 'center',
                    },
                )
            ),
            html.Div(
                className="div-for-area-beneath-control-tabs",
                children=[
                    dcc.Tabs([
                        dcc.Tab(label='Past', style=app_style.control_tab_style,
                                selected_style=app_style.control_tab_selected_style, children=[
                                html.Div(
                                    className="div-for-area-beneath-control-tabs",
                                    children=[
                                        html.Div(
                                            className="div-for-date-selector",
                                            children=[cm.date_selector_past()],
                                        ),

                                        html.Div(
                                            children=[html.Div(
                                                className="div-for-dropdown",
                                                children=[cm.crime_selector()],
                                                style={
                                                    'width': '39%', 'display': 'inline-block', 'float': 'left',
                                                }
                                            ),
                                                html.Div(
                                                    className="div-for-dropdown",
                                                    children=[cm.location_selector()],
                                                    style={
                                                        'width': '39%', 'display': 'inline-block',
                                                        'float': 'right',
                                                    }
                                                ),
                                            ],
                                         ),html.Div(
                                                className="div-for-search-button",
                                                children=[html.Button('Search', id='button')],
                                                style={
                                                    # 'width': '50%', 'display': 'inline-block','textAlign':'center',
                                                    # 'margin-top': '10px','float': 'center', 'display': 'inline-block',
                                                    # 'margin-left': '22%',
                                                }
                                            ),
                                    ],
                                ),
                            ]),

                        dcc.Tab(label='Future', style=app_style.control_tab_style,
                                selected_style=app_style.control_tab_selected_style, children=[

                                html.Div(
                                    className="div-for-date-selector",
                                    children=[cm.date_selector_future()],
                                ),

                                html.Div(
                                    children=[html.Div(
                                        className="div-for-dropdown",
                                        children=[cm.fut_crime_selector()],
                                        style={
                                            'width': '39%', 'display': 'inline-block', 'float': 'left',
                                        }
                                    ),
                                        html.Div(
                                            className="div-for-dropdown",
                                            children=[cm.fut_location_selector()],
                                            style={
                                                'width': '39%', 'display': 'inline-block',
                                                'float': 'right',
                                            }
                                        ),
                                    ]),html.Div(
                                                className="div-for-search-button",
                                                children=[html.Button('Search')],
                                                style={
                                                    # 'width': '50%', 'display': 'inline-block','textAlign':'center',
                                                    # 'margin-left': '125px','margin-top': '10px'
                                                }
                                            ),
                            ]),
                    ]),
                ],
            ),
            html.Div(
                className="space to fill gap of address search",
                style={
                    'padding': '1em',
                    'background-color': '#292927',
                    'margin-left': '5px',
                }
            ),
            html.Div(
                className="div-for-news-stream",
                children=[
                    html.Div(
                        html.H2(
                            className="div-for-search-title",
                            children="NEWS",
                            style={
                                'textAlign': 'center',
                                'overflow': 'auto'
                            })
                    ),
                    html.Iframe(
                        src="https://feed.mikle.com/widget/v2/126269/?preloader-text=Loading",
                        style={
                            'textAlign': 'center',
                            "width": "264px",
                            "height": "438px",
                            "pointer-events": "none",
                            "cursor": "default"
                        },
                    ),
                ],
                style={
                    'textAlign': 'center',
                }
            ),
        ],
        style={
            "margin-left": f"{CPANEL_ML}%",
        },
    )


def new_layout():
    return html.Div(
        style={
            'margin-top': '8px',
        },
        children=[
            g_panel(),
            g_tabs(),
        ],
    )
