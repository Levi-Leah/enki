# enki

Command-line validation tool.

## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:Levi-Leah/enki.git
    ```

1. Navigate to the root directory of the repository:
    ```bash
    cd enki
    ```

1. Switch to the `oop` branch:
    ```bash
    git checkout oop
    ```

1. Run the installation script:
    ```bash
    sh install.sh
    ```

1. Source your `~/.baschrc` file:
    ```bash
    source ~/.bashrc
    ```

## Verification steps

* To verify that `enki` is installed, run:
    ```bash
    enki -h
    ```

## Usage

* To see the help message, run:
    ```bash
    enki -h
    ```

* To validate the files, run:
    ```bash
    enki validate <PATH>
    ```
    Replace `<PATH>` with one of the following options:

    * Path to the valid `build.yml` file
    * Path to the valid `.adoc` file
    * Path to a directory containing `.adoc` files

* To generate a `build.yml` from a template, run:
    ```bash
    enki generate <PATH>
    ```
    Replace `<PATH>` with the path to a directory where you want to generate the `build.yml` file.

## Reporting a bug
[Issue tracker](https://github.com/Levi-Leah/enki/issues)


## License
[MIT](https://choosealicense.com/licenses/mit/)
