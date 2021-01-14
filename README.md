# site_compare
little tiny piece of code to compare two site by determining the screenshot of each given path

# Usage

download `chromedriver` from https://chromedriver.chromium.org/getting-started and place it in `os.path.getcwd()`

`-s` to specify the smartphone mode

```bash
$ python site_compare.py -p path.txt site-1.com site-2.com
```
* `path.txt` contain all the available path of the given site
* `site-1.com` and `site-2.com` target site (without the http or https protocol)

after execution finish the program will generate an `output` folder in `os.path.getcwd()`

```bash
├── output
│   ├── site-1
│   │   ├── output
│   │   │   ├── ...path.png (output after compare)
│   │   ├── ...path.png (screenshots)
│   ├── site-2
│   │   ├── output
│   │   │   ├── ...path.png (output after compare)
│   │   ├── ...path.png (screenshots)
```
and `result.txt` in `os.path.getcwd()` contain the similarity output of the both sites
