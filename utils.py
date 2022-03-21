import scipy.io
import pandas as pd
import random
import plotly.graph_objects as go
from dataclasses import make_dataclass
from plotly.subplots import make_subplots
from telegram import ReplyKeyboardMarkup

#Для работы с dataframe pandas
Point = make_dataclass("Point", [("Hist1", str), ("Hist2", str), ("Sim", int),
                                 ("NonSim", int), ("DontKnow", int)])
mat = scipy.io.loadmat('SHNOLL_BASE.mat')
SHNOLL_BASE = mat.get("SHNOLL_BASE")

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['Голосовать!'], ['Как сравнивать?']],
                                      parse_mode='bold',
                                      resize_keyboard=False)
    return my_keyboard

def write_answer_to_csv(answer):
    df = pd.read_csv(
        'answers.csv',
        delimiter=',',
        names=['Hist1', 'Hist2', 'Sim',
               'NonSim', 'Dont Know']
    )
    if answer == "Похожи":
        df.tail(n=1)[['Sim']].replace(0, 1)
    elif answer == "Не похожи":
        df.tail(n=1)[['NonSim']].replace(0, 1)
    else:
        df.tail(n=1)[['Dont Know']].replace(0, 1)
    with open('/content/gdrive/MyDrive/Saved_Hist111/answers.csv', 'a') as f:
        af.to_csv(f, header=False)

#Функция print_gist возвращает img_bytes
def print_gist(a):

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Scatter(y=SHNOLL_BASE[a[0]][a[1]][0], mode="lines", line=dict(color='rgb(15, 133, 84)', width=6)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=SHNOLL_BASE[a[2]][a[3]][0], mode="lines", line=dict(color='rgb(228, 26, 28)', width=6)),
                  row=1, col=2)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(annotations=[], overwrite=True)
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10, l=10, b=10, r=10)
    )
    # fig.show(config=dict(displayModeBar=False))
    img_bytes = fig.to_image(format="png")
    return img_bytes

#Функция  get_gists() возвращает рандомные индексы из SHNOLL_BASE для двух гистограмм
def get_gists():
    random.seed()
    x = random.choice([0, 1])
    if x == 0:
      y = random.randint(0, 23114)
      y1, y2 = y, y
      x1, x2 = 0, 1
    else:
      y1 = random.randint(0, 23114)
      y2 = random.randint(0, 23114)
      x1 = random.randint(0, 1)
      x2 = random.randint(0, 1)
    return [y1, x1, y2, x2]