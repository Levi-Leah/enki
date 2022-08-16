# Validation errors

- **`VALIDATION ERROR: VALIDATION ERROR: More than 1/3 of the lines are comments. Too many comments found`**

    Comments comprise over 1/3 of the file.

- **`VALIDATION ERROR: Unterminated conditional statement found`**

    The number of the opening conditional statements (e.g. `ifdef`, `ifndef`, `ifeval`) does not match the number of the closing conditional statements (e.g. `endif`).


- **``VALIDATION ERROR: Deprecated footnote referenceDeprecated `footnoteref` markup found``**

    The file contains the deprecated footnote reference (e.g. `footnoteref:[some text]`).

- **`VALIDATION ERROR: No empty line after the include statement found`**

    The file does not have empty lines after every include statement as shown in the example below:

    ```
    include::some-file.adoc
                                # this is an empty line
    include::other-file.adoc
    ```

- **`VALIDATION ERROR: Vanilla xrefs found`**

    The file contains vanilla xrefs (e.g. `<<some_id>>`).

- **`VALIDATION ERROR: Xrefs or links without the human readable label found`**

    The file contains xrefs or links without the human readable label (e.g. `xref:some_id[]`, `link:some-link.com[]`).

- **`VALIDATION ERROR: Nesting in modules found`**

    The module contains includes of files other than snippets (e.g. modules or assemblies).

- **`VALIDATION ERROR: Multiple abstract tags found`**

    The file contains multiple abstract tags (`[role="_abstract"]`).


- **`VALIDATION ERROR: "Related information" section found`**

    The file contains `Related information` section instead of the `Additional recourse` section.


<!--- **`VALIDATION ERROR: `**


- **`VALIDATION ERROR: `**


- **`VALIDATION ERROR: `**-->
