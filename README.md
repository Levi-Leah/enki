# enki

## Installation

1. Clone the repository:
```bash
git@github.com:Levi-Leah/enki.git
```
1. Navigate to the root directory of the repository:
```bash
cd enki
```
1. Run the installation script:
```bash
sh install.sh
```

## Verification steps
* To verify enki is installed, run:
```bash
enki -h
```

## Troubleshooting
* If you can't run the commands, source your `~/.baschrc` file or restart your terminal:
```bash
source ~/.bashrc
```

## Usage

* To see the help message, use:
```bash
enki -h
```

* To validate files, use:
```bash
enki validate <PATH>
```
Replace `<PATH>` with the path to a valid `build.yml` file, valid `.adoc` file, or with the path to a directory conatining your `.adoc` files.


* To generate a `build.yml` from a template, run:
```bash
enki generate <PATH>
```
Replace `<PATH>` with the path to a valid directory where you want to generate the `build.yml`.

## Reporting a bug
[Issue tracker](https://github.com/Levi-Leah/enki/issues)


## License
[MIT](https://choosealicense.com/licenses/mit/)
