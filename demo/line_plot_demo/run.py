import pandas as pd
from random import randint, random
import gradio as gr


temp_sensor_data = pd.DataFrame(
    {
        "time": pd.date_range("2021-01-01", end="2021-01-05", periods=200),
        "temperature": [randint(50 + 10 * (i % 2), 65 + 15 * (i % 2)) for i in range(200)],
        "humidity": [randint(50 + 10 * (i % 2), 65 + 15 * (i % 2)) for i in range(200)],
        "location": ["indoor", "outdoor"] * 100,
    }
)

food_rating_data = pd.DataFrame(
    {
        "cuisine": [["Italian", "Mexican", "Chinese"][i % 3] for i in range(100)],
        "rating": [random() * 4 + 0.5 * (i % 3) for i in range(100)],
        "price": [randint(10, 50) + 4 * (i % 3) for i in range(100)],
        "wait": [random() for i in range(100)],
    }
)

with gr.Blocks() as line_plots:
    with gr.Row():
        start = gr.DateTime("2021-01-01 00:00:00", label="Start")
        end = gr.DateTime("2021-01-05 00:00:00", label="End")
        apply_btn = gr.Button("Apply", scale=0)
    with gr.Row():
        group_by = gr.Radio(["None", "30m", "1h", "4h", "1d"], value="None", label="Group by")
        aggregate = gr.Radio(["sum", "mean", "median", "min", "max"], value="sum", label="Aggregation")

    temp_by_time = gr.LinePlot(
        temp_sensor_data,
        x="time",
        y="temperature",
    )
    temp_by_time_location = gr.LinePlot(
        temp_sensor_data,
        x="time",
        y="temperature",
        color="location",
    )

    time_graphs = [temp_by_time, temp_by_time_location]
    group_by.change(
        lambda group: [gr.LinePlot(x_bin=None if group == "None" else group)] * len(time_graphs),
        group_by,
        time_graphs
    )
    aggregate.change(
        lambda aggregate: [gr.LinePlot(y_aggregate=aggregate)] * len(time_graphs),
        aggregate,
        time_graphs
    )

    def rescale(select: gr.SelectData):
        return select.index
    rescale_evt = gr.on([plot.select for plot in time_graphs], rescale, None, [start, end])

    for trigger in [apply_btn.click, rescale_evt.then]:
        trigger(
            lambda start, end: [gr.LinePlot(x_lim=[start, end])] * len(time_graphs), [start, end], time_graphs
        )

    price_by_cuisine = gr.LinePlot(
        food_rating_data,
        x="cuisine",
        y="price",
    )
    with gr.Row():
        price_by_rating = gr.LinePlot(
            food_rating_data,
            x="rating",
            y="price",
        )
        price_by_rating_color = gr.LinePlot(
            food_rating_data,
            x="rating",
            y="price",
            color="cuisine",
            color_map={"Italian": "red", "Mexican": "green", "Chinese": "blue"},
        )

if __name__ == "__main__":
    line_plots.launch()
