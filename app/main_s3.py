import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from botoTest import CSV

plt.rc('font', family='NanumGothic')
mpl.rcParams['axes.unicode_minus'] = False

csv = CSV()

df = csv.read()

df_index = ["Index","Date","Type","Category","Item","Amount", "Note"]
category_list = ["식비","카페","교통비","생일선물","용돈"]

def calBalance(df):
    used_money = int(sum(df[df["Type"]=="지출"]["Amount"]))
    gotten_money = int(sum(df[df["Type"]=="수입"]["Amount"]))
    return gotten_money - used_money

#CREATE
def addData(date,type,category,item,amount, note):
    global df, df_balance
    now_index = df.iloc[-1]["Index"]
    new_df = pd.DataFrame({ "Index" : now_index + 1,
           "Date":[date],
           "Type":[type],
           "Category":[category],
           "Item":[item],
           "Amount":[amount],
           "Note":[note]})
    df = pd.concat([df,new_df],ignore_index=True)
    csv.write(df)
    
    return df.tail(1)
#READ
def viewAllData():
    global df
    return [df, calBalance(df)]
#UPDATE
def updateData(index,date,type,category,item,amount,note):
    global df
    df.loc[df["Index"] == index, "Date"] = date
    df.loc[df["Index"] == index, "Type"] = type
    df.loc[df["Index"] == index, "Category"] = category
    df.loc[df["Index"] == index, "Item"] = item
    df.loc[df["Index"] == index, "Amount"] = amount
    df.loc[df["Index"] == index, "Note"] = note
    
    csv.write(df)
    
    return "정보업데이트 완료"
#DELETE
def deleteData(index):
    global df, df_balance
    
    df = df.drop(df[df["Index"]==index].index)
    
    csv.write(df)
    
    return calBalance(df)
    
def loadIndex(index):
    global df
    i_df = df[df["Index"]==int(index)]
    #["Index","Date","Type","Item","Category","Amount", "Note"]
    return [i_df.iloc[0,1],i_df.iloc[0,2],i_df.iloc[0,3],i_df.iloc[0,4],i_df.iloc[0,5],i_df.iloc[0,6]]

def barPlot_fn(display,search_month):
    global df
    if display == "ALL":
        gotten_money = int(sum(df[df["Type"]=="수입"]["Amount"]))
        used_money = int(sum(df[df["Type"]=="지출"]["Amount"]))
        x = ["지출","수입"]
        y = [used_money,gotten_money]

        fig = plt.figure()
        plt.barh(x,y, color=['b','r'],height=0.3)
        plt.subplots_adjust( top=0.7, bottom=0.4)
        plt.title("전체 수입/지출")

        return [fig ,gotten_money, used_money]
    elif display == "MONTHLY":
        month_df = df[df["Date"].str.contains(f"^{search_month}")]
        gotten_money = int(sum(month_df[month_df["Type"]=="수입"]["Amount"]))
        used_money = int(sum(month_df[month_df["Type"]=="지출"]["Amount"]))
        x = ["지출","수입"]
        y = [used_money,gotten_money]

        fig = plt.figure()
        plt.title(f"{search_month} 지출/수입")
        plt.barh(x,y, color=['b','r'],height=0.3)
        plt.subplots_adjust( top=0.7, bottom=0.4)
        plt.title("전체 수입/지출")
        
        return [fig ,gotten_money, used_money]
        
        
        

with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    with gr.Tab("viewAllData"):
        view_btn = gr.Button("가계부 보기")
        output = gr.DataFrame(headers=df_index)
        balance = gr.Number(label="Balance",interactive=False)
        
        view_btn.click(fn=viewAllData,outputs=[output,balance])
    with gr.Tab("addData"):
        add_date = gr.Textbox(value="23.07.01", label="date")
        add_type = gr.Radio(["수입", "지출"], label="type")
        add_category = gr.Dropdown(category_list, label="category")
        add_item = gr.Textbox(value="지출/수입 요인", label="item")
        add_amount = gr.Number(label="amount")
        add_note = gr.Textbox(value="세부설명",label="note")
        
        add_btn = gr.Button("Submit")
        output = gr.DataFrame()
        add_btn.click(fn=addData,
                      inputs=[add_date,add_type,add_category,add_item,add_amount,add_note],
                      outputs=output)
    with gr.Tab("deleteData"):
        view_btn = gr.Button("가계부 보기")
        output = gr.DataFrame(headers=df_index)
        balance = gr.Number(label="Balance",interactive=False)
        
        view_btn.click(fn=viewAllData,outputs=[output,balance])

        
        delete_index = gr.Number(label="index",info="삭제하려는 가계부의 index번호를 입력하세요")
        delete_btn = gr.Button("Delete")
        balance = gr.Number(label="현재 잔액")
        delete_btn.click(fn=deleteData,inputs=delete_index,outputs=balance)
        
    with gr.Tab("updateData"):
        view_btn = gr.Button("가계부 보기")
        output = gr.DataFrame(headers=df_index)
        balance = gr.Number(label="Balance",interactive=False)
        
        view_btn.click(fn=viewAllData,outputs=[output,balance])
        
        update_index = gr.Number(label="index",info="불러올 인덱스 입력")
        load_index = gr.Button("인덱스 불러오기")
        
        text = gr.Text("수정할 정보 입력")
        update_date = gr.Textbox(label="date", interactive=True)
        update_type = gr.Radio(["수입", "지출"], label="type", interactive=True)
        update_category = gr.Dropdown(category_list, label="category", interactive=True)
        update_item = gr.Textbox(value="지출/수입 요인", label="item", interactive=True)
        update_amount = gr.Number(label="amount", interactive=True)
        update_note = gr.Textbox(value="세부설명",label="note", interactive=True)
        update_btn = gr.Button("정보 업데이트 하기")
        message = gr.Textbox()
        
        load_index.click(fn=loadIndex , 
                         inputs=update_index, 
                         outputs=[update_date,update_type,update_category,update_item,update_amount,update_note])
        update_btn.click(fn=updateData, 
                         inputs =[update_index,update_date,update_type,update_category,update_item,update_amount,update_note], 
                         outputs=message)
    with gr.Tab("통계"):
        with gr.Row():
            with gr.Column():
                display = gr.Dropdown(
                choices=[
                "ALL",
                "MONTHLY",
                "WEEKLY"
                ],
                value = "ALL",
                label="통계 그래프"
        )
            with gr.Column():
                search_month = gr.Text(label="월 입력 ex)23.07")
        
        plot = gr.Plot()
        with gr.Row():
            with gr.Column():
                income_num = gr.Number(label="수입")
            with gr.Column():
                used_num = gr.Number(label="지출")
            
        display.change(barPlot_fn, inputs=[display,search_month], outputs=[plot,income_num,used_num])
        search_month.change(barPlot_fn, inputs=[display,search_month], outputs=[plot,income_num,used_num])
        demo.load(fn=barPlot_fn, inputs=[display,search_month], outputs=[plot,income_num,used_num])
        
        
        
demo.launch()