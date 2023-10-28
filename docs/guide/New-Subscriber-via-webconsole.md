<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# New Subscriber via Webconsole

## 1. Install Webconsole

If Webconsole isn't installed yet, please, follow the instructions from [this page](./3-install-free5gc.md#d-install-webconsole).

## 2. (Optional) Delete MongoDB database

If another version of free5GC was ran before, you have to delete MongoDB.
```
$ mongo --eval "db.dropDatabase()" free5gc
```
    
## 3. Run Webconsole server
```
$ cd ~/free5gc/webconsole
$ go run server.go
```
    
## 4. Use browser to connect to Webconsole
Enter `<Webconsole server's IP>:5000` in URL bar, as shown in the image below
![](https://i.imgur.com/dF0P9W2.jpg)
The default access credentials are
```
Username: admin
Password: free5gc
```

## 5. Add new subscriber
* Choose `SUBSCRIBERS` in the left side and press `New Subscriber` button
* Fill the data and press `Submit` button

![](https://i.imgur.com/aCuRJtZ.png)

Check that the new subscriber was added successfully

![](https://i.imgur.com/4is8Q9h.png)

## 6. Modify an existing subscriber
Currently, there are some issues with subscriber modification. To modify an existing subscriber, please `Delete` it first and add it again using the `New Subscriber` button for now.
