1. Over tainting data out of db… Assumption:
       - Unlike sample real world apps, most customer apps would be using model.Models for inserting data into the db as well.
       - Even if we tainting data which is otherwise safe (added thru admin/console), it will take few more explicit steps to be flagged as XSS. 
       - Above 2 assumptions should keep FPs in check, if we hear complains we can tune it down based on usage of corresponding ModelForm or model.Models.save() method.

2. If by flagging for mark_safe et al as XSS sinks, we land up not cutting the data flow path and we land up with 2 XSS flaws, i.e. flaw in Python code at mark_safe and in template when it’s rendered, we should remove mark_safe as sink and look for form and formset initialized with `initial` or `data` variable and continue taint tracking.

ToDo:
- SQLi Sinks for extra(), ...
- DetailView, CreateView, *View enhanced examples. Expand on Django 2.x testcases
- If any Django eco-system plugin which is super popular needs to be supported
