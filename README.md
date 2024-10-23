<h1>Ticket Manager</h1>
I created a simple lighweight and user-friendly Ticket Manager designed to interact using JIRA API.
<br>
<h2>FEATURES</h2>
<p><b>• JQL Search:</b> Enter JQL queries to search for issues in JIRA.</p>
<p><b>• Log Time:</b> Log time spent on existing issues, including comments for better tracking.</p>
<p><b>• Create Tickets:</b> Easily create new JIRA tickets with project keys, issue types, summaries, and descriptions.</p>

<h2>Tools</h2>
<p><b>• Python:</b> The core programming language for building the application.</p>
<p><b>• Tkinter:</b> Used for creating the GUI.</p>
<p><b>• JIRA API:</b> Interaction with JIRA's API for fetching and managing issues.</p>

<h2>Installation</h2>
<p>To run the application, ensure you have Python installed on your computer. Then, follow these steps:</p>
• First, create a json file named <em>"creds.json"</em> on the root folder where you need to put three data:

```shell
{
  "base_url": "your-jira-base-url",
  "token": "your-jira-token",
  "email": "your-work-email"
}
```
• Second, Clone the repository:
```shell
  git clone https://github.com/Code-Me-N0t/Jira-Logger-App.git
  cd JiraLoggerApp
```
• Third, install the required package/s:
```python
  pip install -r requirements.txt
```
• Fourth, run the application:
```python
  python timelogger_fe.py
```
<i>* You can also run the executable file created in the <b>dist</b> folder</i>

<h2>Usage</h2>
<p>• Launch the application</p>
<p>• Use the "Search" tab to enter your JQL query and click the "Search" button to retrieve issues</p>
<p>• In the "Log Time" tab, enter the issue key, time spent, and a comment, then click "Create" to log your time.</p>
<p>• In the "Create Ticket" tab, fill in the necessary details to create a new ticket and click "Create" to submit it.</p>

<h2>Customization</h2>
<p>You can customize the application's appearance and functionality by modifying the color_scheme.py and custom_style.py files to suit your preferences.</p>

<h2>License</h2>
This project is licensed under the GNU Lesser General Public License See the <a href="http://www.gnu.org/licenses">LICENSE</a> file for details.
