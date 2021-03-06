a colourgame~

much thanks to [Anthony Luo](https://github.com/antholuo) for helping me too many times.

# Installation Instructions
Installation is different on Windows and MacOS. Please read carefully
## Windows Installation
1. Install VLC 64-bit. You can do so by clicking [here](https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe).
2. Clone the entire repository wherever you would like. A link to the top level of the repository can be found by clicking [here](https://github.com/Chrisytz/I-Love-Hue-python-ver).
    - It is important that you clone the entire repository. Dependencies have not been packaged with the exe.
    - If you're struggling to clone the repository, click [here](https://github.com/Chrisytz/I-Love-Hue-python-ver) and then click the green `'code'` arrow in the top right corner., which will open a dropdown like this. Then click on 'download zip'.
    - ![image](https://user-images.githubusercontent.com/45152791/126379142-161d5f31-77d1-49f9-a0c1-aee835504ad9.png). 
3. Open the repository within your file system. Unpack the zip file wherever you would like.
4. In the unpacked folder, find `main.exe`, and double-click to run on windows.
5. If windows security blocks you from playing the game click 'More info' and then 'Run anyways'.
![image](https://user-images.githubusercontent.com/52107461/126377564-a232f23a-10ab-40e5-bd07-b351bda47d17.png)![image](https://user-images.githubusercontent.com/52107461/126377733-dadaeb99-c9f6-4032-ac65-60eb7829b0d2.png)

## MacOS Installation
1. Install VLC 64-bit. You can do so by clicking [here](https://www.videolan.org/vlc/download-macosx.html).
2. Clone the entire repository wherever you would like. A link to the top level of the repository can be found by clicking [here](https://github.com/Chrisytz/I-Love-Hue-python-ver).
    - It is important that you clone the entire repository. Dependencies have not been packaged with the exe.
    - If you're struggling to clone the repository, click [here](https://github.com/Chrisytz/I-Love-Hue-python-ver) and then click the green `'code'` arrow in the top right corner., which will open a dropdown like this. Then click on 'download zip'.
    - ![image](https://user-images.githubusercontent.com/45152791/126379142-161d5f31-77d1-49f9-a0c1-aee835504ad9.png). 
3. Open the repository within your file system. Unpack the zip file wherever you would like.
4. If you have python and pip installed, skip to step #7. If you have a python IDE, you can now open the repository, install dependencies, and run `main.py`.
5. run `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
6. run `python get-pip.py`
7. Navigate to the unpacked repository.
8. run `pip install -r requirements.txt`
9. run `python main.py`
10. profit!

* note: We are unclear about the compatibility of the exe with wine. Feel free to try.

### Useful commands for codebase
Install all dependencies:
```python
pip install -r requirements.txt
```
update dependencies:
```python
pip freeze > requirements.txt
```

There are (afaik) no packages which are dependent on version, so >= can be used for all requirements. -Anni.

## Some thoughts
Chris worked really hard for this game! Hope you guys get to enjoy :).
![](https://d.newsweek.com/en/full/822411/pikachu-640x360-pokemon-anime.jpg?w=1600&h=1600&q=88&f=b65592079ef009b8b80897ddb8660b29)


## License
 
The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
