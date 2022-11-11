from shiny import App, render, ui, reactive
import matplotlib.pyplot as plt
import numpy as np

import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='/Users/caroline.buck/Desktop/Fun_R/shinylive-test/frolidays-8b363e98f7b9.json')
sh = gc.open('frolidays_rsvp')
wks = sh.sheet1

# Note that if the window is narrow, then the sidebar will be shown above the
# main content, instead of being on the left.

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            "What will you bring to Frolidays?",
            ui.input_text("name", "Name(s): ", placeholder="Enter text"),
            ui.input_text("dish", "What you're bringing to share: ", placeholder="Enter text"),
            ui.input_action_button("btn", "Sign me up!"),),
        ui.panel_main(
            ui.output_text_verbatim("txt", placeholder=True),
            ui.output_table("result"),
            ),
    ),
)


def server(input, output, session):
    # The @reactive.event() causes the function to run only when input.btn is
    # invalidated.
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
        print(f"You clicked the button!")
        # You can do other things here, like write data to disk.
        df = wks.get_as_df() # get current sheet content as df
        new = pd.DataFrame()
        new['name'] = [input.name()]
        new['bringing'] = [input.dish()]
        df = df.append(new).reset_index(drop=True)
        wks.set_dataframe(df,(1,1))
        

    # This output updates only when input.btn is invalidated.
    @output
    @render.text
    @reactive.event(input.btn)
    def txt():
        df = wks.get_as_df()
        return f"See ya soon! Don't forget your festive wear and the {df.iloc[-1]['bringing']}!"
        #return f"{input.name()} is coming and bringing {input.dish()}"


    @output
    @render.table
    @reactive.event(input.btn, ignore_none=False)
    def result():
        df = wks.get_as_df()
            # If we're not highlighting values, we can simply
            # return the pandas data frame as-is; @render.table
            # will call .to_html() on it.
        return df

    

    


app = App(app_ui, server)

