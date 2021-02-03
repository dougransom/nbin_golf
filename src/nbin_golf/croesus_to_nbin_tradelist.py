#python script to convert a croesus rebalancing output to a national bank independent network
#mutual fund trade list.

import pandas as pd
import numpy as np
import argparse
import sys
import datetime as dt
import os
from enum import Enum
from pathlib import Path, PureWindowsPath

pd.set_option('display.min_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class OrderType(Enum):
    SELL=6
    BUY=5
    SWITCH=8
    
class AmountTypeCode(Enum):
    DOLLAR_AMOUNT='D'
    SHARES='S'
    ALL_SHARES='A'
    DSC_FREE='F'
    MATURED_ONY='M'
    FREE_ONLY='T'    #ten percent free

class DividendOption(Enum):
    CASH=4,
    REINVEST=1

#!this will reset when the script starts
default_trade_amount_type=AmountTypeCode.DOLLAR_AMOUNT
 
source_id="ABCD"


amount_type_code="D"
blank_gross=""
client_paid_commission="0"
dividend_option=""
blank_from_id=""
additional_commission="0"

mvsc="Market Value Security Currency"

def getTemplateFileName():
    return  Path(__file__).parent/"Mutual Fund File Template.xlsx"

def process_file(infile,outfile):
    df=pd.read_excel(infile)
    if not "Sell All" in df.columns:
        df['Sell All']=False
    df['Sell All'] =  df['Sell All'].replace(np.nan,False)
    print(f"\nsell all\n {df['Sell All']}")

    if False:
        #this is for reading csv, currently unused
        #pandas doesn't handle "," in strings when converting to numeric
        #rip the commas out
        def fn(str):
            return str.replace(",","")
        df[mvsc]=df[mvsc].apply(fn)
        print(df[mvsc])

        #now convert to numeric
        df[mvsc]=pd.to_numeric(df[mvsc])


    global template
    print(f"df \n{df}")
    excel_template_path=getTemplateFileName()
    print(f"Reading {excel_template_path}") 
    template=pd.read_excel(excel_template_path)
    trades=pd.DataFrame(columns=template.columns)
    print(f"Blank trades {trades}")

    trades=df.apply(order,axis=1,result_type="expand")
    trades.columns = template.columns
    trade_mask = trades["Source identification"]!="No Trade"
    trades=trades[trade_mask]
    print(f"Trades \n{trades}\n {trades.to_csv()}")
    trades.to_csv(ofile)




def order(row):
    account,symbol, security,read_dollar_amount, read_quantity,sell_all  = row['Account No.'], row['Symbol'], \
        str(row['Security']), row[mvsc],row['Quantity'],row['Sell All']
    order_type=str(row["Type"])
    company_code=symbol[0:3]
    fund_code_number=symbol[3:]
    print(f"\n Company code {company_code} Fund Code {fund_code_number} amount {read_dollar_amount} Symbol {symbol} Security {security}" )
    ignore_row=True
    if ignore_row := (security[0] != '9'):
        print(f"Warning {symbol} not a fund code, ignored")
        return [symbol]+["No Trade"]*(-1+len(template.columns))

    no_dash_account = account.replace("-","")
    trade_amount_type = default_trade_amount_type
    if order_type=="Buy":
        dollar_amount=-1*read_dollar_amount
        trade_code=OrderType.BUY.value
        quantity=read_quantity
        row_dividend_option=dividend_option
    else:
        if sell_all:
            trade_amount_type = AmountTypeCode.ALL_SHARES
            quantity = ""
        else:
            dollar_amount=read_dollar_amount
            quantity=-1*read_quantity

        row_dividend_option=""
        trade_code=OrderType.SELL.value

    front_cols=[company_code,source_id,fund_code_number,\
        no_dash_account,trade_code,"",trade_amount_type.value,blank_gross]
    
    back_cols=[client_paid_commission,row_dividend_option,blank_from_id,additional_commission,"",""]

    trade_amount = dollar_amount if trade_amount_type == AmountTypeCode.DOLLAR_AMOUNT \
        else  quantity if default_trade_amount_type == AmountTypeCode.SHARES \
        else 0
    
    result = front_cols+[trade_amount]+back_cols
     
    return result


import argparse

description = """Converts a Croesus generated tradelist into a Mutual Fund Bulk comma seperated value (csv) file
used by National Bank Independent Network.  By default croesus creates a .txt file which is hard to work with, but with 
multiple steps you can save the .txt file as a .xslx file.  

The output file must be edited.  You must verify the file is correct to your satisfaction and remove the first column 
in order to be compatible with the National Bank Independent Network bulk mutual fund format.  

The bulk mutual fund trade list will be saved in AO_xxxx_yyyymmdd_n.csv where
xxxx is the advisor code, yyyymmdd is the ISO date, and n is the sequence number.  

Note orders are buy and sell only.  You can request the buys and sells are in dollar or shares.

An attempt is made to strip any orders for securities that do not have fundserv codes.

If you would like to sell all units of a  particular security, you can add a column to the Croesus
generated tradelist ‘Sell All’, and put True in that column for rows in which you would like to sell all units.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




"""

parser = argparse.ArgumentParser(description)
parser.add_argument("-d", choices=['c','r'],
                    help = "c for cash dividends, r for reinvest dividends (default)")

parser.add_argument("--amount_type", choices=['dollars','shares'],default="dollars",
                    help = "orders to be submited in dollars or shares. default is dollars")

parser.set_defaults(d='r')
croesus_help="""The generated orders from a Croesus rebalancing activity, saved as a .xslx file.
You may add a column to that .xslx file (in any position) called ‘Sell All’. 
Place a ‘True’ in any row with a sell action, where you would like to sell all units.  Leave it blank
otherwise.  
"""



parser.add_argument("croesus_generated_orders",help=croesus_help)
parser.add_argument("repcode",help="""A repcode to be used in the file name.  It can be any string, but you would be wise
                              to use any of your own repcodes.""")
parser.add_argument("sequence_number",help="""A number to append to the file name, in case you submit more than one file
for mutual fund bulk trading in any particular day.   """)




def main():
    args = parser.parse_args()
    print(f"Args ok {args}")
    dividend_option = 4 if args.d == "c" else 1  # 1 is reinvest, 4 is cash
    default_trade_amount_type = AmountTypeCode.DOLLAR_AMOUNT if args.amount_type == "dollars" else AmountTypeCode.SHARES
    # Press the green button in the gutter to run the script.
    print(args.croesus_generated_orders)

    print(f"{sys.argv}")
    global infile, repcode,sequence_number,dt_v,source_id,ofile
    (infile, repcode, sequence_number) = (args.croesus_generated_orders,args.repcode,args.sequence_number)

    dt_v = dt.datetime.now().date()
    date_str=f"{dt_v}".replace("-","")

    source_id=repcode

    print(f"infile {infile} repcode {repcode} Sequence Number {sequence_number} date {date_str}")
    ofile=f"AO_{repcode}_{date_str}_{sequence_number}.csv"
    print(f"creating output file {ofile}")
    process_file(infile,ofile)


if __name__ == "__main__":
    main()