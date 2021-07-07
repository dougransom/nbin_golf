# nbin_golf

The  nbin_golf project aims to provide some scripts to manipulate Croesus trade lists and various file formats used by National Bank Independent Network.

## Installing

First, install Python   3.8 or later.  [Choose the options to add python to your system path, and install for all users](https://docs.python.org/3.8/using/windows.html).


Start a command promt as **administrator**.

If you are not editing the code, install from the Python Packaging index:
`pip install natlink_golf`

If you have the sourced cloned from github:
- Build the package with the build.cmd batch file.
- Install with `flit install --symlink`


## Running 

Currently the only command available is **croesus_to_nbin_tradelist**.


usage: Converts a Croesus generated tradelist into a Mutual Fund Bulk comma seperated value (csv) file
used by National Bank Independent Network.  By default croesus creates a .txt file which is hard to work with, but with 
multiple steps you can save the .txt file as a .xlsx file.  

The output file must be edited.  You must verify the file is correct to your satisfaction.    

The bulk mutual fund trade list will be saved in AO_xxxx_yyyymmdd_n.csv where
xxxx is the advisor code, yyyymmdd is the ISO date, and n is the sequence number.  

Note orders are buy and sell only.  You can request the buys and sells are in dollar or shares.

An attempt is made to strip any orders for securities that do not have fundserv codes.

If you would like to sell all units of a  particular security, you can add a column to the Croesus
generated tradelist ‘Sell All’, and put True in that column for rows in which you would like to sell all units.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

       [-h] [-d {c,r}] [--amount_type {dollars,shares}]
       croesus_generated_orders croesus_projected_portfolio repcode
       sequence_number
Converts a Croesus generated tradelist into a Mutual Fund Bulk comma seperated value (csv) file
used by National Bank Independent Network.  By default croesus creates a .txt file which is hard to work with, but with 
multiple steps you can save the .txt file as a .xlsx file.  

The output file must be edited.  You must verify the file is correct to your satisfaction.    

The bulk mutual fund trade list will be saved in AO_xxxx_yyyymmdd_n.csv where
xxxx is the advisor code, yyyymmdd is the ISO date, and n is the sequence number.  

Note orders are buy and sell only.  You can request the buys and sells are in dollar or shares.

An attempt is made to strip any orders for securities that do not have fundserv codes.

If you would like to sell all units of a  particular security, you can add a column to the Croesus
generated tradelist ‘Sell All’, and put True in that column for rows in which you would like to sell all units.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



