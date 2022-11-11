# assorted links for figuring out how to use pygsheets (some more helpful than others)

# https://erikrood.com/Posts/py_gsheets.html
# https://github.com/nithinmurali/pygsheets

import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='/Users/caroline.buck/Desktop/Fun_R/shinylive-test/frolidays-8b363e98f7b9.json')

# Create empty dataframe
df = pd.DataFrame()
df['names'] = ['colin','caro','claire']

# had to make new sheet before could open it (b/c service key for api is assoc w/ service acct, not my regular email)
res = gc.sheet.create("frolidays_rsvp")  # Please set the new Spreadsheet name.
sh = gc.open('frolidays_rsvp')
wks = sh.sheet1


#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))

# Update a cell with value (just to let him know values is updated ;) )
wks.update_value('A1', "Hey yank this numpy array")
import numpy as np
my_nparray = np.random.randint(10, size=(3, 4))

# update the sheet with array
wks.update_values('A2', my_nparray.tolist())

# share the sheet with your friend --> v helpful lol. idk how to see sheet from service acct. 
sh.share("cbuck717@gmail.com")


## get whole thing as df, then reset as df in shiny app
wks.clear()
wks.update_value('A1', "name")
wks.update_value('B1', "bringing")

df = wks.get_as_df() # get current sheet content as df
new = pd.DataFrame()
new['name'] = ['caro']
new['bringing'] = ['fajitas']

df = df.append(new).reset_index(drop=True)

wks.set_dataframe(df,(1,1))

#you can also get the values of sheet as dataframe
df = wks.get_as_df()

df.tail()['name'].iloc[0]
