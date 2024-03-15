import customtkinter
import requests
from bs4 import BeautifulSoup
from CTkMessagebox import CTkMessagebox
import csv
import os
from datetime import datetime
import re
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser

date_format = '%d-%m-%Y %H-%M'

folderPath = os.path.dirname(os.path.abspath(__file__))

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x600")

price_label = None


# Controls The Big W Web Scraping Algo
titleslist = []

def BigWCall(URL):
    global titletxtBigW
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    page = requests.get(URL, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(page.content, "html.parser")
    priceBig1 = soup.find_all("span", {"class": "dollars"})
    title = soup.find('title')

    priceBigW = priceBig1[0].get("content")
    titletxtBigW = title.text
    titleslist.append(titletxtBigW)

    return f"{titletxtBigW} | Price: ${priceBigW}"


def KoganCall(URL):
    global titletxtKogan
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    page = requests.get(URL, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(page.content, "html.parser")
    priceKogan1 = soup.find_all("meta", {"property": "product:price:amount"})
    title = soup.find_all('meta', {'property': "og:title"})

    priceKogan = priceKogan1[0].get("content")
    titletxtKogan = title[0].get("content")
    titleslist.append(titletxtKogan)

    return f"{titletxtKogan} | Price: ${priceKogan}"


def CatchCall(URL):
    global titletxtCatch
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    page = requests.get(URL, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(page.content, "html.parser")
    priceCatch1 = soup.find_all("meta", {"itemprop": "price"})
    title = soup.find_all('meta', {'name': "description"})

    priceCatch = priceCatch1[0].get("content")
    titletxtCatch = title[0].get('content')
    titleslist.append(titletxtCatch)

    return f"{titletxtCatch} | Price: ${priceCatch}"


def EbayCall(URL):
    global titletxtEbay
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    page = requests.get(URL, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(page.content, "html.parser")
    priceEbay1 = soup.find("div", {"class": "x-price-primary"})
    title = soup.find('title')

    priceEbay = priceEbay1.text.replace("AU $",'').replace("US $","")
    titletxtEbay = title.text.replace('+',' ').replace("%28","").replace("%29","")
    titleslist.append(titletxtEbay)

    return f"{titletxtEbay.replace('for sale online','')} | Price: ${priceEbay}"





flag = False
# Controls the Add Products Button 
def addprod():
    global flag
    flag = True
    if optionmenu.get() == optionmenu._values[0] or optionmenu.get() == optionmenu._values[1] or optionmenu.get() == optionmenu._values[2] or optionmenu.get() == optionmenu._values[3] :
       productplus()
       for index3, button in enumerate(Buttonbox):
          if rowplus == index3 + 2:
             button.destroy()
             Buttonbox.pop(index3)

       for index4, button1 in enumerate(Button1box):
          if rowplus == index4 + 3:
             button1.destroy()
             Button1box.pop(index4)
    else:
       CTkMessagebox(title="Please Choose Store", message="Please Choose a Store Before Adding More Products ", icon="warning")
       
      
 




prodcall = [1]
URLBoxes = []
Optionbox = []
Buttonbox = []
Button1box = []
Cancelbox = []

# Controls the adding of entries when the add products button is used
def productplus():
    global prodcall
    global rowplus
    global optionmenu
    global URLBoxes
    global cancel
    global button1
    global button
    global Optionbox
    global Buttonbox
    global Button1box
    global Cancelbox

    rowplus = len(prodcall) + 1
    prodcall.append(rowplus)

    Url = customtkinter.CTkEntry(master=frame, width=600, placeholder_text="URL")
    Url.grid(row=rowplus, column=0, padx=10, pady=12)
    URLBoxes.append(Url)

    optionmenu = customtkinter.CTkOptionMenu(master=frame, values=["Big W", "Kogan", "Catch", "Ebay"])
    optionmenu.grid(row=rowplus, column=1, padx=10, pady=12)
    optionmenu.set("Please Choose A Store")
    Optionbox.append(optionmenu)

    if len(Buttonbox) > 0:
        Buttonbox[-1].destroy()
        Buttonbox.pop()
    if len(Button1box) > 0:
        Button1box[-1].destroy()
        Button1box.pop()
    

    button = customtkinter.CTkButton(master=frame, text="Add Product", command=addprod)
    button.grid(row=rowplus+1, column=0, columnspan=2, pady=12, padx=10)
    Buttonbox.append(button)

    button1 = customtkinter.CTkButton(master=frame, text="Compare", command=pricecomp)
    button1.grid(row=rowplus+1, column=1, columnspan=2, pady=12, padx=10, sticky='w')
    Button1box.append(button1)
    
    cancel = customtkinter.CTkButton(master=frame, text="X", command=lambda rownum=rowplus: removebutton(rownum), width=10, height=10)
    cancel.grid(row=rowplus, column=2, columnspan=2, pady=1, padx=1)
    Cancelbox.append(cancel)


    if len(prodcall) == 5:
        button.destroy()
        CTkMessagebox(title="Maximum Amount Reached", message="Maximum Amount of Trackable Products Reached ", icon="info")
   
    rowplus += 1

def removebutton(rownum):
    
   for index, box in enumerate(URLBoxes):
    if rownum == index + 1:
       box.destroy()
       prodcall.pop()
       URLBoxes.pop(index)
   
   for index2, option in enumerate(Optionbox):
    if rownum == index2 + 2:
       option.destroy()
       Optionbox.pop(index2)

   for index4, button1 in enumerate(Button1box):
    if rownum == 2:
       button1.destroy()  
       Button1box.pop(index4)
        
   for index5, cancel in enumerate(Cancelbox):
    if rownum == index5 + 2:
       cancel.destroy() 
       Cancelbox.pop(index5) 
    
   if rowplus - 1 == rownum:
     try:
       button = customtkinter.CTkButton(master=frame, text="Add Product", command=addprod)
       button.grid(row=rowplus, column=0, columnspan=2, pady=12, padx=10)
       Buttonbox.append(button)
     except len(Buttonbox) > 1:
       return
    
   elif rowplus ==  6:
      button = customtkinter.CTkButton(master=frame, text="Add Product", command=addprod)
      button.grid(row=rowplus, column=0, columnspan=2, pady=12, padx=10)
    
URLStore = []
# Controls the compare price button
def pricecomp():
    global URLBoxes
    global price_label
    global prices
    global Url_val
    prices = []
    errors = []
    titleslist.clear()
    URLStore.clear()

    if  price_label:
       price_label.destroy()

    for box in URLBoxes:
         Url_val = box.get()
         errors.append(Url_val)
         if optionmenu.get() == optionmenu._values[0] or optionmenu.get() == optionmenu._values[1] or optionmenu.get() == optionmenu._values[2] or optionmenu.get() == optionmenu._values[3]:

           if Url_val:   
            if 'bigw.com.au' in Url_val or optionmenu.get() == optionmenu._values[0]:
              try:
                 price = BigWCall(Url_val)
                 prices.append(price)
                 URLStore.append(Url_val)
                 save = customtkinter.CTkButton(master=frame, text='Save', command = saveprod)
                 save.grid(row = 10, column=0, columnspan=2, pady=12, padx=10)
              except requests.exceptions.MissingSchema:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')
              except IndexError:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')

            elif 'kogan.com' in Url_val or optionmenu.get() == optionmenu._values[1]:
              try:
                 price = KoganCall(Url_val)
                 prices.append(price)
                 URLStore.append(Url_val)
                 save = customtkinter.CTkButton(master=frame, text='Save', command = saveprod)
                 save.grid(row = 10, column=0, columnspan=2, pady=12, padx=10)
              except requests.exceptions.MissingSchema:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')
              except IndexError:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')

            elif 'catch.com.au' in Url_val or optionmenu.get() == optionmenu._values[2]:
              try:
                 price = CatchCall(Url_val)
                 prices.append(price)
                 URLStore.append(Url_val)
                 save = customtkinter.CTkButton(master=frame, text='Save', command = saveprod)
                 save.grid(row = 10, column=0, columnspan=2, pady=12, padx=10)
              except requests.exceptions.MissingSchema:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')
              except IndexError:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')

            elif 'ebay.com' in Url_val or optionmenu.get() == optionmenu._values[3]:
              try:
                 price = EbayCall(Url_val)
                 prices.append(price)
                 URLStore.append(Url_val)
                 save = customtkinter.CTkButton(master=frame, text='Save', command = saveprod)
                 save.grid(row = 10, column=0, columnspan=2, pady=12, padx=10)
              except requests.exceptions.MissingSchema:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')
              except IndexError:
                 CTkMessagebox(title='Invalid URL', message=f'Invalid URL Entered. Please Enter a Valid URL in Box {errors.index(Url_val)+1}',icon='cancel')


           if Url_val == '':
              CTkMessagebox(title='No URL Entered', message=f'Please Enter a URL in Box {errors.index(Url_val)+1}',icon='warning')
           
           if duplicheck(URLStore):
              CTkMessagebox(title='Duplicates Present', message=f'A Duplicate URL Has Been Entered, Please Remove It',icon='warning')

         else:  
           CTkMessagebox(title="Please Choose a Store", message="Please Choose a Store Before Comparing ", icon="warning")

    price_label = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 16))
    price_label.grid(row=rowplus+2, column=0, columnspan=2, pady=12, padx=10)
    price_label.configure(text="\n".join([f"{price}" for price in prices]))
    
def duplicheck(list):
   return any(list.count(i)>1 for i in list)


def fileclean(filename):  
   fileclean = re.sub(r'[\\/:*?"<>|]', '',filename)
   fileclean = fileclean + ".csv"
   return fileclean


def saveprod():
   global filename
   global csvfolder
   global column_names
   savechoice = CTkMessagebox(title="Save?", message="Are you sure you would like to save these products no further changes can be made to this comparison", icon="warning", option_1='Yes', option_2='No')
   response = savechoice.get()
   if response == 'Yes':
     dialog = customtkinter.CTkInputDialog(text="Please Enter a Name for Your CSV File:", title="CSV Filename")
     column_names = ['Date']
     i = 0
     while i < len(URLStore):
        column_names.append(titleslist[i] + "("+ URLStore[i]+')')
        i += 1
     csvfolder = 'csv_files'
     if not os.path.exists(csvfolder):
        os.mkdir(csvfolder)
     filename = os.path.join(csvfolder, f'{datetime.now().strftime(date_format)} {fileclean(dialog.get_input())}')
     with open(filename, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(column_names)
      cutPrices = []
      cutPrices.append(datetime.now().strftime(date_format))
      for price in prices:
         t, temp = price.split('$')
         cutPrices.append(temp)
      writer.writerow(cutPrices)
      homefunc()
   else:
      return

graph_frame = None

def homefunc():
   plt.close()
   frame.destroy()
   URLBoxes.clear()
   Optionbox.clear()
   Buttonbox.clear()
   Button1box.clear()
   prodcall.clear()
   prodcall.append(1)
   Cancelbox.clear()
   titleslist.clear()
   URLStore.clear()
   mainwin()
   if graph_frame is not None:
      graph_frame.destroy()

def graphmenu():
    global graph_frame

    frame.destroy()
    if graph_frame is not None:
       graph_frame.destroy()
    plt.close()

    graph_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
    graph_frame.pack(pady=20, padx=60, fill="both", expand=False)
    graph_frame.place(relx=.5, rely=.5, anchor="center")

    graph_label = customtkinter.CTkLabel(master=graph_frame, text="Graph Menu", font=("Roboto", 24))
    graph_label.grid(row=0, column=0, columnspan=2, pady=12, padx=10)
    
    csvfolder = 'csv_files'
    if not os.path.exists(csvfolder):
      os.mkdir(csvfolder)
    csvlist = [file for file in os.listdir(csvfolder) if file.endswith('.csv')]

    if csvlist:
       for index, csvlists in enumerate(csvlist):
          filebutton = customtkinter.CTkButton(master=graph_frame, text=csvlists, command=lambda file=csvlists: graphview(file))
          filebutton.grid(row=index+1, column=0, columnspan=2, pady=12, padx=10)
    else:
      nofile_label = customtkinter.CTkLabel(master=graph_frame, text="No CSV files found, please start a comparison to create CSV files", font=("Roboto", 24))
      nofile_label.grid(row=1, column=0, columnspan=2, pady=12, padx=10)
    
graphwin = None
def graphview(file):
   global graphwin
   if graphwin is not None:
     graphwin.destroy()
     plt.close()

   graphwin = customtkinter.CTkToplevel(master=graph_frame)
   graphwin.geometry('800x500')
   graphwin.after(100, graphwin.lift)

   filenamelabel = customtkinter.CTkLabel(master=graphwin, text=file, font=("Roboto", 20))
   filenamelabel.pack(padx=10,pady=15,side='top')

   deletebutton = customtkinter.CTkButton(master=graphwin, text="Delete File", command=lambda file=file: graphdel(file))
   deletebutton.pack(padx=10,pady=10,side='bottom')
   
   compnowbutton = customtkinter.CTkButton(master=graphwin, text="Compare & Update Prices Now", command=lambda file=file: compnow(file))
   compnowbutton.pack(padx=10,pady=10,side="bottom")

   openurlbutton = customtkinter.CTkButton(master=graphwin, text="Open Products In Browser", command=lambda file=file: openlinks(file))
   openurlbutton.pack(padx=10,pady=10,side="bottom")

   showgraphbutton = customtkinter.CTkButton(master=graphwin, text="Show Graph", command=lambda file=file: graphplt(file))
   showgraphbutton.pack(padx=10,pady=10,side="bottom")

def graphplt(file):
   plt.close()
   filepath = fr"{folderPath}\csv_files\{file}"

   df = pd.read_csv(filepath)

   plt.figure(figsize=(10, 6)) 

   legendlist = []
     
   for column in df.columns:
     if column != 'Date':
        legendsplit = column.split('(')[0]
        legendlist.append(legendsplit)
        plt.plot(df['Date'], df[column], label=column, marker='o')
        ymin,ymax = plt.ylim()
        for i in range(len(df['Date'])):
         plt.annotate(f'{df[column][i]:.2f}', (df['Date'][i], df[column][i]), textcoords="offset points", xytext=(0,10),ha='center')
   
   plt.xlabel('Date')
   plt.ylabel('Price')
   plt.title('Product Prices Over Time')
   plt.ylim(0,ymax+200)
   plt.legend(legendlist,loc='upper left')
 
   plt.grid(True)
   plt.show()



def graphdel(file):
   filepath = fr"{folderPath}\csv_files\{file}"
   os.remove(filepath)
   graphwin.destroy()
   plt.close()
   graph_frame.destroy()
   graphmenu()


priceshow = None
def compnow(file):
   plt.close()
   global priceshow
   global prodlinks
   if priceshow is not None:
      priceshow.destroy()
   csvprices = []
   filepath = fr"{folderPath}\csv_files\{file}"
   df = pd.read_csv(filepath)
   prodlinks = [col.split('(')[-1][:-1] for col in df.columns[1:]]
   for links in prodlinks:
      if 'bigw.com.au' in links:
        try:
         csvprice = BigWCall(links)
         csvprices.append(csvprice)
        except IndexError:
         CTkMessagebox(title="Duplicate", message="Your Comparison Contains Duplicate Products Which Are Not Displayed Here", icon="warning")
           
      elif 'kogan.com' in links:
        try:
         csvprice = KoganCall(links)
         csvprices.append(csvprice)
        except IndexError:
         CTkMessagebox(title="Duplicate", message="Your Comparison Contains Duplicate Products Which Are Not Displayed Here", icon="warning")
         
      elif 'catch.com.au' in links:
        try:
         csvprice = CatchCall(links)
         csvprices.append(csvprice)
        except IndexError:
         CTkMessagebox(title="Duplicate", message="Your Comparison Contains Duplicate Products Which Are Not Displayed Here", icon="warning")
      
      elif 'ebay.com' in links:
        try:
         csvprice = EbayCall(links)
         csvprices.append(csvprice)
        except IndexError:
         CTkMessagebox(title="Duplicate", message="Your Comparison Contains Duplicate Products Which Are Not Displayed Here", icon="warning")



   priceshow = customtkinter.CTkLabel(master=graphwin, text="", font=("Roboto", 16))
   priceshow.pack(padx=10,pady=10,side="bottom")
   priceshow.configure(text="\n".join([f"{csvprice}" for csvprice in csvprices]))

   newprice = [datetime.now().strftime(date_format)] + [price.split('$')[1] for price in csvprices]
   df.loc[len(df)] = newprice
   df.to_csv(filepath, index=False)

   graphplt(file)

def openlinks(file):
   filepath = fr"{folderPath}\csv_files\{file}"
   df = pd.read_csv(filepath)
   prodlinks = [col.split('(')[-1][:-1] for col in df.columns[1:]]

   for links in prodlinks:
      webbrowser.open(links)



def closeroot():
   plt.close()
   root.destroy()

# Main init code     
def mainwin():
  global frame
  global optionmenu
  global Url
  global button

  frame = customtkinter.CTkFrame(master=root,fg_color="transparent")
  frame.pack(pady=20, padx=60, fill="both", expand=False)
  frame.place(relx=.5, rely=.5,anchor="center")

  label = customtkinter.CTkLabel(master=frame, text="Product Price Tracker", font=("Roboto", 24))
  label.grid(row=0, column=0, columnspan=2, pady=12, padx=10)

  Url = customtkinter.CTkEntry(master=frame, width=600, placeholder_text="URL")
  Url.grid(row=1, column=0, padx=10, pady=12)

  URLBoxes.append(Url)

  optionmenu = customtkinter.CTkOptionMenu(master=frame, values=["Big W", "Kogan", "Catch", "Ebay"])
  optionmenu.grid(row=1, column=1, padx=10, pady=12)
  optionmenu.set("Please Choose A Store") 

  button = customtkinter.CTkButton(master=frame, text="Add Product", command=addprod)
  button.grid(row=2, column=0, columnspan=2, pady=12, padx=10)
  Buttonbox.append(button)

mainwin()
# Main init code


# Sidebar Code
homeimage = ImageTk.PhotoImage(Image.open('homeicon.png').resize((20,20), Image.BILINEAR))
graphimage = ImageTk.PhotoImage(Image.open('graphicon.png').resize((20,20), Image.BILINEAR))

sidebar = customtkinter.CTkFrame(master=root, width=70,)
sidebar.pack(side="left", fill="y")

homebutton = customtkinter.CTkButton(master=sidebar, image=homeimage, text = '', command=homefunc, width = 30, height= 30)
homebutton.pack(pady=10, padx=10)

graphbutton = customtkinter.CTkButton(master=sidebar, image=graphimage, text = '', command=graphmenu, width = 30, height= 30)
graphbutton.pack(pady=10, padx=10)
# Sidebar Code

root.protocol("WM_DELETE_WINDOW",closeroot)


root.mainloop()
