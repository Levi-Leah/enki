# enki

Command-line validation tool.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Levi-Leah/enki.git
    ```

1. Navigate to the root directory of the repository:
    ```bash
    cd enki
    ```

1. Run the installation script:
    ```bash
    sh install.sh
    ```

1. Source your `~/.bashrc` file:
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
    Replace `<PATH>` with the path to files or directories you want to validate.

* To print one validation error per line, run:
    ```bash
    enki validate --oneline <PATH>
    ```
    Replace `<PATH>` with the path to files or directories you want to validate.

* To validate the links, run:
    ```bash
    enki validate --links <PATH>
    ```
    **Note**
    Validation can only be performed on `master.adoc` files.


**Note**
`enki` does not descend into symlinks.

## Examples

* To validate all files in the directory, run:
    ```bash
    enki validate path/
    ```

* To validate a specific file or files, run:
    ```bash
    enki validate path/to/file.adoc
    ```

* To validate all files that match a global pattern, run:
    ```bash
    enki validate path/to/**/**/*adoc
    ```

* To validate all files that match the special character, run:
    ```bash
    enki validate path/to/*adoc
    ```

* To validate files and print one validation error per line, run:
    ```bash
    enki validate --oneline path/to/*adoc
    ```

* To validate links, run:
    ```bash
    enki validate --links path/to/dir/
    ```

## Error messages

`enki` has the following errors:

- enki errors
- validation errors
- link errors

### enki errors

enki errors occur when `enki` is unable to perform the validation.

For more information, see [enki error messages](docs/error-msg.md).

### Validation errors

Validation errors occur when the files you are validating did not pass the validation checks.

For more information, see [validation error messages](docs/error-msg.md).

### Link errors

Link errors occur when the link can not be resolved.

For more information, see [link error messages](docs/error-msg.md).

## Reporting a bug
[Issue tracker](https://github.com/Levi-Leah/enki/issues)


## License
[MIT](https://choosealicense.com/licenses/mit/)
