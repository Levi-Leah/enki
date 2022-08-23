# Enki error messages

| Error message  | Description |
| ------------- | ------------- |
| ERROR: '<PATH/TO/FILE>' doesn't exist in your repository. | The path to the files you provided does not exist.|
| ERROR: Unsupported file format. The following files cannot be validated | The files you are trying to validate are not `.adoc` files.|

# Validation error messages

| Error message  | Description |
| ------------- | ------------- |
| ERROR: More than 1/3 of the lines are comments. Too many comments found | Comments comprise over 1/3 of the file. |
| ERROR: Unterminated conditional statement found|The number of the opening conditional statements (e.g. `ifdef`, `ifndef`, `ifeval`) does not match the number of the closing conditional statements (e.g. `endif`). |
| ERROR: Deprecated \`footnoteref\` markup found | The file contains the deprecated footnote reference (e.g. `footnoteref:[some text]`). |
| ERROR: No empty line after the include statement found | The file does not have empty lines after include statements. |
| ERROR: Vanilla xrefs found | The file contains vanilla xrefs (e.g. `<<some_id>>`). |
| ERROR: Xrefs or links without the human readable label found | The file contains xrefs or links without the human readable label (e.g. `xref:some_id[]`, `link:some-link.com[]`). |
| ERROR: Nesting in modules found | The module contains includes of files other than snippets (e.g. modules or assemblies). |
| ERROR: "Related information" section found | The file contains `Related information` section instead of the `Additional recourses` section. |

# Link error messages
| Error message  | Description |
| ------------- | ------------- |
| 404 | Page not found. |
| 403 | Restricted or forbidden access. Most likely, link is behind pay wall. |
| Bad URI | The link uses xref syntax. (e.g. `xref:http:://some-link.com[]`) |
| Invalid URL | Most likely, the link contains an unresolved attribute (e.g. link:http:://some-link-{attribute}.com[]). |
