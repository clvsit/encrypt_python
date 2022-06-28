# encrypt_python

## Installation
For Linux and Windows
```bash
$ git clone https://github.com/clvsit/encrypt_python.git
$ python setup.py install
```

## Usage
First, go to the root directory of your project, then enter the following command at the command line.

```bash
encrypt -d core -f .*\.pyc -r -i
```

Where encrypt is the main body of the command, followed by various configuration parameters.

Name | Type | Description
---|---|---
`-d` or `--dir_path` | str | The directory of the python script to be encrypted 
`-f` or `--filter` | str or List[str] | Filtering rules, as strings, can specify a single regular expression or the path to the rule file; as lists, specify multiple regular expressions. **When the path of a script file meets the filter criteria, the script file will not be encrypted**.
`-o` or `--output` | str | Specify the output directory of the encrypted script file
`-i` or `--inplace` | bool |  Whether to replace the original directory, default is false, when set to true, it will automatically move the encrypted files in build to the dir_path directory and copy the original script files to the `dir_path + time.time()` directory as a backup
`-r` or `--recursive` | bool | Whether to recursively find all script files in the dir_path directory, default is false.

If the `--filter` parameter is passed in as a file path, the file will have the following format:

```text
.*\.pyc
__init__\.py
```

## Contributing
- https://www.freesion.com/article/7200461513/
