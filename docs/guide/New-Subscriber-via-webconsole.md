## New Subscriber via webconsole

### 1. [Install webconsole](https://github.com/free5gc/free5gc/wiki/Installation#d-install-webconsole)

### 2. (Optional)Delete MongoDB 

If another version of free5GC was ran before, you have to delete MongoDB.
    
    $ mongo --eval "db.dropDatabase()" free5gc
    
### 3. Run WebConsole server
```
$ cd ~/free5gc/webconsole
$ ./bin/webconsole
```
    
### 4. Use browser to connect to WebConsole
Enter **<WebConsole server's IP>:5000** in URL bar.
```
Username: admin
Password: free5gc
```
![](https://i.imgur.com/dF0P9W2.jpg)

### 5. Add new subscriber
* Choose **SUBSCRIBERS** in the left side and press **New Subscriber** button
* Fill the data and press **Submit** button

![](https://i.imgur.com/aCuRJtZ.png)

### 6. New subscriber is added successfully
![](https://i.imgur.com/4is8Q9h.png)

### 7. Modify the existed subscriber
There are some issues for subscriber modification.
If you want to modify the existed subscriber, please `Delete` it first and `New` again for now.
