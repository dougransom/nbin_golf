# nbin_golf

The  nbin_golf project aims to provide some scripts to manipulate Croesus trade lists and various file formats used by National Bank Independent Network.

#Installing

First, install Python, later than Python 3.8.  [Choose the options to add python to your system path](https://docs.python.org/3.8/using/windows.html).


Start a command promt as **administrator**.

If you are not editing the code, install from the Python Packaging index:
`pip install natlink_golf`

If you have the sourced cloned from github:
- Build the package with the build.cmd batch file.
- Install with `flit install --symlink`


#Running 

Currently the only command available is **croesus_to_nbin_tradelist**.


usage: Converts a Croesus generated tradelist into a Mutual Fund Bulk comma seperated value (csv) file
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

       [-h] [-d {c,r}] [--amount_type {dollars,shares}]
       croesus_generated_orders repcode sequence_number

positional arguments:
  croesus_generated_orders
                        The generated orders from a Croesus rebalancing
                        activity, saved as a .xslx file. You may add a column
                        to that .xslx file (in any position) called ‘Sell
                        All’. Place a ‘True’ in any row with a sell action,
                        where you would like to sell all units. Leave it blank
                        otherwise.
  repcode               A repcode to be used in the file name. It can be any
                        string, but you would be wise to use any of your own
                        repcodes.
  sequence_number       A number to append to the file name, in case you
                        submit more than one file for mutual fund bulk trading
                        in any particular day.

optional arguments:
  -h, --help            show this help message and exit
  -d {c,r}              c for cash dividends, r for reinvest dividends
                        (default)
  --amount_type {dollars,shares}
                        orders to be submited in dollars or shares. default is
                        dollars

